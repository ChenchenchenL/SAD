"""
Correct algorithm for multi-digit multiplication with carrying.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import CorrectAlgorithm, Problem, Solution


class MultiDigitMultiplicationCorrectAlgorithm(CorrectAlgorithm):
    """Correctly multiplies multi-digit numbers with proper carrying."""

    def get_name(self):
        return "Correct Multi-Digit Multiplication"

    def get_description(self):
        return "Multiplies multi-digit numbers by adding carried values correctly"

    def _generate_concise_steps(self, problem: Problem, correct_answer: str) -> list:
        """Generate concise steps with only formula and values."""
        template = problem.metadata.get('template', 'basic_two_digit_times_one')
        steps = []
        steps.append(f"Question: {problem.text}")

        if template == 'three_digit_times_one':
            multiplicand = problem.metadata['multiplicand']
            multiplier = problem.metadata['multiplier']
            hundreds_digit = problem.metadata['hundreds_digit']
            tens_digit = problem.metadata['tens_digit']
            ones_digit = problem.metadata['ones_digit']
            ones_product = problem.metadata['ones_product']
            carry_to_tens = problem.metadata['carry_to_tens']
            tens_product = problem.metadata['tens_product']
            tens_with_carry = problem.metadata['tens_with_carry']
            carry_to_hundreds = problem.metadata['carry_to_hundreds']

            steps.append(f"{multiplicand} × {multiplier}")
            steps.append(f"{ones_digit} × {multiplier} = {ones_product}")
            steps.append(f"{tens_digit} × {multiplier} + {carry_to_tens} = {tens_with_carry}")
            steps.append(f"{hundreds_digit} × {multiplier} + {carry_to_hundreds} = {correct_answer}")

        elif template in ['two_digit_times_two', 'three_digit_times_two']:
            num1 = problem.metadata['num1']
            num2 = problem.metadata['num2']
            ones2 = problem.metadata['ones2']
            tens2 = problem.metadata.get('tens2', num2 // 10)
            partial_product_1 = problem.metadata['partial_product_1']
            partial_product_2 = problem.metadata['partial_product_2']

            steps.append(f"{num1} × {num2}")
            steps.append(f"{num1} × {ones2} = {partial_product_1}")
            steps.append(f"{num1} × {tens2} = {partial_product_2}")
            steps.append(f"{partial_product_1} + {partial_product_2}0 = {correct_answer}")

        elif template in ['money_context', 'word_problem', 'area_calculation', 'total_cost_bulk', 'distance_calculation', 'array_larger']:
            multiplicand = problem.metadata.get('multiplicand', problem.operands[0])
            multiplier = problem.metadata.get('multiplier', problem.operands[1] if len(problem.operands) > 1 else problem.metadata['multiplier'])
            tens_digit = problem.metadata['tens_digit']
            ones_digit = problem.metadata['ones_digit']
            ones_product = problem.metadata['ones_product']
            carry = problem.metadata['carry']
            tens_product = problem.metadata['tens_product']

            steps.append(f"{multiplicand} × {multiplier}")
            steps.append(f"{ones_digit} × {multiplier} = {ones_product}")
            steps.append(f"{tens_digit} × {multiplier} + {carry} = {tens_product + carry}")

        else:  # basic_two_digit_times_one or legacy
            multiplicand = problem.metadata.get('multiplicand', problem.operands[0])
            multiplier = problem.metadata.get('multiplier', problem.operands[1] if len(problem.operands) > 1 else problem.metadata.get('multiplier', problem.operands[0]))
            tens_digit = problem.metadata['tens_digit']
            ones_digit = problem.metadata['ones_digit']
            ones_product = problem.metadata['ones_product']
            carry = problem.metadata['carry']
            tens_product = problem.metadata['tens_product']
            tens_with_carry = problem.metadata.get('tens_with_carry', tens_product + carry)

            steps.append(f"{multiplicand} × {multiplier}")
            steps.append(f"{ones_digit} × {multiplier} = {ones_product}")
            steps.append(f"{tens_digit} × {multiplier} + {carry} = {tens_with_carry}")

        steps.append(f"Answer: {correct_answer}")
        return steps

    def _generate_verbose_steps(self, problem: Problem, correct_answer: str) -> list:
        """Generate verbose steps with full explanations."""
        template = problem.metadata.get('template', 'basic_two_digit_times_one')
        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("CORRECT METHOD: Multiply each place and add carries")
        steps.append("")

        if template == 'three_digit_times_one':
            multiplicand = problem.metadata['multiplicand']
            multiplier = problem.metadata['multiplier']
            hundreds_digit = problem.metadata['hundreds_digit']
            tens_digit = problem.metadata['tens_digit']
            ones_digit = problem.metadata['ones_digit']
            ones_product = problem.metadata['ones_product']
            ones_result = problem.metadata['ones_result']
            carry_to_tens = problem.metadata['carry_to_tens']
            tens_product = problem.metadata['tens_product']
            tens_with_carry = problem.metadata['tens_with_carry']
            carry_to_hundreds = problem.metadata['carry_to_hundreds']

            steps.append(f"Step 1: Multiply ones: {ones_digit} × {multiplier} = {ones_product}")
            steps.append(f"  Write {ones_result}, carry {carry_to_tens}")
            steps.append("")
            steps.append(f"Step 2: Multiply tens: {tens_digit} × {multiplier} = {tens_product}")
            steps.append(f"  Add carry: {tens_product} + {carry_to_tens} = {tens_with_carry}")
            steps.append(f"  Write {tens_with_carry % 10}, carry {carry_to_hundreds}")
            steps.append("")
            steps.append(f"Step 3: Multiply hundreds: {hundreds_digit} × {multiplier}")
            steps.append(f"  Add carry: {hundreds_digit * multiplier} + {carry_to_hundreds}")
            steps.append(f"  = {correct_answer}")

        elif template in ['two_digit_times_two', 'three_digit_times_two']:
            num1 = problem.metadata['num1']
            num2 = problem.metadata['num2']
            ones2 = problem.metadata['ones2']
            tens2 = problem.metadata.get('tens2', num2 // 10)
            partial_product_1 = problem.metadata['partial_product_1']
            partial_product_2 = problem.metadata['partial_product_2']
            pp1_carry = problem.metadata.get('pp1_carry', problem.metadata.get('pp1_carry_to_tens', 0))

            steps.append(f"Step 1: Multiply {num1} × {ones2} (ones digit)")
            steps.append(f"  Partial product 1: {partial_product_1}")
            steps.append(f"  (Remember to add carry {pp1_carry} correctly)")
            steps.append("")
            steps.append(f"Step 2: Multiply {num1} × {tens2} (tens digit)")
            steps.append(f"  Partial product 2: {partial_product_2} (shifted left)")
            steps.append("")
            steps.append(f"Step 3: Add partial products:")
            steps.append(f"  {partial_product_1} + {partial_product_2}0 = {correct_answer}")

        elif template in ['money_context', 'word_problem', 'area_calculation', 'total_cost_bulk', 'distance_calculation', 'array_larger']:
            multiplicand = problem.metadata.get('multiplicand', problem.operands[0])
            multiplier = problem.metadata.get('multiplier', problem.operands[1] if len(problem.operands) > 1 else problem.metadata['multiplier'])
            tens_digit = problem.metadata['tens_digit']
            ones_digit = problem.metadata['ones_digit']
            ones_product = problem.metadata['ones_product']
            ones_result = problem.metadata['ones_result']
            carry = problem.metadata['carry']
            tens_product = problem.metadata['tens_product']

            steps.append(f"Step 1: Multiply ones place: {ones_digit} × {multiplier} = {ones_product}")
            steps.append(f"  Write {ones_result}, carry {carry}")
            steps.append("")
            steps.append(f"Step 2: Multiply tens place: {tens_digit} × {multiplier} = {tens_product}")
            steps.append(f"  ADD the carry: {tens_product} + {carry} = {tens_product + carry}")
            steps.append("")
            steps.append(f"Answer: {correct_answer}")

        else:  # basic_two_digit_times_one or legacy
            multiplicand = problem.metadata.get('multiplicand', problem.operands[0])
            multiplier = problem.metadata.get('multiplier', problem.operands[1] if len(problem.operands) > 1 else problem.metadata.get('multiplier', problem.operands[0]))
            tens_digit = problem.metadata['tens_digit']
            ones_digit = problem.metadata['ones_digit']
            ones_product = problem.metadata['ones_product']
            ones_result = problem.metadata['ones_result']
            carry = problem.metadata['carry']
            tens_product = problem.metadata['tens_product']
            tens_with_carry = problem.metadata.get('tens_with_carry', tens_product + carry)

            steps.append("Step 1: Multiply ones place")
            steps.append(f"  {ones_digit} × {multiplier} = {ones_product}")
            steps.append(f"  Write {ones_result} in ones place")
            steps.append(f"  Carry {carry} to tens place")
            steps.append("")
            steps.append("Step 2: Multiply tens place")
            steps.append(f"  {tens_digit} × {multiplier} = {tens_product}")
            steps.append("")
            steps.append("Step 3: ADD the carried value")
            steps.append(f"  {tens_product} + {carry} (carry) = {tens_with_carry}")
            steps.append(f"  Write {tens_with_carry} in tens/hundreds place")
            steps.append("")
            steps.append("Step 4: Combine results")
            steps.append(f"  Answer: {correct_answer}")

        steps.append("")
        steps.append("Verification:")
        steps.append(f"  {correct_answer} ✓")
        steps.append("")
        steps.append(
            "The key is remembering to ADD the carried value to the next place "
            "product. This is the regrouping step that students often forget."
        )

        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply correct multi-digit multiplication algorithm.

        Args:
            problem: The multiplication problem
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution showing correct multiplication with carrying
        """
        # Compute answer (never use metadata['correct_answer'])
        correct_answer = str(problem.operands[0] * problem.operands[1])

        if verbose:
            steps = self._generate_verbose_steps(problem, correct_answer)
        else:
            steps = self._generate_concise_steps(problem, correct_answer)

        return Solution(
            answer=str(correct_answer),
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
