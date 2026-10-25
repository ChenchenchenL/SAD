"""
Problem generator for Confuse-Slope-And-Intercept-Roles malrule.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Tuple, List, Optional
from utils import ProblemGenerator, Problem, DifficultyLevel


class ConfuseSlopeAndInterceptRolesProblemGenerator(ProblemGenerator):
    """Generates linear equation problems to test understanding of slope vs y-intercept roles."""

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        return [
            'write_equation',
            'identify_slope',
            'identify_y_intercept',
            'standard_form_identify',
            'word_problem_context'
        ]

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        ranges = {
            7: {
                DifficultyLevel.EASY: {'slope_min': 1, 'slope_max': 5, 'b_min': 1, 'b_max': 8},
                DifficultyLevel.MEDIUM: {'slope_min': -5, 'slope_max': 8, 'b_min': -8, 'b_max': 10},
                DifficultyLevel.HARD: {'slope_min': -8, 'slope_max': 10, 'b_min': -12, 'b_max': 12}
            },
            8: {
                DifficultyLevel.EASY: {'slope_min': 1, 'slope_max': 6, 'b_min': 1, 'b_max': 10},
                DifficultyLevel.MEDIUM: {'slope_min': -6, 'slope_max': 10, 'b_min': -10, 'b_max': 12},
                DifficultyLevel.HARD: {'slope_min': -10, 'slope_max': 12, 'b_min': -15, 'b_max': 15}
            },
            9: {
                DifficultyLevel.EASY: {'slope_min': -5, 'slope_max': 8, 'b_min': -8, 'b_max': 10},
                DifficultyLevel.MEDIUM: {'slope_min': -8, 'slope_max': 12, 'b_min': -12, 'b_max': 15},
                DifficultyLevel.HARD: {'slope_min': -12, 'slope_max': 15, 'b_min': -20, 'b_max': 20}
            },
            10: {
                DifficultyLevel.EASY: {'slope_min': -6, 'slope_max': 10, 'b_min': -10, 'b_max': 12},
                DifficultyLevel.MEDIUM: {'slope_min': -10, 'slope_max': 15, 'b_min': -15, 'b_max': 18},
                DifficultyLevel.HARD: {'slope_min': -15, 'slope_max': 20, 'b_min': -25, 'b_max': 25}
            }
        }
        lvl = self.level if self.level in ranges else 8
        return ranges[lvl][self.difficulty]

    def generate(self, seed=None, template: Optional[str] = None) -> Problem:
        """
        Generate a slope-intercept problem based on selected template.

        Args:
            seed: Optional random seed for reproducibility
            template: Specific template to use, or None for random selection

        Returns:
            Problem testing understanding of slope vs y-intercept roles
        """
        if seed is not None:
            random.seed(seed)

        # Select template
        if template is None:
            template = random.choice(self.get_available_templates())

        # Generate based on template
        if template == 'write_equation':
            return self._generate_write_equation(seed)
        elif template == 'identify_slope':
            return self._generate_identify_slope(seed)
        elif template == 'identify_y_intercept':
            return self._generate_identify_y_intercept(seed)
        elif template == 'standard_form_identify':
            return self._generate_standard_form_identify(seed)
        elif template == 'word_problem_context':
            return self._generate_word_problem_context(seed)
        else:
            raise ValueError(f"Unknown template: {template}")

    def _generate_write_equation(self, seed=None) -> Problem:
        """Generate problem: write equation given slope and y-intercept."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        m, b = self._generate_m_and_b(ranges)

        text = f"Write the equation of a line with slope {m} and y-intercept {b}."

        # Correct equation: y = mx + b
        correct_equation = self._format_equation(m, b)

        # Malrule equation: y = bx + m (swapped!)
        malrule_equation = self._format_equation(b, m)

        return Problem(
            text=text,
            operands=[m, b],
            operation='write_equation',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'slope': m,
                'y_intercept': b,
                'problem_type': 'write_equation',
                'correct_equation': correct_equation,
                'malrule_equation': malrule_equation,
                'correct_answer': correct_equation,
                'malrule_answer': malrule_equation,
                'template': 'write_equation'
            }
        )

    def _generate_identify_slope(self, seed=None) -> Problem:
        """Generate problem: identify slope from equation."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        m, b = self._generate_m_and_b(ranges)

        equation = self._format_equation(m, b)
        text = f"What is the slope of the line {equation}?"

        # Correct answer: m
        correct_answer = str(m)

        # Malrule answer: b (student confuses slope with y-intercept)
        malrule_answer = str(b)

        return Problem(
            text=text,
            operands=[m, b],
            operation='identify_slope',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'slope': m,
                'y_intercept': b,
                'equation': equation,
                'problem_type': 'identify_slope',
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'template': 'identify_slope'
            }
        )

    def _generate_identify_y_intercept(self, seed=None) -> Problem:
        """Generate problem: identify y-intercept from equation."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        m, b = self._generate_m_and_b(ranges)

        equation = self._format_equation(m, b)
        text = f"What is the y-intercept of the line {equation}?"

        # Correct answer: b
        correct_answer = str(b)

        # Malrule answer: m (student confuses y-intercept with slope)
        malrule_answer = str(m)

        return Problem(
            text=text,
            operands=[m, b],
            operation='identify_y_intercept',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'slope': m,
                'y_intercept': b,
                'equation': equation,
                'problem_type': 'identify_y_intercept',
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'template': 'identify_y_intercept'
            }
        )

    def _generate_standard_form_identify(self, seed=None) -> Problem:
        """Generate problem: identify slope from standard form equation."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        m, b = self._generate_m_and_b(ranges)

        # Convert y = mx + b to Ax + By = C
        # y = mx + b → -mx + y = b → multiply by -1 if needed
        A = -m
        B = 1
        C = b

        # Make A positive if possible
        if A < 0:
            A, B, C = -A, -B, -C

        # Format equation
        if A == 1:
            if B == 1:
                equation = f"x + y = {C}"
            elif B == -1:
                equation = f"x - y = {C}"
            else:
                equation = f"x + {B}y = {C}" if B > 0 else f"x - {abs(B)}y = {C}"
        else:
            if B == 1:
                equation = f"{A}x + y = {C}"
            elif B == -1:
                equation = f"{A}x - y = {C}"
            else:
                equation = f"{A}x + {B}y = {C}" if B > 0 else f"{A}x - {abs(B)}y = {C}"

        text = f"What is the slope of the line {equation}?"

        # Correct answer: slope = -A/B (in standard form)
        # But we know from y = mx + b that slope = m
        correct_answer = str(m)

        # Malrule answer: student thinks slope is related to constant C (confuses with b)
        # Student might convert incorrectly and swap roles
        malrule_answer = str(b)

        return Problem(
            text=text,
            operands=[A, B, C],
            operation='identify_slope',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'A': A,
                'B': B,
                'C': C,
                'slope': m,
                'y_intercept': b,
                'equation': equation,
                'problem_type': 'standard_form_identify',
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'template': 'standard_form_identify'
            }
        )

    def _generate_word_problem_context(self, seed=None) -> Problem:
        """Generate comprehensive word problems covering all applicable cases."""
        if seed is not None:
            random.seed(seed)

        # Select word problem type (what aspect of slope/intercept to test)
        word_problem_types = ['write_equation', 'identify_slope', 'identify_intercept']
        problem_type = random.choice(word_problem_types)

        if problem_type == 'write_equation':
            return self._generate_word_problem_write_equation(seed)
        elif problem_type == 'identify_slope':
            return self._generate_word_problem_identify_slope(seed)
        elif problem_type == 'identify_intercept':
            return self._generate_word_problem_identify_intercept(seed)

    def _generate_word_problem_write_equation(self, seed=None) -> Problem:
        """Word problem: Write equation from rate and starting value."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        slope_max = ranges['slope_max']
        m = random.randint(1, max(5, slope_max))

        b_min = ranges['b_min']
        b_max = ranges['b_max']
        b = random.randint(max(0, b_min), b_max)
        if b == m:
            b = m + 2

        # Three context scenarios, each with 3 question variations
        scenarios = [
            {
                'context_type': 'taxi_service',
                'questions': [
                    f"A taxi charges ${b} as a base fare plus ${m} per mile traveled. Write an equation for the total cost C in terms of miles d.",
                    f"A rideshare service has a pickup fee of ${b} and charges ${m} for each mile. Create an equation for total cost C based on distance d in miles.",
                    f"The cost of a taxi ride starts at ${b} and increases by ${m} per mile. Write an equation showing how total cost C relates to miles driven d."
                ]
            },
            {
                'context_type': 'phone_plan',
                'questions': [
                    f"A phone plan costs ${b} per month as a base fee, plus ${m} per gigabyte of data. Write an equation for monthly cost M in terms of gigabytes g used.",
                    f"Your cell phone plan has a ${b} monthly charge and ${m} per GB of data used. Create an equation for the total bill M based on data usage g in GB.",
                    f"A mobile plan starts at ${b}/month and adds ${m} for each gigabyte of data. Write an equation for the total cost M as a function of data usage g."
                ]
            },
            {
                'context_type': 'car_rental',
                'questions': [
                    f"A rental car costs ${b} per day plus ${m} per mile driven. Write an equation for daily cost D based on miles m driven.",
                    f"Car rental pricing is ${b} for the day plus ${m} per mile. Create an equation showing total daily cost D in terms of miles m.",
                    f"The daily rate for a car rental is ${b} with an additional ${m} per mile. Write an equation relating total cost D to miles driven m."
                ]
            }
        ]

        scenario = random.choice(scenarios)
        question_text = random.choice(scenario['questions'])

        correct_equation = f"y = {m}x + {b}"
        malrule_equation = f"y = {b}x + {m}"

        return Problem(
            text=question_text,
            operands=[m, b],
            operation='write_equation',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'slope': m,
                'y_intercept': b,
                'context_type': scenario['context_type'],
                'problem_type': 'word_problem_context',
                'word_problem_subtype': 'write_equation',
                'rate_name': 'rate',
                'starting_name': 'starting value',
                'correct_equation': correct_equation,
                'malrule_equation': malrule_equation,
                'correct_answer': correct_equation,
                'malrule_answer': malrule_equation,
                'template': 'word_problem_context'
            }
        )

    def _generate_word_problem_identify_slope(self, seed=None) -> Problem:
        """Word problem: Identify slope/rate from context."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        slope_max = ranges['slope_max']
        m = random.randint(1, max(5, slope_max))

        b_min = ranges['b_min']
        b_max = ranges['b_max']
        b = random.randint(max(0, b_min), b_max)
        if b == m:
            b = m + 2

        scenarios = [
            {
                'context_type': 'plant_growth',
                'questions': [
                    f"A plant is {b} inches tall and grows {m} inches per week. What is the growth rate (slope) in inches per week?",
                    f"Starting at {b} inches, a bamboo plant grows {m} inches each week. Identify the rate of growth (slope).",
                    f"A seedling measures {b} inches initially and increases by {m} inches weekly. What is the slope representing the growth rate?"
                ]
            },
            {
                'context_type': 'savings_account',
                'questions': [
                    f"Maria has ${b} in savings and deposits ${m} each week. What is the rate of savings (slope) per week?",
                    f"A savings account starts with ${b} and gains ${m} per week. Identify the weekly savings rate (slope).",
                    f"Starting with ${b}, Juan saves ${m} every week. What is the slope of his savings rate?"
                ]
            },
            {
                'context_type': 'distance_travel',
                'questions': [
                    f"A car is {b} miles from home and travels away at {m} miles per hour. What is the speed (slope)?",
                    f"Starting {b} miles from the start point, a cyclist travels at {m} miles per hour. What is the rate (slope) of travel?",
                    f"A vehicle begins {b} miles into a journey and continues at {m} mph. Identify the slope representing speed."
                ]
            }
        ]

        scenario = random.choice(scenarios)
        question_text = random.choice(scenario['questions'])

        correct_answer = str(m)
        malrule_answer = str(b)

        return Problem(
            text=question_text,
            operands=[m, b],
            operation='identify_slope',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'slope': m,
                'y_intercept': b,
                'context_type': scenario['context_type'],
                'problem_type': 'word_problem_context',
                'word_problem_subtype': 'identify_slope',
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'template': 'word_problem_context'
            }
        )

    def _generate_word_problem_identify_intercept(self, seed=None) -> Problem:
        """Word problem: Identify y-intercept/starting value from context."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        slope_max = ranges['slope_max']
        m = random.randint(1, max(5, slope_max))

        b_min = ranges['b_min']
        b_max = ranges['b_max']
        b = random.randint(max(0, b_min), b_max)
        if b == m:
            b = m + 2

        scenarios = [
            {
                'context_type': 'initial_investment',
                'questions': [
                    f"An investment starts with an initial amount and grows by ${m} per month. If the equation is A = {m}t + {b}, what is the initial investment (y-intercept)?",
                    f"The value of an account increases by ${m} monthly, described by V = {m}m + {b}. What is the starting balance (y-intercept)?",
                    f"Given the equation P = {m}t + {b} for an investment growing at ${m} per period, what is the initial value (y-intercept)?"
                ]
            },
            {
                'context_type': 'starting_position',
                'questions': [
                    f"A hiker moves upward at {m} meters per minute, following equation h = {m}t + {b}. What is the starting elevation (y-intercept)?",
                    f"An elevator rises at {m} feet per second, described by h = {m}t + {b}. What is the initial height (y-intercept)?",
                    f"Given altitude equation a = {m}t + {b}, where a climber ascends {m} meters per minute, find the starting altitude (y-intercept)."
                ]
            },
            {
                'context_type': 'base_cost',
                'questions': [
                    f"A subscription costs ${m} per month plus a base fee, with total C = {m}n + {b}. What is the base fee (y-intercept)?",
                    f"The pricing equation is P = {m}x + {b}, where ${m} is charged per unit. What is the fixed cost (y-intercept)?",
                    f"Given cost formula C = {m}q + {b} with ${m} per item, identify the base charge (y-intercept)."
                ]
            }
        ]

        scenario = random.choice(scenarios)
        question_text = random.choice(scenario['questions'])

        correct_answer = str(b)
        malrule_answer = str(m)

        return Problem(
            text=question_text,
            operands=[m, b],
            operation='identify_y_intercept',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'slope': m,
                'y_intercept': b,
                'context_type': scenario['context_type'],
                'problem_type': 'word_problem_context',
                'word_problem_subtype': 'identify_intercept',
                'correct_answer': correct_answer,
                'malrule_answer': malrule_answer,
                'template': 'word_problem_context'
            }
        )

    def _generate_m_and_b(self, ranges):
        """Helper to generate m and b that are different from each other."""
        slope_min = ranges['slope_min']
        slope_max = ranges['slope_max']
        b_min = ranges['b_min']
        b_max = ranges['b_max']

        # Generate slope (m) - avoid 0
        attempts = 0
        while attempts < 100:
            m = random.randint(slope_min, slope_max)
            if m != 0:
                break
            attempts += 1

        if attempts >= 100:
            m = 2  # fallback

        # Generate y-intercept (b) - avoid 0 and ensure b != m
        attempts = 0
        while attempts < 100:
            b = random.randint(b_min, b_max)
            if b != 0 and b != m:
                break
            attempts += 1

        if attempts >= 100:
            b = m + 3  # fallback that ensures b != m

        return m, b

    def _format_equation(self, m, b):
        """Format equation y = mx + b with proper sign handling."""
        # Format slope coefficient
        if m == 1:
            m_str = ""
        elif m == -1:
            m_str = "-"
        else:
            m_str = str(m)

        # Format the b term with proper sign
        if b >= 0:
            equation = f"y = {m_str}x + {b}"
        else:
            equation = f"y = {m_str}x - {abs(b)}"

        return equation
