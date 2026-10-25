"""
Problem generator for Multiply-Exponents-When-Multiplying-Powers malrule.

Generates problems where students need to multiply powers with the same base,
eliciting the misconception of multiplying exponents instead of adding them.
"""

import random
import sys
sys.path.append('/home/user/malrule-coding')

from typing import Dict, Tuple, Optional, List
from utils import Problem, ProblemGenerator, DifficultyLevel


class MultiplyExponentsWhenMultiplyingPowersProblemGenerator(ProblemGenerator):
    """
    Generates x^m × x^n problems.

    Templates:
    1. basic_two_powers - Simple x^m × x^n
    2. three_powers - Chain of three: x^a × x^b × x^c
    3. numerical_base - With actual numbers: 2^3 × 2^4
    4. mixed_operations - Combining mult and div: x^5 × x^3 ÷ x^2
    5. word_problem - Real-world exponential contexts (bacteria, compound interest)
    """

    def get_name(self) -> str:
        return "Multiply-Exponents-When-Multiplying-Powers Problem Generator"

    def get_description(self) -> str:
        return (
            "Generates power multiplication problems to elicit the misconception "
            "of multiplying exponents instead of adding them."
        )

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        return [
            'basic_two_powers',
            'three_powers',
            'numerical_base',
            'mixed_operations',
            'word_problem',  # Old word problem (kept for backwards compatibility)
            'word_problem_context'  # NEW: Covers all formula types with 3 variants each
        ]

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        """Return the value ranges for problem generation."""
        ranges = {
            7: {
                DifficultyLevel.EASY: (2, 4),
                DifficultyLevel.MEDIUM: (2, 5),
                DifficultyLevel.HARD: (2, 6),
            },
            8: {
                DifficultyLevel.EASY: (2, 5),
                DifficultyLevel.MEDIUM: (2, 6),
                DifficultyLevel.HARD: (3, 7),
            },
            9: {
                DifficultyLevel.EASY: (2, 6),
                DifficultyLevel.MEDIUM: (3, 7),
                DifficultyLevel.HARD: (3, 8),
            }
        }

        lvl = self.level if self.level in ranges else 8
        return {'exponent': ranges[lvl][self.difficulty]}

    def generate(self, seed: Optional[int] = None, template: Optional[str] = None) -> Problem:
        """
        Generate a power multiplication problem.

        Args:
            seed: Optional random seed for reproducibility
            template: Optional template name to use

        Returns:
            Problem with x^m × x^n question
        """
        if seed is not None:
            random.seed(seed)

        # Select template
        if template is None:
            template = random.choice(self.get_available_templates())

        # Generate based on template
        if template == 'basic_two_powers':
            return self._generate_basic_two_powers(seed)
        elif template == 'three_powers':
            return self._generate_three_powers(seed)
        elif template == 'numerical_base':
            return self._generate_numerical_base(seed)
        elif template == 'mixed_operations':
            return self._generate_mixed_operations(seed)
        elif template == 'word_problem':
            return self._generate_word_problem(seed)
        elif template == 'word_problem_context':
            return self._generate_word_problem_context(seed)
        else:
            raise ValueError(f"Unknown template: {template}")

    def _generate_basic_two_powers(self, seed=None) -> Problem:
        """Generate basic x^m × x^n."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        m = random.randint(*ranges['exponent'])
        n = random.randint(*ranges['exponent'])

        # Ensure m+n ≠ m×n (avoid cases like 2,2 where 2+2=4 and 2×2=4)
        while m + n == m * n or m == n == 2:
            n = random.randint(*ranges['exponent'])

        # Correct: add exponents
        correct_answer = m + n
        # Malrule: multiply exponents
        malrule_answer = m * n

        problem_statement = f"Simplify: x^{m} × x^{n}"

        metadata = {
            'template': 'basic_two_powers',
            'exponent1': m,
            'exponent2': n,
            'correct_answer': correct_answer,
            'malrule_answer': malrule_answer
        }

        return Problem(
            text=problem_statement,
            operands=[m, n],
            operation='multiply_powers',
            level=self.level,
            difficulty=self.difficulty,
            metadata=metadata
        )

    def _generate_three_powers(self, seed=None) -> Problem:
        """Generate x^a × x^b × x^c."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        a = random.randint(*ranges['exponent'])
        b = random.randint(*ranges['exponent'])
        c = random.randint(*ranges['exponent'])

        # Ensure a+b+c ≠ a×b×c (avoid edge cases)
        max_attempts = 10
        attempts = 0
        while (a + b + c == a * b * c) and attempts < max_attempts:
            c = random.randint(*ranges['exponent'])
            attempts += 1

        # Correct: add all exponents
        correct_answer = a + b + c
        # Malrule: multiply all exponents
        malrule_answer = a * b * c

        problem_statement = f"Simplify: x^{a} × x^{b} × x^{c}"

        metadata = {
            'template': 'three_powers',
            'exponent1': a,
            'exponent2': b,
            'exponent3': c,
            'correct_answer': correct_answer,
            'malrule_answer': malrule_answer
        }

        return Problem(
            text=problem_statement,
            operands=[a, b, c],
            operation='multiply_powers',
            level=self.level,
            difficulty=self.difficulty,
            metadata=metadata
        )

    def _generate_numerical_base(self, seed=None) -> Problem:
        """Generate 2^m × 2^n or 3^m × 3^n."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        m = random.randint(*ranges['exponent'])
        n = random.randint(*ranges['exponent'])

        # Use base 2 or 3
        base = random.choice([2, 3])

        # Correct: add exponents
        correct_answer = base ** (m + n)
        # Malrule: multiply exponents
        malrule_answer = base ** (m * n)

        problem_statement = f"Simplify: {base}^{m} × {base}^{n}"

        metadata = {
            'template': 'numerical_base',
            'base': base,
            'exponent1': m,
            'exponent2': n,
            'correct_answer': correct_answer,
            'correct_exponent': m + n,
            'malrule_answer': malrule_answer,
            'malrule_exponent': m * n
        }

        return Problem(
            text=problem_statement,
            operands=[base, m, n],
            operation='multiply_powers',
            level=self.level,
            difficulty=self.difficulty,
            metadata=metadata
        )

    def _generate_mixed_operations(self, seed=None) -> Problem:
        """Generate x^a × x^b ÷ x^c."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()

        max_attempts = 100
        for attempt in range(max_attempts):
            a = random.randint(*ranges['exponent'])
            b = random.randint(*ranges['exponent'])
            c = random.randint(2, min(ranges['exponent'][1], a + b - 1))  # Ensure result is positive

            # Correct: add for ×, subtract for ÷
            correct_answer = a + b - c
            # Malrule: multiply for ×, divide for ÷
            malrule_answer = (a * b) // c if (a * b) % c == 0 else (a * b) / c

            # Ensure correct != malrule (avoid edge cases)
            if correct_answer != malrule_answer:
                break

        # If we couldn't find a good case, use a known good case
        if correct_answer == malrule_answer:
            a, b, c = 3, 5, 2  # 3+5-2=6 vs (3*5)/2=7.5
            correct_answer = a + b - c
            malrule_answer = (a * b) / c

        problem_statement = f"Simplify: x^{a} × x^{b} ÷ x^{c}"

        metadata = {
            'template': 'mixed_operations',
            'exponent1': a,
            'exponent2': b,
            'exponent3': c,
            'correct_answer': correct_answer,
            'malrule_answer': malrule_answer
        }

        return Problem(
            text=problem_statement,
            operands=[a, b, c],
            operation='multiply_powers',
            level=self.level,
            difficulty=self.difficulty,
            metadata=metadata
        )

    def _generate_word_problem(self, seed=None) -> Problem:
        """Generate word problem with exponential context."""
        if seed is not None:
            random.seed(seed)

        ranges = self.get_value_ranges()
        m = random.randint(*ranges['exponent'])
        n = random.randint(*ranges['exponent'])

        contexts = [
            {
                'text': f"A bacteria colony doubles every hour. If it starts at 2^{m} bacteria and grows for {n} doubling periods, how many bacteria are there? (Express as a power of 2)",
                'type': 'bacteria',
                'correct': m + n,
                'malrule': m * n
            },
            {
                'text': f"A computer processes data in blocks of 2^{m} bytes. If it processes 2^{n} such blocks, how many bytes total? (Express as a power of 2)",
                'type': 'computer',
                'correct': m + n,
                'malrule': m * n
            },
            {
                'text': f"An investment triples (×3) every year. Starting with 3^{m} dollars and waiting {n} tripling periods, what's the amount? (Express as a power of 3)",
                'type': 'investment',
                'correct': m + n,
                'malrule': m * n
            }
        ]

        context = random.choice(contexts)

        problem_statement = context['text']
        correct_answer = context['correct']
        malrule_answer = context['malrule']

        base = 2 if 'bacteria' in context['type'] or 'computer' in context['type'] else 3

        metadata = {
            'template': 'word_problem',
            'base': base,
            'exponent1': m,
            'exponent2': n,
            'context_type': context['type'],
            'correct_answer': correct_answer,
            'malrule_answer': malrule_answer
        }

        return Problem(
            text=problem_statement,
            operands=[m, n],
            operation='multiply_powers',
            level=self.level,
            difficulty=self.difficulty,
            metadata=metadata
        )

    def _generate_word_problem_context(self, seed=None) -> Problem:
        """Generate word problem covering ALL formula types with 3 variants each."""
        if seed is not None:
            random.seed(seed)

        # Select which formula type to embed
        formula_types = ['basic_two_powers', 'three_powers', 'numerical_base', 'mixed_operations']
        formula_type = random.choice(formula_types)
        variant = random.randint(0, 2)  # 3 variants per formula type

        if formula_type == 'basic_two_powers':
            # Formula: x^m × x^n
            ranges = self.get_value_ranges()
            m = random.randint(*ranges['exponent'])
            n = random.randint(*ranges['exponent'])

            # Ensure m+n ≠ m×n
            while m + n == m * n or m == n == 2:
                n = random.randint(*ranges['exponent'])

            correct_answer = m + n
            malrule_answer = m * n

            templates = [
                f"A bacteria colony grows by a factor of x^{m} in the first generation and x^{n} in the second generation. When you multiply these growth factors together, what is the combined growth factor? (Express as x^? - provide the exponent)",
                f"A data compression algorithm processes blocks of size x^{m} units. If you process x^{n} such operations sequentially and multiply the processing factors, what is the total processing factor? (Express as x^? - provide the exponent)",
                f"The energy output increases by x^{m} in phase 1 and x^{n} in phase 2. When these energy factors are multiplied together, what is the total energy increase factor? (Express as x^? - provide the exponent)"
            ]

            problem_text = templates[variant]

            return Problem(
                text=problem_text,
                operands=[m, n],
                operation='multiply_powers',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'template': 'word_problem_context',
                    'exponent1': m,
                    'exponent2': n,
                    'correct_answer': correct_answer,
                    'malrule_answer': malrule_answer,
                    'is_word_problem': True,
                    'word_problem_type': formula_type,
                    'word_problem_variant': variant
                }
            )

        elif formula_type == 'three_powers':
            # Formula: x^a × x^b × x^c
            ranges = self.get_value_ranges()
            a = random.randint(*ranges['exponent'])
            b = random.randint(*ranges['exponent'])
            c = random.randint(*ranges['exponent'])

            # Ensure a+b+c ≠ a×b×c
            max_attempts = 10
            attempts = 0
            while (a + b + c == a * b * c) and attempts < max_attempts:
                c = random.randint(*ranges['exponent'])
                attempts += 1

            correct_answer = a + b + c
            malrule_answer = a * b * c

            templates = [
                f"A bacterial culture multiplies by x^{a} in morning, x^{b} in afternoon, and x^{c} in evening. When all three growth factors are multiplied, what is the total daily growth factor? (Express as x^? - provide the exponent)",
                f"Three data processing stages have efficiency factors of x^{a}, x^{b}, and x^{c} respectively. When these factors are multiplied together, what is the combined efficiency? (Express as x^? - provide the exponent)",
                f"A chain reaction has three stages with amplification factors x^{a}, x^{b}, and x^{c}. What is the total amplification when all stages are multiplied? (Express as x^? - provide the exponent)"
            ]

            problem_text = templates[variant]

            return Problem(
                text=problem_text,
                operands=[a, b, c],
                operation='multiply_powers',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'template': 'word_problem_context',
                    'exponent1': a,
                    'exponent2': b,
                    'exponent3': c,
                    'correct_answer': correct_answer,
                    'malrule_answer': malrule_answer,
                    'is_word_problem': True,
                    'word_problem_type': formula_type,
                    'word_problem_variant': variant
                }
            )

        elif formula_type == 'numerical_base':
            # Formula: base^m × base^n
            ranges = self.get_value_ranges()
            m = random.randint(*ranges['exponent'])
            n = random.randint(*ranges['exponent'])

            # Use base 2 or 3
            base = random.choice([2, 3])

            correct_answer = base ** (m + n)
            malrule_answer = base ** (m * n)

            templates = [
                f"A server farm has {base}^{m} servers in building A and {base}^{n} servers in building B. If the total number of servers follows the pattern {base}^{{total}}, calculate the total number of servers.",
                f"A computer memory system has {base}^{m} blocks in cache 1 and {base}^{n} blocks in cache 2. When combined multiplicatively, calculate the total memory blocks (evaluate {base}^m × {base}^n).",
                f"A binary tree has {base}^{m} nodes at level 1 and continues growing. After {n} more doublings (represented as {base}^{n}), calculate the total nodes (evaluate {base}^m × {base}^n)."
            ]

            problem_text = templates[variant]

            return Problem(
                text=problem_text,
                operands=[base, m, n],
                operation='multiply_powers',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'template': 'word_problem_context',
                    'base': base,
                    'exponent1': m,
                    'exponent2': n,
                    'correct_answer': correct_answer,
                    'correct_exponent': m + n,
                    'malrule_answer': malrule_answer,
                    'malrule_exponent': m * n,
                    'is_word_problem': True,
                    'word_problem_type': formula_type,
                    'word_problem_variant': variant
                }
            )

        else:  # mixed_operations
            # Formula: x^a × x^b ÷ x^c
            ranges = self.get_value_ranges()

            # Retry until we find values where correct != malrule
            max_attempts = 100
            for attempt in range(max_attempts):
                a = random.randint(*ranges['exponent'])
                b = random.randint(*ranges['exponent'])
                c = random.randint(2, min(ranges['exponent'][1], a + b - 1))

                correct_answer = a + b - c
                malrule_answer = (a * b) // c if (a * b) % c == 0 else (a * b) / c

                # Ensure correct != malrule
                if correct_answer != malrule_answer:
                    break

            # If we couldn't find a good case, use a known good case
            if correct_answer == malrule_answer:
                a, b, c = 3, 5, 2  # 3+5-2=6 vs (3*5)/2=7.5
                correct_answer = a + b - c
                malrule_answer = (a * b) / c

            templates = [
                f"A population grows by x^{a} in spring and x^{b} in summer, then decreases by a factor of x^{c} in fall. Using multiplication for growth and division for decrease, what is the net population change? (Express as x^? - provide the exponent)",
                f"A machine's efficiency is multiplied by x^{a}, then by x^{b}, then divided by x^{c}. What is the final efficiency factor? (Express as x^? - provide the exponent)",
                f"Signal strength amplifies by x^{a}, then x^{b}, then attenuates by x^{c}. Calculate the net signal change. (Express as x^? - provide the exponent)"
            ]

            problem_text = templates[variant]

            return Problem(
                text=problem_text,
                operands=[a, b, c],
                operation='multiply_powers',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'template': 'word_problem_context',
                    'exponent1': a,
                    'exponent2': b,
                    'exponent3': c,
                    'correct_answer': correct_answer,
                    'malrule_answer': malrule_answer,
                    'is_word_problem': True,
                    'word_problem_type': formula_type,
                    'word_problem_variant': variant
                }
            )
