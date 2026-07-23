import asyncio
import signal

import structlog
from pyzeebe import ZeebeWorker, create_insecure_channel

from config import config
from handlers import provisioning
from logging_config import configure_logging

configure_logging(log_level=config.log_level)
logger = structlog.get_logger(__name__)


async def run() -> None:
    logger.info("starting worker", zeebe_address=config.zeebe_address)

    channel = create_insecure_channel(grpc_address=config.zeebe_address)
    worker = ZeebeWorker(channel)

    provisioning.register(worker)

    loop = asyncio.get_running_loop()

    def _shutdown(sig: signal.Signals) -> None:
        logger.info("shutdown signal received", signal=sig.name)
        loop.stop()

    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, _shutdown, sig)

    logger.info("worker polling for jobs")
    await worker.work()


if __name__ == "__main__":
    asyncio.run(run())
