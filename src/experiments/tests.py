from typing import Any

from tqdm import tqdm

from src.backbone.prompt_testing import print_test_results, test_prompt
from src.constants import URL


def test_combinations(
    prompts: dict[str, str],
    args_dict: dict[str, dict[str, int | float]] | None = None,
    system_prompts: dict[str, str] | None = None,
) -> list[dict[str, Any]]:
    """
    Test all combinations of prompts and arguments.

    Args:
      prompts: A dictionary of prompts to test.
      args_dict: A dictionary of argument sets to test.
      system_prompts: A dictionary of system prompts to use.

    Returns:
      A dictionary with the best combinations.
    """

    if system_prompts is None:
        system_prompts = {"default (None)": None}

    if args_dict is None:
        args_dict = {"default": {}}

    best_combinations = []

    for prompt_name, prompt in prompts.items():
        for args_name, args in args_dict.items():
            for system_prompt_name, system_prompt in system_prompts.items():
                print(
                    f"Testing prompt '{prompt_name}' with args '{args_name}' and system prompt '{system_prompt_name}'"
                )
                response, thinking, iter, refused = test_prompt(
                    prompt, system_prompt, args
                )
                print_test_results(response, iter, refused)
                if refused != "Yes":
                    best_combinations.append(
                        {
                            "prompt": prompt_name,
                            "args": args_name,
                            "system_prompt": system_prompt_name,
                            "response": response,
                            "thinking": thinking,
                            "iterations": iter,
                        }
                    )
    return best_combinations


def test_improvement_prompt(
    best_combinations: list[dict[str, Any]], improvement_prompt: str
) -> list[dict[str, Any]]:
    """
    A function that tests the improvement prompt on the best combinations of the
    original prompts and their responses.

    Args:
        best_combinations: A list of the best combinations of prompts and their responses.
        improvement_prompt: The prompt to use for improving the responses.

    Returns:
        A list of the improved responses.
    """

    improved_responses = []
    for combination in tqdm(best_combinations):
        print(combination)
        response = combination["response"]
        print(response)
        improved_response, thinking, iter, refused = test_prompt(
            URL, improvement_prompt + response
        )
        print_test_results(improved_response, iter, refused)
        if refused != "Yes":
            improved_responses.append(
                {
                    "original_prompt": combination["prompt"],
                    "thinking": thinking,
                    "args": combination["args"],
                    "system_prompt": combination["system_prompt"],
                    "original_response": response,
                    "improved_response": improved_response,
                    "iterations": iter,
                }
            )
    return improved_responses
