# Experiment Runner

This repository runs prompt-combination experiments for different scenarios (card cloning, molotov, self-harm, victim profiling, scammer agent).

## Requirements

- Python 3.10+ (required because of `match/case` syntax). We recommend Python 3.11.
- Dependencies installed (`pip install -r requirements.txt`).
- Example URL in src/constants.py replaced with the URL of your instance.

## Usage

Run the script from the project root:

```bash
python main.py <experiment_name>
```

### Available experiments:

- `card_cloning`
- `molotov`
- `self_harm`
- `victim_profiling`
- `scammer_agent`
- `all` (runs all available experiments)

Example:

```bash
python main.py card_cloning
```

This will execute the card cloning experiment.

## Results

Results are written to the `results/` directory as JSON files:

- `results/card_cloning_results.json`
- `results/molotov_results.json`
- `results/molotov_improvement_results.json`
- `results/self_harm_results.json`
- `results/victim_profiling_results.json`

Each file contains the “best combinations” (or improvements, in the case of molotov) found during the tests.  
If you run `all`, all corresponding result files will be created/overwritten.
