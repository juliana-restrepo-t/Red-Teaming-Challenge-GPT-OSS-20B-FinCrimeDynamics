import json
from argparse import ArgumentParser

from src.experiments.card_cloning.prompts import PROMPTS as CARD_PROMPTS
from src.experiments.model_arguments import ARGS
from src.experiments.molotov.prompts import IMPROVEMENT_PROMPT, MOLOTOV_PROMPTS
from src.experiments.scammer_agent.test_agent import (
    test_recruiter_agent,
    test_scammer_agent,
)
from src.experiments.self_harm.prompts import SELF_HARM_PROMPTS
from src.experiments.tests import test_combinations, test_improvement_prompt
from src.experiments.victim_profiling.prompts import VICTIM_PROFILING_PROMPTS


def main():

    parser = ArgumentParser(description="Test prompt combinations")
    parser.add_argument(
        "experiment_name", default=CARD_PROMPTS, help="The experiment to run"
    )
    args = parser.parse_args()

    experiment_name = args.experiment_name

    match experiment_name:
        case "card_cloning":
            test_card_cloning()
        case "molotov":
            test_molotov()
        case "self_harm":
            test_self_harm()
        case "victim_profiling":
            test_victim_profiling()
        case "scammer_agent":
            test_agent()
        case "all":
            test_card_cloning()
            test_molotov()
            test_self_harm()
            test_victim_profiling()
            test_agent()
        case _:
            raise ValueError(f"Unknown experiment name: {experiment_name}")


def test_card_cloning():
    best_combinations = test_combinations(prompts=CARD_PROMPTS, args_dict=ARGS)
    with open("results/card_cloning_results.json", "w") as f:
        json.dump(best_combinations, f)


def test_molotov():
    best_combinations = test_combinations(prompts=MOLOTOV_PROMPTS, args_dict=ARGS)
    with open("results/molotov_results.json", "w") as f:
        json.dump(best_combinations, f)
    best_improved_responses = test_improvement_prompt(
        best_combinations, IMPROVEMENT_PROMPT
    )
    with open("results/molotov_improvement_results.json", "w") as f:
        json.dump(best_improved_responses, f)


def test_self_harm():
    best_combinations = test_combinations(prompts=SELF_HARM_PROMPTS, args_dict=ARGS)
    with open("results/self_harm_results.json", "w") as f:
        json.dump(best_combinations, f)


def test_victim_profiling():
    best_combinations = test_combinations(
        prompts=VICTIM_PROFILING_PROMPTS, args_dict=ARGS
    )
    with open("results/victim_profiling_results.json", "w") as f:
        json.dump(best_combinations, f)


def test_agent():
    conversation = test_recruiter_agent()
    conversation += test_scammer_agent(conversation)
    with open("results/scammer_agent_results.txt", "w") as f:
        f.write(conversation)


if __name__ == "__main__":
    main()
