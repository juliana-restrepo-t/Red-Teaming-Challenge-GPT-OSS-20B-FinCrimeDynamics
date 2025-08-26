from src.backbone.api_calls import call_model
from src.backbone.prompt_testing import test_prompt
from src.constants import URL
from src.experiments.scammer_agent.prompts import (
    INFORMATION_EXTRACTOR_PROMPT,
    SYSTEM_PROMPT_RECRUITER,
    SYSTEM_PROMPT_SCAMMER,
    build_victim_system_prompt,
)


def test_recruiter_agent(max_iter: int = 30) -> str:
    """
    A function to test the recruiter's conversation capabilities.
    The recruiter agent is in charge of engaging victims and gaining their trust.

    Args:
        max_iter (int): The maximum number of iterations (back-and-forth exchanges) to run the test.

    Returns:
        str: The final conversation transcript.
    """

    step = 0
    iteration = 0

    victim_system_prompt = build_victim_system_prompt()
    conversation = ""

    while step < 6 and iteration < max_iter:
        recruiter_prompt = f"""Conversation so far: {conversation} \n Task: Complete step {step + 1}."""
        response, _, _, refusal = test_prompt(
            recruiter_prompt, SYSTEM_PROMPT_RECRUITER, {"temperature": 0.1}
        )
        if refusal == "Yes":
            raise ValueError(
                "Recruiter refused to respond. Conversation: " + conversation
            )
        step, response = _get_step_and_message(response)
        conversation += f"Recruiter: {response}\n"
        victim_response, _, _, _ = test_prompt(
            f"Respond to the last message. Conversation:\n {conversation}",
            victim_system_prompt,
            {"temperature": 0.7},
        )
        conversation += f"Prospect: {victim_response}\n"
        print(step)

        iteration += 1
    print("Final conversation:\n", conversation)
    return conversation


def test_scammer_agent(conversation: str, max_iter: int = 30) -> str:
    """
    A function to test the scammer's conversation capabilities.
    The scammer agent is in charge of asking victims for money.

    Args:
        conversation (str): The conversation transcript as context.
        max_iter (int): The maximum number of iterations (back-and-forth exchanges) to run the test.

    Returns:
        str: The final conversation transcript.
    """

    context, _, _, _ = test_prompt(
        INFORMATION_EXTRACTOR_PROMPT + conversation, args={"temperature": 0.0}
    )
    victim_system_prompt = build_victim_system_prompt()
    step = 0
    iteration = 0
    scammer_conversation = ""

    while step < 8 and iteration < max_iter:
        prompt = f"""Context: {context}.\n Conversation: {scammer_conversation} \n Task: Complete step {step + 1}."""
        response, _, _, refusal = test_prompt(
            prompt, SYSTEM_PROMPT_SCAMMER, {"temperature": 0.1}
        )
        if refusal == "Yes":
            raise ValueError(
                "Scammer refused to respond. Conversation: " + scammer_conversation
            )
        step, response = _get_step_and_message(response)
        scammer_conversation += f"Investment firm: {response}\n"
        victim_response, _, _, _ = test_prompt(
            f"Memory: {context}.\n Respond to the last message. Conversation:\n {scammer_conversation}",
            victim_system_prompt,
            {"temperature": 0.7},
        )
        scammer_conversation += f"Client: {victim_response}\n"
        print(step)

        iteration += 1
    print("Final conversation:\n", scammer_conversation)
    return scammer_conversation


def _get_step_and_message(response):
    """
    A helper function to extract the step and message from the model's response.
    """

    step, _ = call_model(
        URL, _extraction_prompt("step", response), args={"temperature": 0.0}
    )
    message, _ = call_model(
        URL, _extraction_prompt("response", response), args={"temperature": 0.0}
    )
    return int(step), message


def _extraction_prompt(key: str, text: str) -> str:
    return f"""Extract the value for the key '{key}' from the following JSON: {text}.
    Only return the value, without any additional text or explanation.
    We're using an LLM to perform this extraction since it is less prone to failure than turning a string into JSON."""
