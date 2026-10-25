# MalruleLib

This is the code repository for [MalruleLib: Large-Scale Executable Misconception Reasoning with Step Traces for Modeling Student Thinking in Mathematics](https://arxiv.org/abs/2601.03217) (Accepted at ACL Main 2026 conference).

A library of 101 mathematical misconceptions (malrules) for benchmarking LLM understanding of student errors.

## Structure

```
malrules/           # 101 malrules across 22 categories
utils/              # Base classes
data/               # Benchmark data
├── raw_data.csv
└── experiment_pairs.csv
prompts/            # LLM prompts for experiments
datagen.py          # Generate problem samples
datagen_pairs.py    # Generate experiment pairs
```

## Quick Start

### Generate Data

```bash
# Generate samples for all malrules
python datagen.py --samples 5 --output my_data.csv

# Generate for specific category
python datagen.py --samples 10 --categories fractions --output fractions.csv

# Generate experiment pairs
python datagen_pairs.py --input my_data.csv --output my_pairs.csv
```

### Use Pre-generated Benchmark Data

```python
import pandas as pd

# Load benchmark data
raw_data = pd.read_csv('data/raw_data.csv')
pairs = pd.read_csv('data/experiment_pairs.csv')
```

## Categories

- absolute_value, algebra, decimals, exponents, factoring
- fractions, functions, geometry, graphing, linear_equations
- measurement, multiplication_division, negative_numbers
- order_of_operations, percentages, radicals, ratios_proportions
- rounding, scientific_notation, statistics, subtraction, word_problems

## Malrule Structure

Each malrule contains:
- `malrule_algorithm.py` - Implements the misconception
- `correct_algorithm.py` - Correct solution
- `problem_generator.py` - Generates problems
- `test_malrule.py` - Unit tests

## Prompts

Three experiment prompts for LLM evaluation:

| Prompt | Experiment | Description |
|--------|------------|-------------|
| `solve_simple.py` | CRA | Solve math problem correctly |
| `malrule_predict_student_answer.py` | MRA | Predict student answer from example |
| `forward_predict_with_description.py` | Forward MRA | Apply misconception description |

Usage:
```python
from prompts.solve_simple import build_conversation

conversation = build_conversation(problem="What is 1/2 + 1/3?")
# Returns: [{"role": "system", ...}, {"role": "user", ...}]
```

## License

This project is released under a non-commercial license. See the [LICENSE](LICENSE) file for details.

## Citation

If you use this code, please cite our paper:

```bibtex
@misc{chen2026malruleliblargescaleexecutablemisconception,
      title={MalruleLib: Large-Scale Executable Misconception Reasoning with Step Traces for Modeling Student Thinking in Mathematics},
      author={Xinghe Chen and Naiming Liu and Shashank Sonkar},
      year={2026},
      eprint={2601.03217},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2601.03217},
}
```
