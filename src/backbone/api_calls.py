import time
import traceback
from typing import Any, Tuple

import requests

from src.constants import CONSTANT_PARAMS, MIN


def send_post_request(
    url: str, data: dict[str, Any], max_retries: int = 10
) -> dict[str, str] | None:
    """
    Send a POST request to the specified URL with the given data.

    Args:
      url: The URL to send the request to.
      data: The data to send in the request.

    Returns:
      The JSON response from the server, or None if an error occurred.
    """

    successful = False
    iteration = 0

    while not successful and iteration < max_retries:
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            if "error" not in response.json():
                successful = True
            else:
                time.sleep(60 * MIN)
        except requests.exceptions.RequestException as e:
            traceback.print_exc()
            print(f"An error occurred: {e}. Sleeping for {MIN} minutes before retrying")
            time.sleep(60 * MIN)
        iteration += 1

    try:
        res = response.json()
    except Exception:
        res = None

    return res


def call_model(
    url: str,
    prompt: str,
    system_prompt: str | None = None,
    args: dict[str, Any] | None = None,
) -> Tuple[str, str]:
    """
    Call the model at the specified URL with the given prompt, system prompt, and arguments.

    Args:
      url: The URL to call the model at.
      prompt: The prompt to send to the model.
      system_prompt: The system prompt to send to the model.
      args: The arguments to send to the model.

    Returns:
      The response from the model.
    """

    data = {"prompt": prompt}
    if system_prompt is not None:
        data["system"] = system_prompt
    data.update(args)
    data.update(CONSTANT_PARAMS)
    response = send_post_request(url, data)
    return response.get("response", ""), response.get("thinking", "")  # type: ignore
