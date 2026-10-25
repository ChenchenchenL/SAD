"""
Problem generator for Ignore-Outliers-Effect malrule.

Generates data sets with clear outliers (extreme values) to test whether
students recognize how outliers affect the mean and make it less representative
of typical values.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Tuple, Optional, List
from utils import ProblemGenerator, Problem, DifficultyLevel


class IgnoreOutliersEffectProblemGenerator(ProblemGenerator):
    """
    Generates statistics problems to elicit Ignore-Outliers-Effect malrule.

    Creates data sets with clear outliers (extreme values far from typical values)
    to test whether students recognize that:
    1. Outliers pull the mean away from typical values
    2. The mean is NOT representative when outliers are present
    3. The median is more appropriate for skewed data
    """

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        return [
            'basic_outlier',
            'word_problem_context',
            'multiple_outliers',
            'symmetric_no_outlier',
            'comparison_problem',
            'word_problem_expanded'  # NEW: Covers all formula types with variants
        ]

    def get_name(self) -> str:
        return "Ignore-Outliers-Effect Problem Generator"

    def get_description(self) -> str:
        return (
            "Generates data sets with clear outliers (extreme values). "
            "Tests whether students recognize that outliers pull the mean away "
            "from typical values, making it less representative. Students who "
            "ignore outliers say 'yes, mean is representative' when the correct "
            "answer is 'no, median is better.'"
        )

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        """Get appropriate value ranges based on level and difficulty."""
        ranges = {
            6: {
                DifficultyLevel.EASY: (3, 10),       # Simple numbers 3-10 for typical values
                DifficultyLevel.MEDIUM: (5, 15),
                DifficultyLevel.HARD: (5, 20),
            },
            7: {
                DifficultyLevel.EASY: (5, 15),
                DifficultyLevel.MEDIUM: (10, 25),
                DifficultyLevel.HARD: (10, 30),
            },
            8: {
                DifficultyLevel.EASY: (10, 30),
                DifficultyLevel.MEDIUM: (20, 50),
                DifficultyLevel.HARD: (20, 75),
            },
            9: {
                DifficultyLevel.EASY: (10, 40),
                DifficultyLevel.MEDIUM: (25, 75),
                DifficultyLevel.HARD: (30, 100),
            },
            10: {
                DifficultyLevel.EASY: (15, 50),
                DifficultyLevel.MEDIUM: (30, 100),
                DifficultyLevel.HARD: (40, 150),
            },
        }

        lvl = self.level if self.level in ranges else 6
        return {'typical_values': ranges[lvl][self.difficulty]}

    def _generate_dataset_with_outlier(
        self,
        num_typical: int,
        min_typical: int,
        max_typical: int,
        outlier_direction: str,
        seed: Optional[int] = None
    ) -> Tuple[List[int], int]:
        """
        Generate a dataset with typical values and one clear outlier.

        Args:
            num_typical: Number of typical values (clustered together)
            min_typical: Minimum typical value
            max_typical: Maximum typical value
            outlier_direction: 'high' or 'low' - direction of outlier
            seed: Random seed for reproducibility

        Returns:
            Tuple of (dataset, outlier_value)
        """
        if seed is not None:
            random.seed(seed)

        # Generate clustered typical values (with some repeats for clustering)
        typical_values = []
        for _ in range(num_typical):
            typical_values.append(random.randint(min_typical, max_typical))

        # Create a clear outlier (significantly different from typical values)
        if outlier_direction == 'high':
            # High outlier: 3-6x the maximum typical value
            multiplier = random.uniform(3.5, 6.0)
            outlier = int(max_typical * multiplier)
        else:  # 'low'
            # Low outlier: near zero or negative (much less than min typical)
            if min_typical > 10:
                outlier = random.randint(0, min_typical // 4)
            else:
                outlier = random.randint(0, max(1, min_typical // 3))

        # Combine and shuffle
        dataset = typical_values + [outlier]
        random.shuffle(dataset)

        return dataset, outlier

    def generate(self, seed: Optional[int] = None, template: Optional[str] = None) -> Problem:
        """
        Generate a statistics problem with outliers.

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
            template = random.choice(self.get_available_templates())

        # Generate based on template
        if template == 'basic_outlier':
            return self._generate_basic_outlier(seed)
        elif template == 'word_problem_context':
            return self._generate_word_problem_context(seed)
        elif template == 'multiple_outliers':
            return self._generate_multiple_outliers(seed)
        elif template == 'symmetric_no_outlier':
            return self._generate_symmetric_no_outlier(seed)
        elif template == 'comparison_problem':
            return self._generate_comparison_problem(seed)
        elif template == 'word_problem_expanded':
            return self._generate_word_problem_expanded(seed)
        else:
            raise ValueError(f"Unknown template: {template}")

    def _generate_basic_outlier(self, seed: Optional[int] = None) -> Problem:
        """Template 1: Simple dataset with one clear outlier."""
        if seed is not None:
            random.seed(seed)

        min_typical, max_typical = self.get_value_ranges()['typical_values']

        # Determine dataset size based on difficulty
        if self.difficulty == DifficultyLevel.EASY:
            num_typical = random.randint(4, 6)  # Smaller datasets for easier visualization
        elif self.difficulty == DifficultyLevel.MEDIUM:
            num_typical = random.randint(6, 9)
        else:  # HARD
            num_typical = random.randint(8, 12)

        # Randomly choose outlier direction (high is more common in real data)
        outlier_direction = random.choices(['high', 'low'], weights=[0.7, 0.3])[0]

        # Generate dataset with outlier
        dataset, outlier = self._generate_dataset_with_outlier(
            num_typical, min_typical, max_typical, outlier_direction, seed
        )

        # Calculate mean and median for metadata
        mean = sum(dataset) / len(dataset)
        sorted_data = sorted(dataset)
        n = len(sorted_data)
        if n % 2 == 0:
            median = (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2
        else:
            median = sorted_data[n // 2]

        # Correct answer: No, mean is not representative
        correct_answer = "No, mean is not representative"

        # Malrule answer: Yes, mean is representative (ignores outlier)
        malrule_answer = "Yes, mean is representative"

        # Choose question format
        question_formats = [
            "Is the mean representative of this data set: {data}?",
            "Does the mean accurately represent the typical value in {data}?",
            "Is the mean a good measure of center for the data set {data}?",
            "Would you use the mean to describe the typical value in {data}? Why or why not?",
            "Is the mean the best measure of central tendency for {data}? Explain.",
        ]

        question_format = random.choice(question_formats)
        problem_text = question_format.format(data=sorted(dataset))

        return Problem(
            text=problem_text,
            operands=dataset,
            operation='representativeness',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'data': dataset,
                'outlier': outlier,
                'outlier_direction': outlier_direction,
                'mean': mean,
                'median': median,
                'has_outlier': True,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'template': 'basic_outlier'
            }
        )

    def _generate_word_problem_context(self, seed: Optional[int] = None) -> Problem:
        """Template 2: Word problem with real-world context."""
        problem = self._generate_basic_outlier(seed)

        contexts = [
            ("salaries", "A company has employees with salaries (in thousands): {data}. Is the mean salary representative of a typical employee's salary?", "thousand dollars"),
            ("test_scores", "Students scored the following on a test: {data}. Is the mean score representative of typical performance?", "points"),
            ("house_prices", "Houses in a neighborhood sold for (in thousands): {data}. Is the mean price representative of a typical house?", "thousand dollars"),
            ("ages", "A group has ages: {data}. Is the mean age representative of the typical age?", "years"),
            ("commute_times", "Commute times in minutes: {data}. Is the mean commute time representative?", "minutes"),
        ]

        context_type, question_template, unit = random.choice(contexts)
        data = problem.metadata['data']
        problem.text = question_template.format(data=sorted(data))
        problem.metadata['template'] = 'word_problem_context'
        problem.metadata['context'] = context_type
        problem.metadata['unit'] = unit
        return problem

    def _generate_multiple_outliers(self, seed: Optional[int] = None) -> Problem:
        """Template 3: Dataset with multiple outliers."""
        if seed is not None:
            random.seed(seed)

        min_typical, max_typical = self.get_value_ranges()['typical_values']

        # Determine dataset size (larger for multiple outliers)
        if self.difficulty == DifficultyLevel.EASY:
            num_typical = random.randint(5, 7)
            num_outliers = 2
        elif self.difficulty == DifficultyLevel.MEDIUM:
            num_typical = random.randint(7, 10)
            num_outliers = random.randint(2, 3)
        else:  # HARD
            num_typical = random.randint(10, 14)
            num_outliers = random.randint(2, 4)

        # Generate typical values
        typical_values = []
        for _ in range(num_typical):
            typical_values.append(random.randint(min_typical, max_typical))

        # Generate multiple outliers (both high and low)
        outliers = []
        for i in range(num_outliers):
            if i % 2 == 0:  # High outlier
                multiplier = random.uniform(3.5, 6.0)
                outlier = int(max_typical * multiplier)
            else:  # Low outlier
                if min_typical > 10:
                    outlier = random.randint(0, min_typical // 4)
                else:
                    outlier = random.randint(0, max(1, min_typical // 3))
            outliers.append(outlier)

        # Combine and shuffle
        dataset = typical_values + outliers
        random.shuffle(dataset)

        # Calculate mean and median
        mean = sum(dataset) / len(dataset)
        sorted_data = sorted(dataset)
        n = len(sorted_data)
        if n % 2 == 0:
            median = (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2
        else:
            median = sorted_data[n // 2]

        # Correct answer: No, mean is not representative
        correct_answer = "No, mean is not representative"

        # Malrule answer: Yes, mean is representative (ignores outliers)
        malrule_answer = "Yes, mean is representative"

        problem_text = f"The data set {sorted(dataset)} has multiple extreme values. Is the mean representative of the typical values?"

        return Problem(
            text=problem_text,
            operands=dataset,
            operation='representativeness',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'data': dataset,
                'outlier': outliers,  # List of outliers
                'outlier_direction': 'both',
                'mean': mean,
                'median': median,
                'has_outlier': True,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'template': 'multiple_outliers'
            }
        )

    def _generate_symmetric_no_outlier(self, seed: Optional[int] = None) -> Problem:
        """Template 4: Control case - symmetric dataset with NO outliers."""
        if seed is not None:
            random.seed(seed)

        min_typical, max_typical = self.get_value_ranges()['typical_values']

        # Generate symmetric dataset (centered around a mean value)
        if self.difficulty == DifficultyLevel.EASY:
            num_values = random.randint(5, 7)
        elif self.difficulty == DifficultyLevel.MEDIUM:
            num_values = random.randint(7, 10)
        else:  # HARD
            num_values = random.randint(10, 14)

        # Pick a center value
        center = (min_typical + max_typical) // 2
        spread = (max_typical - min_typical) // 4  # Moderate spread

        # Generate values clustered around center
        dataset = []
        for _ in range(num_values):
            value = random.randint(center - spread, center + spread)
            dataset.append(value)

        # Calculate mean and median
        mean = sum(dataset) / len(dataset)
        sorted_data = sorted(dataset)
        n = len(sorted_data)
        if n % 2 == 0:
            median = (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2
        else:
            median = sorted_data[n // 2]

        # Correct answer: YES, mean IS representative (no outliers)
        correct_answer = "Yes, mean is representative"

        # Malrule answer: Also yes (happens to be correct, but for wrong reason - no checking)
        malrule_answer = "Yes, mean is representative"

        problem_text = f"Is the mean representative of this data set: {sorted(dataset)}?"

        return Problem(
            text=problem_text,
            operands=dataset,
            operation='representativeness',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'data': dataset,
                'outlier': None,
                'outlier_direction': 'none',
                'mean': mean,
                'median': median,
                'has_outlier': False,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'template': 'symmetric_no_outlier'
            }
        )

    def _generate_comparison_problem(self, seed: Optional[int] = None) -> Problem:
        """Template 5: Compare two datasets - one with outlier, one without."""
        if seed is not None:
            random.seed(seed)

        min_typical, max_typical = self.get_value_ranges()['typical_values']

        # Generate two datasets
        # Dataset 1: With outlier
        num_typical1 = random.randint(4, 6)
        typical_values1 = [random.randint(min_typical, max_typical) for _ in range(num_typical1)]
        multiplier = random.uniform(3.5, 6.0)
        outlier1 = int(max_typical * multiplier)
        dataset1 = typical_values1 + [outlier1]
        random.shuffle(dataset1)
        mean1 = sum(dataset1) / len(dataset1)
        sorted_data1 = sorted(dataset1)
        n1 = len(sorted_data1)
        if n1 % 2 == 0:
            median1 = (sorted_data1[n1 // 2 - 1] + sorted_data1[n1 // 2]) / 2
        else:
            median1 = sorted_data1[n1 // 2]

        # Dataset 2: No outlier (symmetric)
        num_values2 = random.randint(4, 6)
        center = (min_typical + max_typical) // 2
        spread = (max_typical - min_typical) // 4
        dataset2 = [random.randint(center - spread, center + spread) for _ in range(num_values2)]
        mean2 = sum(dataset2) / len(dataset2)
        sorted_data2 = sorted(dataset2)
        n2 = len(sorted_data2)
        if n2 % 2 == 0:
            median2 = (sorted_data2[n2 // 2 - 1] + sorted_data2[n2 // 2]) / 2
        else:
            median2 = sorted_data2[n2 // 2]

        # Correct answer: Dataset 2 (no outlier, mean is representative)
        correct_answer = "Dataset B has a more representative mean"

        # Malrule answer: Student doesn't check for outliers, might say both are representative
        # or compare the means directly without considering representativeness
        malrule_answer = "Both means are equally representative"

        problem_text = f"Dataset A: {sorted(dataset1)}. Dataset B: {sorted(dataset2)}. Which dataset has a mean that better represents its typical values?"

        return Problem(
            text=problem_text,
            operands=dataset1 + dataset2,
            operation='representativeness',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'data': dataset1,
                'data1': dataset1,
                'data2': dataset2,
                'outlier': outlier1,
                'outlier_direction': 'high',
                'mean': mean1,
                'median': median1,
                'mean1': mean1,
                'median1': median1,
                'mean2': mean2,
                'median2': median2,
                'has_outlier': True,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'template': 'comparison_problem'
            }
        )

    def _generate_word_problem_expanded(self, seed: Optional[int] = None) -> Problem:
        """
        Template 6: Word problem covering ALL formula types with 3 variants each.

        Formula types covered:
        1. evaluate_mean_representativeness: Determine if mean is representative when outliers present
        2. choose_appropriate_measure: Select mean vs median for dataset with outliers
        3. identify_outlier_effect: Recognize how outliers affect mean calculation
        """
        if seed is not None:
            random.seed(seed)

        # Select which formula type to embed
        formula_types = ['evaluate_mean_representativeness', 'choose_appropriate_measure', 'identify_outlier_effect']
        formula_type = random.choice(formula_types)
        variant = random.randint(0, 2)  # 3 variants per formula type

        min_typical, max_typical = self.get_value_ranges()['typical_values']

        if formula_type == 'evaluate_mean_representativeness':
            # Generate dataset with clear outlier
            num_typical = random.randint(5, 7)
            typical_values = [random.randint(min_typical, max_typical) for _ in range(num_typical)]

            # Add high outlier
            multiplier = random.uniform(3.5, 6.0)
            outlier = int(max_typical * multiplier)
            dataset = typical_values + [outlier]
            random.shuffle(dataset)

            # Calculate statistics
            mean = sum(dataset) / len(dataset)
            sorted_data = sorted(dataset)
            n = len(sorted_data)
            if n % 2 == 0:
                median = (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2
            else:
                median = sorted_data[n // 2]

            # 3 different word problem contexts
            templates = [
                (
                    f"A teacher recorded quiz scores for students: {dataset}. "
                    f"Is the mean score representative of typical student performance?",
                    "quiz scores"
                ),
                (
                    f"A company tracked monthly website visitors (in thousands): {dataset}. "
                    f"Does the mean accurately represent typical monthly traffic?",
                    "website visitors"
                ),
                (
                    f"Daily rainfall amounts (in mm) for a city: {dataset}. "
                    f"Is the mean rainfall representative of typical daily rainfall?",
                    "rainfall amounts"
                )
            ]

            problem_text, context = templates[variant]
            correct_answer = "No, mean is not representative"
            malrule_answer = "Yes, mean is representative"

            return Problem(
                text=problem_text,
                operands=dataset,
                operation='representativeness',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'data': dataset,
                    'outlier': outlier,
                    'outlier_direction': 'high',
                    'mean': mean,
                    'median': median,
                    'has_outlier': True,
                    'correct_answer': correct_answer,
                    'malrule_answer': malrule_answer,
                    'template': 'word_problem_expanded',
                    'is_word_problem': True,
                    'word_problem_type': formula_type,
                    'word_problem_variant': variant,
                    'context': context
                }
            )

        elif formula_type == 'choose_appropriate_measure':
            # Generate dataset with outlier to choose between mean and median
            num_typical = random.randint(6, 8)
            typical_values = [random.randint(min_typical, max_typical) for _ in range(num_typical)]

            # Add high outlier
            multiplier = random.uniform(4.0, 7.0)
            outlier = int(max_typical * multiplier)
            dataset = typical_values + [outlier]
            random.shuffle(dataset)

            # Calculate statistics
            mean = sum(dataset) / len(dataset)
            sorted_data = sorted(dataset)
            n = len(sorted_data)
            if n % 2 == 0:
                median = (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2
            else:
                median = sorted_data[n // 2]

            # 3 different word problem contexts
            templates = [
                (
                    f"Housing prices in a neighborhood (in $1000s): {dataset}. "
                    f"Which measure of center best represents the typical home price: mean or median?",
                    "housing prices"
                ),
                (
                    f"Employee ages at a startup company: {dataset}. "
                    f"For HR statistics, should they report mean age or median age?",
                    "employee ages"
                ),
                (
                    f"Number of hours spent studying per week by students: {dataset}. "
                    f"Which statistic better represents typical study time: mean or median?",
                    "study hours"
                )
            ]

            problem_text, context = templates[variant]
            correct_answer = f"Median ({median}) because mean ({mean:.1f}) is distorted by outlier"
            malrule_answer = f"Mean ({mean:.1f}) is always the best measure"

            return Problem(
                text=problem_text,
                operands=dataset,
                operation='representativeness',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'data': dataset,
                    'outlier': outlier,
                    'outlier_direction': 'high',
                    'mean': mean,
                    'median': median,
                    'has_outlier': True,
                    'correct_answer': correct_answer,
                    'malrule_answer': malrule_answer,
                    'template': 'word_problem_expanded',
                    'is_word_problem': True,
                    'word_problem_type': formula_type,
                    'word_problem_variant': variant,
                    'context': context
                }
            )

        elif formula_type == 'identify_outlier_effect':
            # Generate dataset showing clear outlier effect on mean
            num_typical = random.randint(5, 7)
            typical_values = [random.randint(min_typical, max_typical) for _ in range(num_typical)]

            # Add outlier
            multiplier = random.uniform(4.5, 8.0)
            outlier = int(max_typical * multiplier)
            dataset = typical_values + [outlier]
            random.shuffle(dataset)

            # Calculate statistics
            mean = sum(dataset) / len(dataset)
            mean_without_outlier = sum(typical_values) / len(typical_values)
            sorted_data = sorted(dataset)
            n = len(sorted_data)
            if n % 2 == 0:
                median = (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2
            else:
                median = sorted_data[n // 2]

            # 3 different word problem contexts
            templates = [
                (
                    f"A basketball player's points per game: {dataset}. "
                    f"The mean is {mean:.1f}. Does this value represent the player's typical performance? "
                    f"Explain the effect of any outliers.",
                    "points per game"
                ),
                (
                    f"Daily customer counts at a store: {dataset}. "
                    f"The mean is {mean:.1f} customers. Does this reflect typical daily traffic? "
                    f"Consider any unusual days.",
                    "customer counts"
                ),
                (
                    f"Completion times (in minutes) for a task: {dataset}. "
                    f"The mean time is {mean:.1f} minutes. Is this representative? "
                    f"Identify any extreme values affecting the mean.",
                    "completion times"
                )
            ]

            problem_text, context = templates[variant]
            correct_answer = f"No, outlier ({outlier}) pulls mean to {mean:.1f}, far from typical values (median={median})"
            malrule_answer = f"Yes, mean is {mean:.1f}, which represents the data"

            return Problem(
                text=problem_text,
                operands=dataset,
                operation='representativeness',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'data': dataset,
                    'outlier': outlier,
                    'outlier_direction': 'high',
                    'mean': mean,
                    'median': median,
                    'mean_without_outlier': mean_without_outlier,
                    'has_outlier': True,
                    'correct_answer': correct_answer,
                    'malrule_answer': malrule_answer,
                    'template': 'word_problem_expanded',
                    'is_word_problem': True,
                    'word_problem_type': formula_type,
                    'word_problem_variant': variant,
                    'context': context
                }
            )
