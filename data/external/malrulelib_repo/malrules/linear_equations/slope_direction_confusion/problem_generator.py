"""
Problem generator for Slope-Direction-Confusion malrule.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Tuple, Optional, List
from utils import ProblemGenerator, Problem, DifficultyLevel


class SlopeDirectionConfusionProblemGenerator(ProblemGenerator):
    """Generates slope direction problems to test understanding of positive/negative slopes."""

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        ranges = {
            7: {
                DifficultyLevel.EASY: {'slope_min': -5, 'slope_max': 5},
                DifficultyLevel.MEDIUM: {'slope_min': -8, 'slope_max': 8},
                DifficultyLevel.HARD: {'slope_min': -12, 'slope_max': 12}
            },
            8: {
                DifficultyLevel.EASY: {'slope_min': -6, 'slope_max': 6},
                DifficultyLevel.MEDIUM: {'slope_min': -10, 'slope_max': 10},
                DifficultyLevel.HARD: {'slope_min': -15, 'slope_max': 15}
            },
            9: {
                DifficultyLevel.EASY: {'slope_min': -8, 'slope_max': 8},
                DifficultyLevel.MEDIUM: {'slope_min': -12, 'slope_max': 12},
                DifficultyLevel.HARD: {'slope_min': -20, 'slope_max': 20}
            },
            10: {
                DifficultyLevel.EASY: {'slope_min': -10, 'slope_max': 10},
                DifficultyLevel.MEDIUM: {'slope_min': -15, 'slope_max': 15},
                DifficultyLevel.HARD: {'slope_min': -25, 'slope_max': 25}
            }
        }
        lvl = self.level if self.level in ranges else 8
        return ranges[lvl][self.difficulty]

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        return [
            'basic_positive_slope',
            'basic_negative_slope',
            'larger_magnitude',
            'fractional_slope',
            'comparison_problem',
            'word_problem_context'
        ]

    def generate(self, seed: Optional[int] = None, template: Optional[str] = None) -> Problem:
        """
        Generate a slope direction problem.

        Args:
            seed: Optional random seed for reproducibility
            template: Specific template to use, or None for random selection

        Returns:
            Problem testing slope direction understanding
        """
        if seed is not None:
            random.seed(seed)

        # Select template
        if template is None:
            # For random generation, use mix of positive and negative slopes
            template = random.choice(self.get_available_templates())

        # Generate based on template
        if template == 'basic_positive_slope':
            return self._generate_basic_positive_slope(seed)
        elif template == 'basic_negative_slope':
            return self._generate_basic_negative_slope(seed)
        elif template == 'larger_magnitude':
            return self._generate_larger_magnitude(seed)
        elif template == 'fractional_slope':
            return self._generate_fractional_slope(seed)
        elif template == 'comparison_problem':
            return self._generate_comparison_problem(seed)
        elif template == 'word_problem_context':
            return self._generate_word_problem_context(seed)
        else:
            raise ValueError(f"Unknown template: {template}")

    def _generate_basic_positive_slope(self, seed: Optional[int] = None) -> Problem:
        """
        Template 1: Basic positive slope (small integer values).

        Tests fundamental understanding of positive slope direction.

        Args:
            seed: Optional random seed for reproducibility

        Returns:
            Problem with small positive slope
        """
        if seed is not None:
            random.seed(seed)

        # Small positive slope (1-5)
        m = random.randint(1, 5)

        correct_direction = "increasing"
        malrule_direction = "decreasing"
        correct_description = "going up from left to right"
        malrule_description = "going down from left to right"

        text = f"Describe the direction of a line with slope {m}. Is the line increasing or decreasing from left to right?"

        return Problem(
            text=text,
            operands=[m],
            operation='describe_slope_direction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'slope': m,
                'correct_direction': correct_direction,
                'malrule_direction': malrule_direction,
                'correct_description': correct_description,
                'malrule_description': malrule_description,
                'correct_answer': correct_direction,
                'malrule_answer': malrule_direction,
                'template': 'basic_positive_slope'
            }
        )

    def _generate_basic_negative_slope(self, seed: Optional[int] = None) -> Problem:
        """
        Template 2: Basic negative slope (small integer values).

        Tests fundamental understanding of negative slope direction.

        Args:
            seed: Optional random seed for reproducibility

        Returns:
            Problem with small negative slope
        """
        if seed is not None:
            random.seed(seed)

        # Small negative slope (-5 to -1)
        m = random.randint(-5, -1)

        correct_direction = "decreasing"
        malrule_direction = "increasing"
        correct_description = "going down from left to right"
        malrule_description = "going up from left to right"

        text = f"Describe the direction of a line with slope {m}. Is the line increasing or decreasing from left to right?"

        return Problem(
            text=text,
            operands=[m],
            operation='describe_slope_direction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'slope': m,
                'correct_direction': correct_direction,
                'malrule_direction': malrule_direction,
                'correct_description': correct_description,
                'malrule_description': malrule_description,
                'correct_answer': correct_direction,
                'malrule_answer': malrule_direction,
                'template': 'basic_negative_slope'
            }
        )

    def _generate_larger_magnitude(self, seed: Optional[int] = None) -> Problem:
        """
        Template 3: Larger magnitude slopes (tests if magnitude affects confusion).

        Uses larger slope values to test if students maintain the misconception
        with steep lines.

        Args:
            seed: Optional random seed for reproducibility

        Returns:
            Problem with larger magnitude slope
        """
        if seed is not None:
            random.seed(seed)

        # Larger slope (magnitude 7-15), randomly positive or negative
        magnitude = random.randint(7, 15)
        m = magnitude if random.choice([True, False]) else -magnitude

        if m > 0:
            correct_direction = "increasing"
            malrule_direction = "decreasing"
            correct_description = "going up from left to right"
            malrule_description = "going down from left to right"
        else:
            correct_direction = "decreasing"
            malrule_direction = "increasing"
            correct_description = "going down from left to right"
            malrule_description = "going up from left to right"

        text = f"A line has slope {m}. Is the line increasing or decreasing?"

        return Problem(
            text=text,
            operands=[m],
            operation='describe_slope_direction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'slope': m,
                'correct_direction': correct_direction,
                'malrule_direction': malrule_direction,
                'correct_description': correct_description,
                'malrule_description': malrule_description,
                'correct_answer': correct_direction,
                'malrule_answer': malrule_direction,
                'template': 'larger_magnitude'
            }
        )

    def _generate_fractional_slope(self, seed: Optional[int] = None) -> Problem:
        """
        Template 4: Fractional slope (tests with non-integer slopes).

        Uses fractional slopes like 1/2, -3/4 to test if the misconception
        persists with non-integer values.

        Args:
            seed: Optional random seed for reproducibility

        Returns:
            Problem with fractional slope
        """
        if seed is not None:
            random.seed(seed)

        # Generate fraction: numerator/denominator
        numerator = random.choice([-3, -2, -1, 1, 2, 3])
        denominator = random.choice([2, 3, 4, 5])

        # Determine sign
        if numerator > 0:
            correct_direction = "increasing"
            malrule_direction = "decreasing"
            correct_description = "going up from left to right"
            malrule_description = "going down from left to right"
        else:
            correct_direction = "decreasing"
            malrule_direction = "increasing"
            correct_description = "going down from left to right"
            malrule_description = "going up from left to right"

        text = f"What is the direction of a line with slope {numerator}/{denominator}? Is it increasing or decreasing?"

        return Problem(
            text=text,
            operands=[numerator, denominator],
            operation='describe_slope_direction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'slope': f"{numerator}/{denominator}",
                'slope_value': numerator / denominator,
                'numerator': numerator,
                'denominator': denominator,
                'correct_direction': correct_direction,
                'malrule_direction': malrule_direction,
                'correct_description': correct_description,
                'malrule_description': malrule_description,
                'correct_answer': correct_direction,
                'malrule_answer': malrule_direction,
                'template': 'fractional_slope'
            }
        )

    def _generate_comparison_problem(self, seed: Optional[int] = None) -> Problem:
        """
        Template 5: Compare directions of two lines with opposite slope signs.

        Asks students to compare the directions of two lines: one with positive
        slope and one with negative slope.

        Args:
            seed: Optional random seed for reproducibility

        Returns:
            Problem comparing two slope directions
        """
        if seed is not None:
            random.seed(seed)

        # Line A: positive slope
        m_a = random.randint(2, 6)
        # Line B: negative slope
        m_b = random.randint(-6, -2)

        text = f"Line A has slope {m_a}, and Line B has slope {m_b}. Which line is increasing and which is decreasing?"

        # Correct: A is increasing, B is decreasing
        correct_answer = f"Line A is increasing, Line B is decreasing"

        # Malrule: A is decreasing, B is increasing (backwards!)
        malrule_answer = f"Line A is decreasing, Line B is increasing"

        return Problem(
            text=text,
            operands=[m_a, m_b],
            operation='describe_slope_direction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'slope_a': m_a,
                'slope_b': m_b,
                'direction_a_correct': 'increasing',
                'direction_b_correct': 'decreasing',
                'direction_a_malrule': 'decreasing',
                'direction_b_malrule': 'increasing',
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'template': 'comparison_problem'
            }
        )

    def _generate_word_problem_context(self, seed=None) -> Problem:
        """Generate word problems testing slope direction in real-world contexts."""
        if seed is not None:
            random.seed(seed)

        # Select word problem type
        word_problem_types = ['positive_trend', 'negative_trend', 'compare_trends']
        problem_type = random.choice(word_problem_types)

        if problem_type == 'positive_trend':
            return self._generate_word_problem_positive_trend(seed)
        elif problem_type == 'negative_trend':
            return self._generate_word_problem_negative_trend(seed)
        elif problem_type == 'compare_trends':
            return self._generate_word_problem_compare_trends(seed)

    def _generate_word_problem_positive_trend(self, seed=None) -> Problem:
        """Word problem with positive slope context."""
        if seed is not None:
            random.seed(seed)

        # Generate positive slope
        m = random.randint(2, 8)

        scenarios = [
            {
                'context_type': 'profit_growth',
                'questions': [
                    f"A company's profit increases by ${m} thousand per month. Is the profit trend increasing or decreasing over time?",
                    f"Monthly profits are growing at a rate of ${m} thousand per month. Describe whether this trend is increasing or decreasing.",
                    f"A business sees profits rise ${m} thousand each month. Is this an increasing or decreasing trend?"
                ]
            },
            {
                'context_type': 'temperature_rise',
                'questions': [
                    f"The temperature rises {m}°F per hour during the day. Is the temperature increasing or decreasing?",
                    f"As morning progresses, temperature climbs {m} degrees per hour. Describe if this is an increasing or decreasing pattern.",
                    f"During sunrise, the temperature goes up {m}°F every hour. Is this trend increasing or decreasing?"
                ]
            },
            {
                'context_type': 'population_growth',
                'questions': [
                    f"A town's population grows by {m} hundred people per year. Is the population increasing or decreasing?",
                    f"The number of residents rises by {m}00 annually. Describe whether the population is increasing or decreasing.",
                    f"Population expands by {m}00 people each year. Is this an increasing or decreasing trend?"
                ]
            }
        ]

        scenario = random.choice(scenarios)
        question_text = random.choice(scenario['questions'])

        correct_answer = "increasing"
        malrule_answer = "decreasing"

        return Problem(
            text=question_text,
            operands=[m],
            operation='describe_slope_direction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'slope': m,
                'context_type': scenario['context_type'],
                'problem_type': 'word_problem_context',
                'word_problem_subtype': 'positive_trend',
                'correct_direction': correct_answer,
                'malrule_direction': malrule_answer,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'template': 'word_problem_context'
            }
        )

    def _generate_word_problem_negative_trend(self, seed=None) -> Problem:
        """Word problem with negative slope context."""
        if seed is not None:
            random.seed(seed)

        # Generate positive magnitude for readability
        m_magnitude = random.randint(2, 8)
        m = -m_magnitude

        scenarios = [
            {
                'context_type': 'debt_reduction',
                'questions': [
                    f"Someone's debt decreases by ${m_magnitude} per month. Is the debt increasing or decreasing?",
                    f"A loan balance drops ${m_magnitude} each month through payments. Is this amount increasing or decreasing?",
                    f"Monthly debt falls by ${m_magnitude}. Describe if the debt is increasing or decreasing."
                ]
            },
            {
                'context_type': 'water_draining',
                'questions': [
                    f"Water level in a tank drops {m_magnitude} inches per hour as it drains. Is the water level increasing or decreasing?",
                    f"A pool empties at a rate of {m_magnitude} inches per hour. Is the water level increasing or decreasing?",
                    f"As water drains, the level falls {m_magnitude} inches each hour. Describe if this is increasing or decreasing."
                ]
            },
            {
                'context_type': 'altitude_descending',
                'questions': [
                    f"An airplane descends {m_magnitude} hundred feet per minute. Is the altitude increasing or decreasing?",
                    f"During landing, altitude drops {m_magnitude}00 feet each minute. Is the plane's height increasing or decreasing?",
                    f"A helicopter loses {m_magnitude}00 feet of elevation per minute. Is altitude increasing or decreasing?"
                ]
            }
        ]

        scenario = random.choice(scenarios)
        question_text = random.choice(scenario['questions'])

        correct_answer = "decreasing"
        malrule_answer = "increasing"

        return Problem(
            text=question_text,
            operands=[m],
            operation='describe_slope_direction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'slope': m,
                'context_type': scenario['context_type'],
                'problem_type': 'word_problem_context',
                'word_problem_subtype': 'negative_trend',
                'correct_direction': correct_answer,
                'malrule_direction': malrule_answer,
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'template': 'word_problem_context'
            }
        )

    def _generate_word_problem_compare_trends(self, seed=None) -> Problem:
        """Word problem comparing two trends with opposite directions."""
        if seed is not None:
            random.seed(seed)

        m_a = random.randint(2, 6)
        m_b_magnitude = random.randint(2, 6)
        m_b = -m_b_magnitude

        scenarios = [
            {
                'context_type': 'comparing_businesses',
                'questions': [
                    f"Company A's revenue grows ${m_a}k monthly while Company B's revenue decreases ${m_b_magnitude}k monthly. Which company has increasing revenue and which has decreasing?",
                    f"Business A gains ${m_a},000 per month in sales, while Business B loses ${m_b_magnitude},000 monthly. Identify which is increasing and which is decreasing.",
                    f"Store A's profits rise ${m_a}k each month; Store B's profits fall ${m_b_magnitude}k monthly. Which trend is increasing and which is decreasing?"
                ]
            },
            {
                'context_type': 'comparing_temperatures',
                'questions': [
                    f"In City A, temperature rises {m_a}°F per hour. In City B, it drops {m_b_magnitude}°F per hour. Which city has increasing temperature and which has decreasing?",
                    f"Location A warms up {m_a} degrees hourly while Location B cools down {m_b_magnitude} degrees hourly. Identify increasing vs decreasing trends.",
                    f"Region A's temperature climbs {m_a}°F/hour; Region B's falls {m_b_magnitude}°F/hour. Which is increasing and which is decreasing?"
                ]
            },
            {
                'context_type': 'comparing_accounts',
                'questions': [
                    f"Account A gains ${m_a} daily, Account B loses ${m_b_magnitude} daily. Which account balance is increasing and which is decreasing?",
                    f"Savings A grows by ${m_a} per day while Savings B shrinks by ${m_b_magnitude} daily. Identify which is increasing and which is decreasing.",
                    f"Balance A rises ${m_a} each day; Balance B drops ${m_b_magnitude} daily. Which trend is increasing and which is decreasing?"
                ]
            }
        ]

        scenario = random.choice(scenarios)
        question_text = random.choice(scenario['questions'])

        correct_answer = "A is increasing, B is decreasing"
        malrule_answer = "A is decreasing, B is increasing"

        return Problem(
            text=question_text,
            operands=[m_a, m_b],
            operation='describe_slope_direction',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'slope_a': m_a,
                'slope_b': m_b,
                'context_type': scenario['context_type'],
                'problem_type': 'word_problem_context',
                'word_problem_subtype': 'compare_trends',
                'direction_a_correct': 'increasing',
                'direction_b_correct': 'decreasing',
                'direction_a_malrule': 'decreasing',
                'direction_b_malrule': 'increasing',
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'template': 'word_problem_context'
            }
        )
