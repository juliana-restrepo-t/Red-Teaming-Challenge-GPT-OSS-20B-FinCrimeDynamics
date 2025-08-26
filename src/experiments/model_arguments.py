max_randomness_args = {
    "temperature": 1,
    "top_p": 1,
    "top_k": 500,  # A high value for top_k allows for more diverse outputs
}

deterministic_args = {
    "temperature": 0,
    "top_k": 1,  # Redundant but included for clarity
}

default_args = {"temperature": 0.8, "top_p": 0.95, "top_k": 40}

ARGS = {
    "max_randomness": max_randomness_args,
    "deterministic": deterministic_args,
    "default": default_args,
}
