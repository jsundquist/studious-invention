from typing import Any

from pyzeebe import ZeebeClient, create_insecure_channel

from config import config


async def start_process(bpmn_process_id: str, variables: dict[str, Any]) -> str:
    channel = create_insecure_channel(grpc_address=config.zeebe_address)
    client = ZeebeClient(channel)
    try:
        instance_key = await client.run_process(
            bpmn_process_id=bpmn_process_id,
            variables=variables,
        )
    finally:
        await channel.close()
    return str(instance_key)
