"""
Problem generator for Mode-Must-Exist malrule.

Generates data sets where no value repeats (no mode exists), testing
whether students understand that not all data sets have a mode.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Tuple, Optional, List
from utils import ProblemGenerator, Problem, DifficultyLevel


class ModeMustExistProblemGenerator(ProblemGenerator):
    """
    Generates statistics problems to elicit Mode-Must-Exist malrule.

    Creates data sets with no repeating values to test whether students
    recognize that a mode doesn't always exist, or if they force one
    by picking largest, smallest, or middle value.
    """

    def get_name(self) -> str:
        return "Mode-Must-Exist Problem Generator"

    def get_description(self) -> str:
        return (
            "Generates data sets with no repeating values (no mode exists). "
            "Tests whether students understand that not all data sets have a mode, "
            "or if they incorrectly identify the largest, smallest, or middle value as the mode."
        )

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        """Get appropriate value ranges based on level and difficulty."""
        ranges = {
            6: {
                DifficultyLevel.EASY: (1, 20),       # Simple numbers 1-20
                DifficultyLevel.MEDIUM: (1, 50),
                DifficultyLevel.HARD: (1, 100),
            },
            7: {
                DifficultyLevel.EASY: (1, 50),
                DifficultyLevel.MEDIUM: (1, 100),
                DifficultyLevel.HARD: (1, 200),
            },
            8: {
                DifficultyLevel.EASY: (1, 100),
                DifficultyLevel.MEDIUM: (1, 200),
                DifficultyLevel.HARD: (1, 500),
            },
        }

        lvl = self.level if self.level in ranges else 6
        return {'values': ranges[lvl][self.difficulty]}

    def _generate_unique_values(self, count: int, min_val: int, max_val: int, seed: Optional[int] = None) -> List[int]:
        """
        Generate a list of unique values (no repeats).

        Args:
            count: Number of values to generate
            min_val: Minimum value
            max_val: Maximum value
            seed: Random seed for reproducibility

        Returns:
            List of unique integers
        """
        if seed is not None:
            random.seed(seed)

        # Ensure we have enough range to generate unique values
        range_size = max_val - min_val + 1
        if count > range_size:
            count = range_size

        # Generate unique values
        values = random.sample(range(min_val, max_val + 1), count)

        # Shuffle to randomize order
        random.shuffle(values)

        return values

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        return [
            'basic_no_mode',
            'larger_no_mode',
            'small_no_mode',
            'has_mode_control',
            'comparison_problem',
            'word_problem_context'  # NEW: Covers all formula types with variants
        ]

    def generate(self, seed: Optional[int] = None, template: Optional[str] = None) -> Problem:
        """
        Generate a statistics problem testing mode understanding.

        Args:
            seed: Optional random seed for reproducibility
            template: Specific template to use, or None for random selection

        Returns:
            Problem instance
        """
        if seed is not None:
            random.seed(seed)

        # Select template
        if template is None:
            # For random generation, exclude control templates where malrule might be correct
            # Only select from templates where malrule is definitely wrong (no mode exists)
            malrule_templates = ['basic_no_mode', 'larger_no_mode', 'small_no_mode']
            template = random.choice(malrule_templates)

        # Generate based on template
        if template == 'basic_no_mode':
            return self._generate_basic_no_mode(seed)
        elif template == 'larger_no_mode':
            return self._generate_larger_no_mode(seed)
        elif template == 'small_no_mode':
            return self._generate_small_no_mode(seed)
        elif template == 'has_mode_control':
            return self._generate_has_mode_control(seed)
        elif template == 'comparison_problem':
            return self._generate_comparison_problem(seed)
        elif template == 'word_problem_context':
            return self._generate_word_problem_context(seed)
        else:
            raise ValueError(f"Unknown template: {template}")

    def _generate_basic_no_mode(self, seed: Optional[int] = None) -> Problem:
        """
        Template 1: Basic dataset with no mode (5-7 values, all unique).

        Tests the fundamental case where students incorrectly identify a mode
        when all values appear only once.

        Args:
            seed: Optional random seed for reproducibility

        Returns:
            Problem with all unique values
        """
        if seed is not None:
            random.seed(seed)

        min_val, max_val = self.get_value_ranges()['values']

        # Medium-sized dataset (5-7 values)
        dataset_size = random.randint(5, 7)

        # Generate unique values (no repeats = no mode)
        data = self._generate_unique_values(dataset_size, min_val, max_val, seed)

        # Choose question format
        question_formats = [
            "What is the mode of the data set: {data}?",
            "Find the mode of: {data}",
            "Identify the mode for the following data set: {data}",
        ]

        question_format = random.choice(question_formats)
        problem_text = question_format.format(data=data)

        # Malrule will pick largest, smallest, or middle
        # We'll use largest for consistency in testing
        malrule_answer = str(max(data))
        correct_answer = "No mode"

        return Problem(
            text=problem_text,
            operands=data,
            operation='mode',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'data': data,
                'has_mode': False,
                'all_unique': True,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'template': 'basic_no_mode'
            }
        )

    def _generate_larger_no_mode(self, seed: Optional[int] = None) -> Problem:
        """
        Template 2: Larger dataset with no mode (8-12 values, all unique).

        Tests with more data points to see if students maintain the misconception
        even with larger datasets.

        Args:
            seed: Optional random seed for reproducibility

        Returns:
            Problem with larger dataset, all unique values
        """
        if seed is not None:
            random.seed(seed)

        min_val, max_val = self.get_value_ranges()['values']

        # Larger dataset (8-12 values)
        dataset_size = random.randint(8, 12)

        # Generate unique values
        data = self._generate_unique_values(dataset_size, min_val, max_val, seed)

        problem_text = f"What is the mode of the data set: {data}?"

        # Malrule picks largest
        malrule_answer = str(max(data))
        correct_answer = "No mode"

        return Problem(
            text=problem_text,
            operands=data,
            operation='mode',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'data': data,
                'has_mode': False,
                'all_unique': True,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'template': 'larger_no_mode'
            }
        )

    def _generate_small_no_mode(self, seed: Optional[int] = None) -> Problem:
        """
        Template 3: Small dataset with no mode (3-4 values, all unique).

        Tests minimal case where students might feel especially compelled to
        pick a mode because "such a small dataset must have one".

        Args:
            seed: Optional random seed for reproducibility

        Returns:
            Problem with small dataset, all unique values
        """
        if seed is not None:
            random.seed(seed)

        min_val, max_val = self.get_value_ranges()['values']

        # Small dataset (3-4 values)
        dataset_size = random.randint(3, 4)

        # Generate unique values
        data = self._generate_unique_values(dataset_size, min_val, max_val, seed)

        problem_text = f"Find the mode of: {data}"

        # Malrule picks largest
        malrule_answer = str(max(data))
        correct_answer = "No mode"

        return Problem(
            text=problem_text,
            operands=data,
            operation='mode',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'data': data,
                'has_mode': False,
                'all_unique': True,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'template': 'small_no_mode'
            }
        )

    def _generate_has_mode_control(self, seed: Optional[int] = None) -> Problem:
        """
        Template 4: Dataset WITH a clear mode (control case).

        This is a control template where a mode DOES exist. The malrule student
        would correctly identify it (though possibly for wrong reasons). This
        shows that the algorithms can handle both cases.

        Args:
            seed: Optional random seed for reproducibility

        Returns:
            Problem with a clear mode
        """
        if seed is not None:
            random.seed(seed)

        min_val, max_val = self.get_value_ranges()['values']

        # Create a dataset with one value appearing more frequently
        # Start with 3-5 unique values
        base_size = random.randint(3, 5)
        base_values = self._generate_unique_values(base_size, min_val, max_val, seed)

        # Pick one value to be the mode (appears multiple times)
        mode_value = random.choice(base_values)
        mode_frequency = random.randint(2, 3)  # Appears 2-3 times

        # Build dataset: mode appears multiple times, others appear once
        data = [mode_value] * mode_frequency
        for val in base_values:
            if val != mode_value:
                data.append(val)

        # Shuffle to randomize order
        random.shuffle(data)

        problem_text = f"Identify the mode for the following data set: {data}"

        # Both correct and malrule would identify the actual mode
        malrule_answer = str(mode_value)
        correct_answer = str(mode_value)

        return Problem(
            text=problem_text,
            operands=data,
            operation='mode',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'data': data,
                'has_mode': True,
                'all_unique': False,
                'mode_value': mode_value,
                'mode_frequency': mode_frequency,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'template': 'has_mode_control'
            }
        )

    def _generate_comparison_problem(self, seed: Optional[int] = None) -> Problem:
        """
        Template 5: Compare two datasets (one with mode, one without).

        Asks students to identify which dataset has a mode, or to compare
        the modes of two datasets where one has a mode and one doesn't.

        Args:
            seed: Optional random seed for reproducibility

        Returns:
            Problem comparing two datasets
        """
        if seed is not None:
            random.seed(seed)

        min_val, max_val = self.get_value_ranges()['values']

        # Dataset A: Has a mode
        base_size_a = random.randint(3, 4)
        base_values_a = self._generate_unique_values(base_size_a, min_val, max_val // 2, seed)
        mode_value_a = random.choice(base_values_a)
        data_a = [mode_value_a] * 2
        for val in base_values_a:
            if val != mode_value_a:
                data_a.append(val)
        random.shuffle(data_a)

        # Dataset B: No mode (all unique)
        dataset_size_b = random.randint(4, 6)
        data_b = self._generate_unique_values(dataset_size_b, max_val // 2 + 1, max_val, seed)

        problem_text = f"Dataset A: {data_a}, Dataset B: {data_b}. Which dataset has a mode?"

        # Correct: Dataset A has mode, Dataset B has no mode
        correct_answer = f"Dataset A has mode ({mode_value_a}), Dataset B has no mode"

        # Malrule: Both datasets have modes (picks largest for Dataset B)
        malrule_answer = f"Dataset A has mode ({mode_value_a}), Dataset B has mode ({max(data_b)})"

        return Problem(
            text=problem_text,
            operands=data_a + data_b,
            operation='mode',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'data_a': data_a,
                'data_b': data_b,
                'mode_a': mode_value_a,
                'has_mode_a': True,
                'has_mode_b': False,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'template': 'comparison_problem'
            }
        )

    def _generate_word_problem_context(self, seed: Optional[int] = None) -> Problem:
        """
        Template 6: Word problem covering ALL formula types with 3 variants each.

        This template embeds mode-finding scenarios in real-world contexts.
        Formula types covered:
        1. find_mode_no_mode: All unique values (no mode exists)
        2. find_mode_single_mode: One value appears most frequently
        3. find_mode_bimodal: Two values tied for most frequent
        """
        if seed is not None:
            random.seed(seed)

        # Select which formula type to embed
        formula_types = ['find_mode_no_mode', 'find_mode_single_mode', 'find_mode_bimodal']
        formula_type = random.choice(formula_types)
        variant = random.randint(0, 2)  # 3 variants per formula type

        min_val, max_val = self.get_value_ranges()['values']

        if formula_type == 'find_mode_no_mode':
            # Generate dataset with no mode (all unique values)
            dataset_size = random.randint(5, 7)
            data = self._generate_unique_values(dataset_size, min_val, max_val, seed)

            # 3 different word problem contexts
            templates = [
                (
                    f"Ms. Johnson recorded the number of books read by each student in her class during summer: "
                    f"{', '.join([f'Student {i+1} read {data[i]} books' for i in range(len(data))])}. "
                    f"What is the mode of the number of books read?",
                    "books read"
                ),
                (
                    f"A survey asked people how many pets they own. The responses were: {data}. "
                    f"What is the mode of the number of pets?",
                    "pets owned"
                ),
                (
                    f"The coach recorded practice times (in minutes) for each team member: {data}. "
                    f"What is the mode of the practice times?",
                    "practice times"
                )
            ]

            problem_text, context = templates[variant]
            correct_answer = "No mode"
            malrule_answer = str(max(data))  # Malrule picks largest

            return Problem(
                text=problem_text,
                operands=data,
                operation='mode',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'data': data,
                    'has_mode': False,
                    'all_unique': True,
                    'correct_answer': correct_answer,
                    'malrule_answer': malrule_answer,
                    'template': 'word_problem_context',
                    'is_word_problem': True,
                    'word_problem_type': formula_type,
                    'word_problem_variant': variant,
                    'context': context
                }
            )

        elif formula_type == 'find_mode_single_mode':
            # Generate dataset with one clear mode
            base_size = random.randint(3, 5)
            base_values = self._generate_unique_values(base_size, min_val, max_val, seed)

            # Pick one value to be the mode (appears multiple times)
            mode_value = random.choice(base_values)
            mode_frequency = random.randint(2, 3)  # Appears 2-3 times

            # Build dataset: mode appears multiple times, others appear once
            data = [mode_value] * mode_frequency
            for val in base_values:
                if val != mode_value:
                    data.append(val)

            # Shuffle to randomize order
            random.shuffle(data)

            # 3 different word problem contexts
            templates = [
                (
                    f"A teacher recorded the shoe sizes of students in the class: {data}. "
                    f"What is the mode of the shoe sizes?",
                    "shoe sizes"
                ),
                (
                    f"Daily high temperatures (in °F) for the past week were: {data}. "
                    f"What is the mode temperature?",
                    "temperatures"
                ),
                (
                    f"Students scored the following points in a game: {data}. "
                    f"What is the mode of the scores?",
                    "game scores"
                )
            ]

            problem_text, context = templates[variant]
            correct_answer = str(mode_value)
            malrule_answer = str(mode_value)  # Happens to be correct

            return Problem(
                text=problem_text,
                operands=data,
                operation='mode',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'data': data,
                    'has_mode': True,
                    'all_unique': False,
                    'mode_value': mode_value,
                    'mode_frequency': mode_frequency,
                    'correct_answer': correct_answer,
                    'malrule_answer': malrule_answer,
                    'template': 'word_problem_context',
                    'is_word_problem': True,
                    'word_problem_type': formula_type,
                    'word_problem_variant': variant,
                    'context': context
                }
            )

        elif formula_type == 'find_mode_bimodal':
            # Generate dataset with two modes (bimodal)
            # Create two values that appear with equal frequency (2 times each)
            mode_val1 = random.randint(min_val, max_val)
            mode_val2 = random.randint(min_val, max_val)
            while mode_val2 == mode_val1:
                mode_val2 = random.randint(min_val, max_val)

            # Add 1-2 unique values
            num_unique = random.randint(1, 2)
            unique_values = self._generate_unique_values(num_unique, min_val, max_val, seed)
            # Ensure unique values don't conflict with modes
            unique_values = [v for v in unique_values if v not in [mode_val1, mode_val2]][:num_unique]

            # Build dataset: both modes appear twice, others once
            data = [mode_val1, mode_val1, mode_val2, mode_val2] + unique_values
            random.shuffle(data)

            # 3 different word problem contexts
            templates = [
                (
                    f"Students were asked how many siblings they have. The responses were: {data}. "
                    f"What is the mode of the number of siblings?",
                    "number of siblings"
                ),
                (
                    f"A librarian counted the number of books borrowed by each patron: {data}. "
                    f"What is the mode?",
                    "books borrowed"
                ),
                (
                    f"The number of goals scored by each player in a tournament: {data}. "
                    f"Find the mode of goals scored.",
                    "goals scored"
                )
            ]

            problem_text, context = templates[variant]
            modes = sorted([mode_val1, mode_val2])
            correct_answer = f"{modes}"  # Bimodal answer
            malrule_answer = str(max(modes))  # Malrule picks one (largest)

            return Problem(
                text=problem_text,
                operands=data,
                operation='mode',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'data': data,
                    'has_mode': True,
                    'bimodal': True,
                    'mode_values': modes,
                    'correct_answer': correct_answer,
                    'malrule_answer': malrule_answer,
                    'template': 'word_problem_context',
                    'is_word_problem': True,
                    'word_problem_type': formula_type,
                    'word_problem_variant': variant,
                    'context': context
                }
            )
