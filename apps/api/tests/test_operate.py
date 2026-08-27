import httpx
import respx

import services.operate as operate

SAMPLE_BPMN = """<?xml version="1.0" encoding="UTF-8"?>
<bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL">
  <bpmn:process id="sample-process" name="Sample Process" isExecutable="true">
    <bpmn:subProcess id="phase-1" name="Phase 1">
      <bpmn:userTask id="review-task" name="Review Task">
        <bpmn:documentation>docs/steps/review-task.md</bpmn:documentation>
      </bpmn:userTask>
      <bpmn:serviceTask id="provision-task" name="Provision Task" />
    </bpmn:subProcess>
  </bpmn:process>
</bpmn:definitions>"""


def test_parse_phases_from_bpmn_extracts_steps_and_doc_path() -> None:
    phases = operate._parse_phases_from_bpmn(SAMPLE_BPMN)

    assert len(phases) == 1
    phase = phases[0]
    assert phase.id == "phase-1"
    assert phase.name == "Phase 1"
    assert len(phase.steps) == 2

    review_step = next(s for s in phase.steps if s.id == "review-task")
    assert review_step.type == "userTask"
    assert review_step.documentation_path == "docs/steps/review-task.md"

    provision_step = next(s for s in phase.steps if s.id == "provision-task")
    assert provision_step.type == "serviceTask"
    assert provision_step.documentation_path is None


def test_parse_phases_from_bpmn_with_no_process_element() -> None:
    assert (
        operate._parse_phases_from_bpmn(
            '<?xml version="1.0"?><bpmn:definitions '
            'xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL"/>'
        )
        == []
    )


@respx.mock
async def test_list_process_definitions_maps_response() -> None:
    respx.post(f"{operate.OPERATE_URL}/api/login").mock(return_value=httpx.Response(204))
    respx.post(f"{operate.OPERATE_URL}/v1/process-definitions/search").mock(
        return_value=httpx.Response(
            200,
            json={
                "items": [
                    {"bpmnProcessId": "sample-process", "name": "Sample", "version": 3, "key": 42}
                ]
            },
        )
    )

    result = await operate.list_process_definitions()

    assert len(result) == 1
    assert result[0].id == "sample-process"
    assert result[0].name == "Sample"
    assert result[0].version == 3
    assert result[0].definition_key == "42"


@respx.mock
async def test_get_process_definition_returns_none_when_not_found() -> None:
    respx.post(f"{operate.OPERATE_URL}/api/login").mock(return_value=httpx.Response(204))
    respx.post(f"{operate.OPERATE_URL}/v1/process-definitions/search").mock(
        return_value=httpx.Response(200, json={"items": []})
    )

    assert await operate.get_process_definition("missing") is None


@respx.mock
async def test_get_process_definition_returns_detail_with_phases() -> None:
    respx.post(f"{operate.OPERATE_URL}/api/login").mock(return_value=httpx.Response(204))
    respx.post(f"{operate.OPERATE_URL}/v1/process-definitions/search").mock(
        return_value=httpx.Response(
            200,
            json={
                "items": [
                    {
                        "bpmnProcessId": "sample-process",
                        "name": "Sample",
                        "version": 1,
                        "key": 42,
                    }
                ]
            },
        )
    )
    respx.get(f"{operate.OPERATE_URL}/v1/process-definitions/42/xml").mock(
        return_value=httpx.Response(200, text=SAMPLE_BPMN)
    )

    detail = await operate.get_process_definition("sample-process")

    assert detail is not None
    assert detail.definition_key == "42"
    assert len(detail.phases) == 1
    step_ids = {step.id for step in detail.phases[0].steps}
    assert step_ids == {"review-task", "provision-task"}


@respx.mock
async def test_get_instance_returns_none_on_404() -> None:
    respx.post(f"{operate.OPERATE_URL}/api/login").mock(return_value=httpx.Response(204))
    respx.get(f"{operate.OPERATE_URL}/v1/process-instances/999").mock(
        return_value=httpx.Response(404)
    )

    assert await operate.get_instance("999") is None


@respx.mock
async def test_get_instance_returns_json_body() -> None:
    respx.post(f"{operate.OPERATE_URL}/api/login").mock(return_value=httpx.Response(204))
    respx.get(f"{operate.OPERATE_URL}/v1/process-instances/1").mock(
        return_value=httpx.Response(
            200, json={"bpmnProcessId": "sample-process", "state": "ACTIVE"}
        )
    )

    result = await operate.get_instance("1")

    assert result == {"bpmnProcessId": "sample-process", "state": "ACTIVE"}


@respx.mock
async def test_get_active_elements_filters_by_active_state() -> None:
    respx.post(f"{operate.OPERATE_URL}/api/login").mock(return_value=httpx.Response(204))
    route = respx.post(f"{operate.OPERATE_URL}/v1/flow-node-instances/search").mock(
        return_value=httpx.Response(200, json={"items": [{"flowNodeId": "review-task"}]})
    )

    result = await operate.get_active_elements("1")

    assert result == [{"flowNodeId": "review-task"}]
    sent_body = route.calls.last.request.content
    assert b'"state":"ACTIVE"' in sent_body or b'"state": "ACTIVE"' in sent_body


@respx.mock
async def test_get_completed_elements_filters_by_completed_state() -> None:
    respx.post(f"{operate.OPERATE_URL}/api/login").mock(return_value=httpx.Response(204))
    route = respx.post(f"{operate.OPERATE_URL}/v1/flow-node-instances/search").mock(
        return_value=httpx.Response(200, json={"items": []})
    )

    result = await operate.get_completed_elements("1")

    assert result == []
    sent_body = route.calls.last.request.content
    assert b'"state":"COMPLETED"' in sent_body or b'"state": "COMPLETED"' in sent_body
