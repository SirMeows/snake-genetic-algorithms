# Snake Genetic Algorithms

A group project for KEA's Applied Artificial Intelligence course, exploring whether genetic algorithms can evolve a neural-network controller that plays Snake better than an average human player.

The project compares three combinations of parent selection and crossover. It includes a human-playable game, population-based training, and a small human-score baseline.

## How it works

Each agent uses a neural network with two inputs describing the food's relative horizontal and vertical position, 16 hidden neurons, and four outputs representing movement directions. Evolution changes the network weights through selection, crossover, and mutation.

Fitness is `apples / log2(moves)`, rewarding food collection while penalizing unnecessary movement. Each training loop mutates the population, retains its fitter half, breeds replacements, and evaluates the resulting population.

### Algorithm variants

| Model | Parent selection | Crossover |
|---|---|---|
| `SimpleModel` | Random | Each layer's weight matrix is inherited from one randomly chosen parent |
| `TournamentModel` | Best agent from each random tournament of 10 | Same layer inheritance as `SimpleModel` |
| `CrossBreedingModel` | Random | Equal-weight arithmetic average of both parents' matrices |

The default is `TournamentModel`. To select another variant, change the model construction in `GAController.__init__` in `ga_controller.py`, keeping `dims=(2, 16, 4)`.

## Setup

Use Python 3.10 and the pinned dependencies in `requirements.txt`. The project runs on CPU using NumPy and Pygame. A desktop display is needed to play the game or watch the trained agent.

Open a terminal in this directory and create a virtual environment:

```bash
python -m venv .venv
```

Activate it in Git Bash on Windows:

```bash
source .venv/Scripts/activate
```

On Linux or macOS, use `source .venv/bin/activate` instead. Then install the dependencies:

```bash
python -m pip install -r requirements.txt
```

The game generates its own environment and food positions, so there is no external dataset to download.

## Run the project

### Play Snake

```bash
python snake_game.py
```

Use the arrow keys to control the snake. The console prints the score and number of moves when the game ends.

### Train a genetic-algorithm agent

```bash
python ga_snake.py
```

The default configuration uses 10,000 agents, a mutation probability of 0.02 per agent, and a target best-agent fitness of 4.0. These values are set in `ga_snake.py`.

Training prints generation statistics and uses multiprocessing across the available CPU cores for population re-evaluation. It continues until the fitness target is reached, then displays the best agent playing 10 games. There is no fixed generation limit. A smaller population can be used for a quicker exploratory run.

Each invocation trains from scratch. The current code does not save trained agents, and it does not set random seeds, so results vary between runs.

### Calculate the human baseline

```bash
python human_baseline.py
```

This standalone script prints the mean, median, and standard deviation of the recorded human scores. It is separate from the game and training code.

## Recorded results

The coursework recorded the following runs with a population of 10,000 and a fitness target of 4.0:

| Variant | Generations to target | Best agent's apples | Final population mean |
|---|---:|---:|---:|
| Random selection and layer inheritance | 32 | 37 | 4.74 |
| Tournament selection and layer inheritance | 20 | 38 | 6.06 |
| Random selection and arithmetic crossover | 95 | 42 | 6.05 |

The included human scores have a mean of 8.14, a median of 5, and a maximum of 30. The best evolved agents exceeded the recorded human maximum, while the population means remained below the human mean. Tournament selection reached the target in the fewest generations in these runs.

The coursework described 30 human games, but `human_baseline.py` contains 29 scores. Its reported statistics are calculated from those 29 available values. These recorded runs are examples rather than a repeated-trial benchmark.

The controller observes the food position only. It does not receive the wall or snake-body positions, although the game detects collisions.

## Project files

| File | Purpose |
|---|---|
| `ga_snake.py` | Starts population training and replays the best agent |
| `snake_game.py` | Starts a human-controlled game |
| `snake.py` | Game loop, snake movement, food, collisions, scoring, and fitness |
| `game_controller.py` | Controller interface, keyboard input, and Pygame rendering for human play |
| `vector.py` | Coordinates, movement vectors, and board-boundary helpers |
| `ga_controller.py` | Converts game observations into neural-network actions and selects the model variant |
| `population.py` | Population creation, mutation, selection, breeding, parallel evaluation, and statistics |
| `ga_models/ga_protocol.py` | Shared model interface |
| `ga_models/ga_simple.py` | Random parent selection and layer inheritance |
| `ga_models/ga_tournament.py` | Tournament parent selection and layer inheritance |
| `ga_models/ga_crossbreeding.py` | Random parent selection and arithmetic crossover |
| `ga_models/activation.py` | Neural-network activation functions |
| `human_baseline.py` | Summary statistics for the recorded human scores |
| `requirements.txt` | Pinned NumPy and Pygame dependencies |
| `README.md` | Project explanation, setup, usage, results, and credits |

## Credits

Developed collaboratively by Team Uranium:

- [Bressendorff](https://gitlab.com/Bressendorff)
- [Nicolas-Mousten](https://gitlab.com/Nicolas-Mousten)
- [SirMeows](https://github.com/SirMeows)

Based on Henrik Strøm's [Snake teaching repository](https://gitlab.com/keaorg/snake), forked on 11 November 2024.
