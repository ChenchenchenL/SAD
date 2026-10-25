"""
Problem generator for Decompose-By-Place-Value-Label malrule.

Generates place value decomposition problems where students must write
the number represented by a decomposition like "2 hundreds 13 tens 1 ones".
"""

import random
from typing import Dict, Tuple, Optional, List
import sys
sys.path.append('/home/user/malrule-coding')

from utils import Problem, ProblemGenerator, DifficultyLevel


class DecomposeByPlaceValueLabelProblemGenerator(ProblemGenerator):
    """
    Generates place value decomposition problems with regrouped values.

    The malrule triggers when students see decompositions like
    "2 hundreds 13 tens 1 ones" and write 2131 instead of 331.

    Templates:
    1. basic_regrouped_tens - Tens > 9 ("2 hundreds 13 tens 1 ones")
    2. regrouped_ones - Ones > 9 ("3 tens 12 ones")
    3. multiple_regroupings - Both tens and ones > 9
    4. four_digit - Extends to thousands place
    5. word_problem - Real-world base-10 block contexts
    """

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        return [
            'basic_regrouped_tens',
            'regrouped_ones',
            'multiple_regroupings',
            'four_digit',
            'word_problem'
        ]

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        """Get appropriate value ranges based on level and difficulty."""
        ranges = {
            2: {
                DifficultyLevel.EASY: (10, 50),      # Small 2-digit decompositions
                DifficultyLevel.MEDIUM: (20, 80),    # Larger 2-digit
                DifficultyLevel.HARD: (40, 99),      # 2-digit with regrouping
            },
            3: {
                DifficultyLevel.EASY: (100, 300),    # 3-digit simple
                DifficultyLevel.MEDIUM: (200, 500),  # 3-digit with regrouping
                DifficultyLevel.HARD: (400, 999),    # 3-digit complex
            },
            4: {
                DifficultyLevel.EASY: (100, 400),    # 3-digit
                DifficultyLevel.MEDIUM: (500, 999),  # 3-digit complex
                DifficultyLevel.HARD: (1000, 9999),  # 4-digit
            }
        }

        # Default to level 3 if not in ranges
        lvl = self.level if self.level in ranges else 3
        return {'value': ranges[lvl][self.difficulty]}

    def _create_regrouped_decomposition(self, target_value: int) -> Tuple[int, int, int, int]:
        """
        Create a place value decomposition with regrouped tens/hundreds.

        For example, 331 could be decomposed as:
        - 3 hundreds 3 tens 1 ones (normal)
        - 2 hundreds 13 tens 1 ones (regrouped - borrowed 1 hundred)
        - 3 hundreds 2 tens 11 ones (regrouped - borrowed 1 ten)

        Args:
            target_value: The actual number to represent

        Returns:
            Tuple of (thousands, hundreds, tens, ones) in the decomposition
        """
        # Get the standard decomposition first
        thousands = target_value // 1000
        hundreds = (target_value % 1000) // 100
        tens = (target_value % 100) // 10
        ones = target_value % 10

        # Decide what to regroup (we want to create opportunities for the malrule)
        regroup_choice = random.choice(['tens', 'ones', 'both'])

        if target_value >= 100 and regroup_choice in ['tens', 'both']:
            # Regroup 1 hundred as 10 tens (if possible)
            if hundreds > 0:
                hundreds -= 1
                tens += 10

        if target_value >= 10 and regroup_choice in ['ones', 'both'] and random.random() < 0.5:
            # Regroup 1 ten as 10 ones (if possible)
            if tens > 0:
                tens -= 1
                ones += 10

        return thousands, hundreds, tens, ones

    def generate(self, seed: Optional[int] = None, template: Optional[str] = None) -> Problem:
        """
        Generate a problem based on selected template.

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
        if template == 'basic_regrouped_tens':
            return self._generate_basic_regrouped_tens(seed)
        elif template == 'regrouped_ones':
            return self._generate_regrouped_ones(seed)
        elif template == 'multiple_regroupings':
            return self._generate_multiple_regroupings(seed)
        elif template == 'four_digit':
            return self._generate_four_digit(seed)
        elif template == 'word_problem':
            return self._generate_word_problem(seed)
        else:
            raise ValueError(f"Unknown template: {template}")

    def _generate_basic_regrouped_tens(self, seed=None) -> Problem:
        """Generate basic problem with regrouped tens (tens > 9)."""
        if seed is not None:
            random.seed(seed)

        # Create a 3-digit number
        # Start hundreds at 2+ to ensure it stays >= 1 after regrouping
        # This avoids edge cases where malrule produces same answer
        # (when hundreds=0, tens=10-19, ones=0-9, concatenation equals correct value)
        hundreds = random.randint(2, 5)
        tens = random.randint(1, 9)
        ones = random.randint(1, 9)

        # Regroup: borrow 1 hundred as 10 tens
        hundreds -= 1
        tens += 10

        # Calculate answers
        target_value = hundreds * 100 + tens * 10 + ones
        malrule_answer = str(hundreds) + str(tens) + str(ones)

        # Build decomposition text
        parts = []
        if hundreds > 0:
            parts.append(f"{hundreds} hundred{'s' if hundreds != 1 else ''}")
        parts.append(f"{tens} tens")
        parts.append(f"{ones} one{'s' if ones != 1 else ''}")

        decomposition_text = " ".join(parts)

        return Problem(
            text=f"What number is represented by {decomposition_text}?",
            operands=[0, hundreds, tens, ones],
            operation='place_value_decomposition',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'thousands': 0,
                'hundreds': hundreds,
                'tens': tens,
                'ones': ones,
                'target_value': target_value,
                'correct_answer': str(target_value),
                'malrule_answer': malrule_answer,
                'has_regrouping': True,
                'template': 'basic_regrouped_tens'
            }
        )

    def _generate_regrouped_ones(self, seed=None) -> Problem:
        """Generate problem with regrouped ones (ones > 9)."""
        if seed is not None:
            random.seed(seed)

        # Create a 2-digit number
        tens = random.randint(2, 7)
        ones = random.randint(1, 9)

        # Regroup: borrow 1 ten as 10 ones
        if tens > 0:
            tens -= 1
            ones += 10

        # Calculate answers
        target_value = tens * 10 + ones
        malrule_answer = str(tens) + str(ones)

        # Build decomposition text
        parts = []
        if tens > 0:
            parts.append(f"{tens} tens")
        parts.append(f"{ones} ones")

        decomposition_text = " ".join(parts)

        return Problem(
            text=f"What number is represented by {decomposition_text}?",
            operands=[0, 0, tens, ones],
            operation='place_value_decomposition',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'thousands': 0,
                'hundreds': 0,
                'tens': tens,
                'ones': ones,
                'target_value': target_value,
                'correct_answer': str(target_value),
                'malrule_answer': malrule_answer,
                'has_regrouping': True,
                'template': 'regrouped_ones'
            }
        )

    def _generate_multiple_regroupings(self, seed=None) -> Problem:
        """Generate problem with both tens and ones regrouped."""
        if seed is not None:
            random.seed(seed)

        # Create a 3-digit number
        hundreds = random.randint(2, 5)
        tens = random.randint(2, 7)
        ones = random.randint(2, 7)

        # Regroup both: borrow 1 hundred to tens, 1 ten to ones
        hundreds -= 1
        tens += 10
        tens -= 1
        ones += 10

        # Calculate answers
        target_value = hundreds * 100 + tens * 10 + ones
        malrule_answer = str(hundreds) + str(tens) + str(ones)

        # Build decomposition text
        parts = []
        if hundreds > 0:
            parts.append(f"{hundreds} hundred{'s' if hundreds != 1 else ''}")
        parts.append(f"{tens} tens")
        parts.append(f"{ones} ones")

        decomposition_text = " ".join(parts)

        return Problem(
            text=f"What number is represented by {decomposition_text}?",
            operands=[0, hundreds, tens, ones],
            operation='place_value_decomposition',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'thousands': 0,
                'hundreds': hundreds,
                'tens': tens,
                'ones': ones,
                'target_value': target_value,
                'correct_answer': str(target_value),
                'malrule_answer': malrule_answer,
                'has_regrouping': True,
                'template': 'multiple_regroupings'
            }
        )

    def _generate_four_digit(self, seed=None) -> Problem:
        """Generate 4-digit problem with thousands place."""
        if seed is not None:
            random.seed(seed)

        # Create a 4-digit number
        thousands = random.randint(1, 5)
        hundreds = random.randint(1, 7)
        tens = random.randint(1, 7)
        ones = random.randint(1, 9)

        # Regroup: borrow 1 thousand to hundreds
        if thousands > 0:
            thousands -= 1
            hundreds += 10

        # Calculate answers
        target_value = thousands * 1000 + hundreds * 100 + tens * 10 + ones

        # Build malrule answer by concatenating
        parts_for_concat = []
        if thousands > 0:
            parts_for_concat.append(str(thousands))
        parts_for_concat.append(str(hundreds))
        if tens > 0:
            parts_for_concat.append(str(tens))
        if ones > 0:
            parts_for_concat.append(str(ones))
        malrule_answer = ''.join(parts_for_concat)

        # Build decomposition text
        parts = []
        if thousands > 0:
            parts.append(f"{thousands} thousand{'s' if thousands != 1 else ''}")
        parts.append(f"{hundreds} hundreds")
        if tens > 0:
            parts.append(f"{tens} tens")
        if ones > 0:
            parts.append(f"{ones} one{'s' if ones != 1 else ''}")

        decomposition_text = " ".join(parts)

        return Problem(
            text=f"What number is represented by {decomposition_text}?",
            operands=[thousands, hundreds, tens, ones],
            operation='place_value_decomposition',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'thousands': thousands,
                'hundreds': hundreds,
                'tens': tens,
                'ones': ones,
                'target_value': target_value,
                'correct_answer': str(target_value),
                'malrule_answer': malrule_answer,
                'has_regrouping': True,
                'template': 'four_digit'
            }
        )

    def _generate_word_problem(self, seed=None) -> Problem:
        """Generate word problem with base-10 blocks context."""
        if seed is not None:
            random.seed(seed)

        # Create values with regrouping
        # Start hundreds at 2+ to ensure it stays >= 1 after regrouping
        # This avoids edge cases where malrule produces same answer
        hundreds = random.randint(2, 4)
        tens = random.randint(1, 6)
        ones = random.randint(1, 9)

        # Regroup hundreds to tens
        hundreds -= 1
        tens += 10

        # Calculate answers
        target_value = hundreds * 100 + tens * 10 + ones
        malrule_answer = str(hundreds) + str(tens) + str(ones)

        # Build word problem
        problem_text = (f"A student has base-10 blocks: {hundreds} hundred-blocks, "
                       f"{tens} ten-rods, and {ones} unit cubes. "
                       f"What number do these blocks represent?")

        return Problem(
            text=problem_text,
            operands=[0, hundreds, tens, ones],
            operation='place_value_decomposition',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'thousands': 0,
                'hundreds': hundreds,
                'tens': tens,
                'ones': ones,
                'target_value': target_value,
                'correct_answer': str(target_value),
                'malrule_answer': malrule_answer,
                'has_regrouping': True,
                'template': 'word_problem'
            }
        )
