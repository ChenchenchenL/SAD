"""
Malrule algorithm for Right-Align-Decimals error.

Students align decimal numbers by the rightmost digit instead of
by the decimal point, treating them like whole numbers.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import Dict, List, Any
from utils import Malrule, Problem, Solution

class RightAlignDecimalsMalrule(Malrule):
    """
    Implements the Right-Align-Decimals malrule.

    Students align decimals by rightmost digit (like whole numbers)
    instead of by the decimal point.

    Example: 3.5 + 2.75
    Correct alignment:    3.5
                        + 2.75
                        ------
                          6.25

    Malrule alignment:    3.5
                          2.75  (rightmost digits aligned)
                        -----
                          6.0   (WRONG!)
    """

    def get_name(self) -> str:
        return "Right-Align-Decimals"

    def get_description(self) -> str:
        return (
            "Students align decimal numbers by the rightmost digit instead of by the "
            "decimal point when performing addition or subtraction. This error stems "
            "from overgeneralizing whole number alignment procedures where right-alignment "
            "is correct. Hiebert & Wearne (1985) found that students compute by relying "
            "on syntax-based rules without semantic understanding of place value."
        )

    def calculate_expected_answer(self, problem: Problem) -> str:
        """
        Calculate the expected incorrect answer for this malrule.

        For Right-Align-Decimals:
        - Student aligns numbers by rightmost digit (like whole numbers)
        - MALRULE: Removes decimal points, right-aligns as integers, operates, replaces decimal

        Example: 3.5 + 2.75
        - Remove decimals: "35" and "275"
        - Right-align: "035" and "275"
        - Add: 35 + 275 = 310
        - Replace decimal (min decimal places = 1): "31.0" → 31.0

        Args:
            problem: Decimal addition/subtraction problem

        Returns:
            Expected incorrect answer as string
        """
        # Check if this is a three-number operation
        if 'num3' in problem.metadata:
            # Handle three-number operation (e.g., a + b - c)
            num1 = problem.metadata['num1']
            num2 = problem.metadata['num2']
            num3 = problem.metadata['num3']

            # Step 1: num1 + num2 with malrule
            num1_str = str(num1)
            num2_str = str(num2)

            num1_no_decimal = num1_str.replace('.', '')
            num2_no_decimal = num2_str.replace('.', '')

            if len(num1_no_decimal) >= len(num2_no_decimal):
                num2_padded = num2_no_decimal.zfill(len(num1_no_decimal))
                num1_padded = num1_no_decimal
            else:
                num1_padded = num1_no_decimal.zfill(len(num2_no_decimal))
                num2_padded = num2_no_decimal

            val1 = int(num1_padded)
            val2 = int(num2_padded)
            result_int = val1 + val2

            # Put decimal back
            decimal_places_12 = min(
                problem.metadata['num1_decimal_places'],
                problem.metadata['num2_decimal_places']
            )
            result_str = str(result_int)
            if decimal_places_12 > 0 and len(result_str) > decimal_places_12:
                insert_pos = len(result_str) - decimal_places_12
                temp_result_str = result_str[:insert_pos] + '.' + result_str[insert_pos:]
                temp_result = float(temp_result_str)
            else:
                temp_result = float(result_int)

            # Step 2: temp_result - num3 with malrule
            temp_result_str = str(temp_result)
            num3_str = str(num3)

            temp_no_decimal = temp_result_str.replace('.', '')
            num3_no_decimal = num3_str.replace('.', '')

            if len(temp_no_decimal) >= len(num3_no_decimal):
                num3_padded = num3_no_decimal.zfill(len(temp_no_decimal))
                temp_padded = temp_no_decimal
            else:
                temp_padded = temp_no_decimal.zfill(len(num3_no_decimal))
                num3_padded = num3_no_decimal

            val_temp = int(temp_padded)
            val3 = int(num3_padded)
            final_result_int = abs(val_temp - val3)

            # Put decimal back
            temp_decimal_places = len(temp_result_str.split('.')[1]) if '.' in temp_result_str else 0
            num3_decimal_places = problem.metadata['num3_decimal_places']
            decimal_places_final = min(temp_decimal_places, num3_decimal_places)

            final_result_str = str(final_result_int)
            if decimal_places_final > 0 and len(final_result_str) > decimal_places_final:
                insert_pos = len(final_result_str) - decimal_places_final
                final_with_decimal = final_result_str[:insert_pos] + '.' + final_result_str[insert_pos:]
                final_result = float(final_with_decimal)
            else:
                final_result = float(final_result_int)

            return str(final_result)

        # Calculate malrule answer from problem data (NOT from metadata)
        num1 = problem.metadata['num1']
        num2 = problem.metadata['num2']
        op_symbol = problem.metadata['operation_symbol']

        # Get string representations
        num1_str = str(num1)
        num2_str = str(num2)

        # Remove decimal points and treat as whole numbers
        num1_no_decimal = num1_str.replace('.', '')
        num2_no_decimal = num2_str.replace('.', '')

        # Right-align them (like whole numbers)
        if len(num1_no_decimal) >= len(num2_no_decimal):
            # Pad num2 on left
            num2_padded = num2_no_decimal.zfill(len(num1_no_decimal))
            num1_padded = num1_no_decimal
        else:
            # Pad num1 on left
            num1_padded = num1_no_decimal.zfill(len(num2_no_decimal))
            num2_padded = num2_no_decimal

        # Convert back to integers for calculation
        val1 = int(num1_padded)
        val2 = int(num2_padded)

        if op_symbol == '+':
            result_int = val1 + val2
        else:
            result_int = abs(val1 - val2)  # Student might take absolute value

        # Put decimal point back (incorrectly)
        # Count decimal places
        num1_decimal_places = len(num1_str.split('.')[1]) if '.' in num1_str else 0
        num2_decimal_places = len(num2_str.split('.')[1]) if '.' in num2_str else 0
        decimal_places = min(num1_decimal_places, num2_decimal_places)

        result_str = str(result_int)

        if decimal_places > 0 and len(result_str) > decimal_places:
            insert_pos = len(result_str) - decimal_places
            result_with_decimal = result_str[:insert_pos] + '.' + result_str[insert_pos:]
            return result_with_decimal
        else:
            return str(float(result_int))

    def _generate_verbose_steps(self, problem: Problem, num1: float, num2: float,
                                 op_symbol: str, malrule_answer: str,
                                 is_word_problem: bool, word_problem_type: str) -> List[str]:
        """Generate verbose, explanatory steps."""
        steps = []

        # For word problems, show extraction step
        if is_word_problem:
            steps.append(f"Word Problem: {problem.text}")
            steps.append("")
            steps.append("Step 1: Extract the equation from the word problem")
            steps.append(f"  Equation: {num1} {op_symbol} {num2}")
            steps.append("")
            steps.append("Step 2: Apply malrule (align by rightmost digit)")
            steps.append("")
        else:
            steps.append(f"Problem: {num1} {op_symbol} {num2}")
            steps.append("")

        # Get string representations
        num1_str = str(num1)
        num2_str = str(num2)

        steps.append("MALRULE: Align by rightmost digit (like whole numbers)")
        steps.append(f"  MALRULE REASONING: 'Stack numbers with right ends aligned'")
        steps.append(f"  (WRONG! Must align by decimal point!)")
        steps.append("")

        # Demonstrate the wrong alignment visually
        steps.append("Step 1: Align by right end")
        if len(num1_str) >= len(num2_str):
            padding = len(num1_str) - len(num2_str)
            steps.append(f"  {num1_str}")
            steps.append(f"  {' ' * padding}{num2_str}")
        else:
            padding = len(num2_str) - len(num1_str)
            steps.append(f"  {' ' * padding}{num1_str}")
            steps.append(f"  {num2_str}")
        steps.append("")

        # Now compute with wrong alignment
        # Remove decimal points and treat as whole numbers
        num1_no_decimal = num1_str.replace('.', '')
        num2_no_decimal = num2_str.replace('.', '')

        # Right-align them (like whole numbers)
        if len(num1_no_decimal) >= len(num2_no_decimal):
            num2_padded = num2_no_decimal.zfill(len(num1_no_decimal))
            num1_padded = num1_no_decimal
        else:
            num1_padded = num1_no_decimal.zfill(len(num2_no_decimal))
            num2_padded = num2_no_decimal

        steps.append("Step 2: Operate on aligned digits")

        val1 = int(num1_padded)
        val2 = int(num2_padded)

        if op_symbol == '+':
            result_int = val1 + val2
            steps.append(f"  {val1} + {val2} = {result_int}")
        else:
            result_int = abs(val1 - val2)
            steps.append(f"  {val1} - {val2} = {result_int}")

        steps.append("")

        # Put decimal point back (incorrectly)
        decimal_places = min(
            problem.metadata['num1_decimal_places'],
            problem.metadata['num2_decimal_places']
        )

        result_str = str(result_int)
        if decimal_places > 0 and len(result_str) > decimal_places:
            insert_pos = len(result_str) - decimal_places
            result_with_decimal = result_str[:insert_pos] + '.' + result_str[insert_pos:]
            result = float(result_with_decimal)
            steps.append(f"Step 3: Place decimal point")
            steps.append(f"  Count {decimal_places} from right: {result}")
        else:
            result = float(result_int)
            steps.append(f"Step 3: Place decimal point")
            steps.append(f"  Result: {result}")

        steps.append("")
        steps.append(f"Final Answer: {malrule_answer} (INCORRECT - aligned by rightmost digit!)")

        return steps

    def _generate_concise_steps(self, problem: Problem, num1: float, num2: float,
                                 op_symbol: str, malrule_answer: str,
                                 is_word_problem: bool, word_problem_type: str) -> List[str]:
        """Generate concise steps with just formulas and values."""
        steps = [f"Problem: {problem.text}"]

        # For word problems, show extraction step
        if is_word_problem:
            steps.append(f"Equation: {num1} {op_symbol} {num2}")

        # Get string representations
        num1_str = str(num1)
        num2_str = str(num2)

        # Remove decimal points
        num1_no_decimal = num1_str.replace('.', '')
        num2_no_decimal = num2_str.replace('.', '')

        # Right-align them
        if len(num1_no_decimal) >= len(num2_no_decimal):
            num2_padded = num2_no_decimal.zfill(len(num1_no_decimal))
            num1_padded = num1_no_decimal
        else:
            num1_padded = num1_no_decimal.zfill(len(num2_no_decimal))
            num2_padded = num2_no_decimal

        val1 = int(num1_padded)
        val2 = int(num2_padded)

        steps.append(f"Right-align: {val1}, {val2}")

        if op_symbol == '+':
            result_int = val1 + val2
            steps.append(f"{val1} + {val2} = {result_int}")
        else:
            result_int = abs(val1 - val2)
            steps.append(f"{val1} - {val2} = {result_int}")

        steps.append(malrule_answer)

        return steps

    def _generate_verbose_steps_three_numbers(self, problem: Problem, num1: float, num2: float,
                                               num3: float, malrule_answer: str,
                                               is_word_problem: bool, word_problem_type: str) -> List[str]:
        """Generate verbose steps for three-number operations."""
        steps = []

        # For word problems, show extraction step
        if is_word_problem:
            steps.append(f"Word Problem: {problem.text}")
            steps.append("")
            steps.append("Step 1: Extract the equation from the word problem")
            steps.append(f"  Equation: {num1} + {num2} - {num3}")
            steps.append("")
            steps.append("Step 2: Apply malrule (align by rightmost digit)")
            steps.append("")
        else:
            steps.append(f"Problem: {num1} + {num2} - {num3}")
            steps.append("")

        steps.append("MALRULE: Align by rightmost digit (like whole numbers)")
        steps.append(f"  MALRULE REASONING: 'Stack numbers with right ends aligned'")
        steps.append(f"  (WRONG! Must align by decimal point!)")
        steps.append("")

        # Step 1: First operation (num1 + num2) with malrule
        steps.append(f"Step 1: Calculate {num1} + {num2} (with malrule)")
        num1_str = str(num1)
        num2_str = str(num2)

        num1_no_decimal = num1_str.replace('.', '')
        num2_no_decimal = num2_str.replace('.', '')

        if len(num1_no_decimal) >= len(num2_no_decimal):
            num2_padded = num2_no_decimal.zfill(len(num1_no_decimal))
            num1_padded = num1_no_decimal
        else:
            num1_padded = num1_no_decimal.zfill(len(num2_no_decimal))
            num2_padded = num2_no_decimal

        val1 = int(num1_padded)
        val2 = int(num2_padded)
        result_int = val1 + val2

        decimal_places_12 = min(
            problem.metadata['num1_decimal_places'],
            problem.metadata['num2_decimal_places']
        )
        result_str = str(result_int)
        if decimal_places_12 > 0 and len(result_str) > decimal_places_12:
            insert_pos = len(result_str) - decimal_places_12
            temp_result_str = result_str[:insert_pos] + '.' + result_str[insert_pos:]
            temp_result = float(temp_result_str)
        else:
            temp_result = float(result_int)
            temp_result_str = str(temp_result)

        steps.append(f"  {val1} + {val2} = {result_int}")
        steps.append(f"  With decimal: {temp_result}")
        steps.append("")

        # Step 2: Second operation (temp_result - num3) with malrule
        steps.append(f"Step 2: Calculate {temp_result} - {num3} (with malrule)")
        temp_result_str = str(temp_result)
        num3_str = str(num3)

        temp_no_decimal = temp_result_str.replace('.', '')
        num3_no_decimal = num3_str.replace('.', '')

        if len(temp_no_decimal) >= len(num3_no_decimal):
            num3_padded = num3_no_decimal.zfill(len(temp_no_decimal))
            temp_padded = temp_no_decimal
        else:
            temp_padded = temp_no_decimal.zfill(len(num3_no_decimal))
            num3_padded = num3_no_decimal

        val_temp = int(temp_padded)
        val3 = int(num3_padded)
        final_result_int = abs(val_temp - val3)

        temp_decimal_places = len(temp_result_str.split('.')[1]) if '.' in temp_result_str else 0
        num3_decimal_places = problem.metadata['num3_decimal_places']
        decimal_places_final = min(temp_decimal_places, num3_decimal_places)

        final_result_str = str(final_result_int)
        if decimal_places_final > 0 and len(final_result_str) > decimal_places_final:
            insert_pos = len(final_result_str) - decimal_places_final
            final_with_decimal = final_result_str[:insert_pos] + '.' + final_result_str[insert_pos:]
            final_result = float(final_with_decimal)
        else:
            final_result = float(final_result_int)

        steps.append(f"  {val_temp} - {val3} = {final_result_int}")
        steps.append(f"  With decimal: {final_result}")
        steps.append("")
        steps.append(f"Final Answer: {malrule_answer} (INCORRECT - aligned by rightmost digit!)")

        return steps

    def _generate_concise_steps_three_numbers(self, problem: Problem, num1: float, num2: float,
                                               num3: float, malrule_answer: str,
                                               is_word_problem: bool, word_problem_type: str) -> List[str]:
        """Generate concise steps for three-number operations."""
        steps = [f"Problem: {problem.text}"]

        # For word problems, show extraction step
        if is_word_problem:
            steps.append(f"Equation: {num1} + {num2} - {num3}")

        steps.append(f"Right-align: {num1}, {num2}, {num3}")
        steps.append(f"{num1} + {num2} - {num3}")
        steps.append(f"= {malrule_answer}")
        steps.append(malrule_answer)

        return steps

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the right-align-decimals malrule.

        Student aligns numbers by rightmost digit, ignoring decimal points.

        Args:
            problem: Problem instance with decimal numbers
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with incorrect answer and student's reasoning
        """
        # Check if this is a word problem
        is_word_problem = problem.metadata.get('is_word_problem', False)
        word_problem_type = problem.metadata.get('word_problem_type', None)

        # Check if this is a three-number operation
        if 'num3' in problem.metadata:
            return self._apply_malrule_three_numbers(problem, verbose)

        num1 = problem.metadata['num1']
        num2 = problem.metadata['num2']
        op_symbol = problem.metadata['operation_symbol']

        # Calculate malrule answer
        malrule_answer = self.calculate_expected_answer(problem)

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(problem, num1, num2, op_symbol, malrule_answer,
                                                  is_word_problem, word_problem_type)
        else:
            steps = self._generate_concise_steps(problem, num1, num2, op_symbol, malrule_answer,
                                                  is_word_problem, word_problem_type)

        return Solution(
            answer=str(malrule_answer),
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _apply_malrule_three_numbers(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply malrule for three-number operations (e.g., a + b - c).

        Args:
            problem: Problem instance with three decimal numbers
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution with incorrect answer and student's reasoning
        """
        # Check if this is a word problem
        is_word_problem = problem.metadata.get('is_word_problem', False)
        word_problem_type = problem.metadata.get('word_problem_type', None)

        num1 = problem.metadata['num1']
        num2 = problem.metadata['num2']
        num3 = problem.metadata['num3']

        # Calculate malrule answer
        malrule_answer = self.calculate_expected_answer(problem)

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps_three_numbers(problem, num1, num2, num3,
                                                                malrule_answer, is_word_problem,
                                                                word_problem_type)
        else:
            steps = self._generate_concise_steps_three_numbers(problem, num1, num2, num3,
                                                                malrule_answer, is_word_problem,
                                                                word_problem_type)

        return Solution(
            answer=str(malrule_answer),
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
