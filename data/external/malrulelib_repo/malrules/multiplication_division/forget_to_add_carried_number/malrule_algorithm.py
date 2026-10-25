"""
Malrule algorithm for Forget-To-Add-Carried-Number.

Students forget to add the carried value when multiplying multi-digit numbers.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from utils import Malrule, Problem, Solution

class ForgetToAddCarriedNumberMalrule(Malrule):
    """Student forgets to add carried value in multiplication."""

    def get_name(self):
        return "Forget-To-Add-Carried-Number"

    def get_description(self):
        return (
            "A systematic procedural bug where students correctly multiply each digit but "
            "forget to add the carried (regrouped) value to the next place value. This was "
            "identified in Brown & Burton's (1978) BUGGY diagnostic system as one of the most "
            "common procedural bugs in arithmetic algorithms. For example, in 23 × 4, the student "
            "computes 3×4=12 (write 2, carry 1), then 2×4=8, but forgets to add the carried 1, "
            "yielding 82 instead of 92."
        )

    def calculate_expected_answer(self, problem: Problem):
        """Calculate the expected malrule answer (incorrect) for this problem."""
        template = problem.metadata.get('template', 'basic_two_digit_times_one')

        # For three-digit times one digit
        if template == 'three_digit_times_one' and 'hundreds_digit' in problem.metadata:
            # Malrule: forget carry from ones to tens
            ones_result = problem.metadata['ones_result']
            tens_product = problem.metadata['tens_product']
            hundreds_digit = problem.metadata['hundreds_digit']
            multiplier = problem.metadata['multiplier']

            tens_without_carry = tens_product  # Forgot the carry from ones
            malrule_tens_result = tens_without_carry % 10
            malrule_carry_to_hundreds = tens_without_carry // 10
            malrule_hundreds = hundreds_digit * multiplier + malrule_carry_to_hundreds
            return str(malrule_hundreds * 100 + malrule_tens_result * 10 + ones_result)

        # For two-digit × two-digit templates
        elif template == 'two_digit_times_two':
            num1 = problem.metadata['num1']
            num2 = problem.metadata['num2']
            ones1 = problem.metadata.get('ones1', num1 % 10)
            tens1 = problem.metadata.get('tens1', num1 // 10)
            ones2 = problem.metadata['ones2']
            tens2 = problem.metadata.get('tens2', num2 // 10)

            # Malrule: forget carry in first partial product (num1 × ones2)
            pp1_ones = ones1 * ones2
            pp1_ones_digit = pp1_ones % 10
            # Forget the carry here!
            malrule_pp1_tens = tens1 * ones2  # Missing the carry!
            malrule_pp1 = malrule_pp1_tens * 10 + pp1_ones_digit

            # Second partial product is computed correctly
            partial_product_2 = num1 * tens2

            return str(malrule_pp1 + partial_product_2 * 10)

        # For three-digit × two-digit templates
        elif template == 'three_digit_times_two':
            num1 = problem.metadata['num1']
            num2 = problem.metadata['num2']
            hundreds = problem.metadata.get('hundreds', num1 // 100)
            tens = problem.metadata.get('tens', (num1 // 10) % 10)
            ones = problem.metadata.get('ones', num1 % 10)
            ones2 = problem.metadata['ones2']
            tens2 = problem.metadata.get('tens2', num2 // 10)

            # First partial: num1 × ones2 with forgotten carry
            pp1_ones = ones * ones2
            pp1_ones_result = pp1_ones % 10
            # Forget carry from ones to tens!
            malrule_pp1_tens = tens * ones2  # Missing carry!
            malrule_pp1_tens_result = malrule_pp1_tens % 10
            malrule_pp1_carry = malrule_pp1_tens // 10
            malrule_pp1_hundreds = hundreds * ones2 + malrule_pp1_carry
            malrule_pp1 = malrule_pp1_hundreds * 100 + malrule_pp1_tens_result * 10 + pp1_ones_result

            # Second partial: num1 × tens2 (computed correctly, shifted)
            partial_product_2 = num1 * tens2

            return str(malrule_pp1 + partial_product_2 * 10)

        # For basic two-digit × one-digit templates
        elif 'tens_without_carry' in problem.metadata:
            ones_result = problem.metadata['ones_result']
            tens_without_carry = problem.metadata['tens_without_carry']
            return str(tens_without_carry * 10 + ones_result)

        # Fallback: compute algorithmically from operands
        else:
            # For two-digit × one-digit multiplication
            multiplicand = problem.operands[0]
            multiplier = problem.operands[1]

            tens_digit = multiplicand // 10
            ones_digit = multiplicand % 10

            ones_product = ones_digit * multiplier
            ones_result = ones_product % 10
            tens_product = tens_digit * multiplier
            # Malrule: forget carry
            malrule_answer = tens_product * 10 + ones_result
            return str(malrule_answer)

    def _generate_concise_steps(self, problem: Problem, malrule_answer: str) -> list:
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
            tens_product = problem.metadata['tens_product']

            steps.append(f"{multiplicand} × {multiplier}")
            steps.append(f"{ones_digit} × {multiplier} = {ones_product}")
            steps.append(f"{tens_digit} × {multiplier} = {tens_product}")
            steps.append(f"{hundreds_digit} × {multiplier} + {tens_product // 10} = {malrule_answer}")

        elif template == 'two_digit_times_two':
            num1 = problem.metadata['num1']
            num2 = problem.metadata['num2']
            ones1 = problem.metadata.get('ones1', num1 % 10)
            tens1 = problem.metadata.get('tens1', num1 // 10)
            ones2 = problem.metadata['ones2']
            tens2 = problem.metadata.get('tens2', num2 // 10)

            # Compute malrule partial products
            pp1_ones = ones1 * ones2
            pp1_ones_digit = pp1_ones % 10
            malrule_pp1_tens = tens1 * ones2  # Missing carry!
            malrule_pp1 = malrule_pp1_tens * 10 + pp1_ones_digit
            partial_product_2 = num1 * tens2

            steps.append(f"{num1} × {num2}")
            steps.append(f"{num1} × {ones2} = {malrule_pp1}")
            steps.append(f"{num1} × {tens2} = {partial_product_2}")
            steps.append(f"{malrule_pp1} + {partial_product_2}0 = {malrule_answer}")

        elif template == 'three_digit_times_two':
            num1 = problem.metadata['num1']
            num2 = problem.metadata['num2']
            hundreds = problem.metadata.get('hundreds', num1 // 100)
            tens = problem.metadata.get('tens', (num1 // 10) % 10)
            ones = problem.metadata.get('ones', num1 % 10)
            ones2 = problem.metadata['ones2']
            tens2 = problem.metadata.get('tens2', num2 // 10)

            # Compute malrule first partial product
            pp1_ones = ones * ones2
            pp1_ones_result = pp1_ones % 10
            malrule_pp1_tens = tens * ones2  # Missing carry!
            malrule_pp1_tens_result = malrule_pp1_tens % 10
            malrule_pp1_carry = malrule_pp1_tens // 10
            malrule_pp1_hundreds = hundreds * ones2 + malrule_pp1_carry
            malrule_pp1 = malrule_pp1_hundreds * 100 + malrule_pp1_tens_result * 10 + pp1_ones_result
            partial_product_2 = num1 * tens2

            steps.append(f"{num1} × {num2}")
            steps.append(f"{num1} × {ones2} = {malrule_pp1}")
            steps.append(f"{num1} × {tens2} = {partial_product_2}")
            steps.append(f"{malrule_pp1} + {partial_product_2}0 = {malrule_answer}")

        elif template in ['money_context', 'word_problem', 'area_calculation', 'total_cost_bulk', 'distance_calculation', 'array_larger']:
            multiplicand = problem.metadata.get('multiplicand', problem.operands[0])
            multiplier = problem.metadata.get('multiplier', problem.operands[1] if len(problem.operands) > 1 else problem.metadata['multiplier'])
            tens_digit = problem.metadata['tens_digit']
            ones_digit = problem.metadata['ones_digit']
            ones_product = problem.metadata['ones_product']
            tens_product = problem.metadata['tens_product']

            steps.append(f"{multiplicand} × {multiplier}")
            steps.append(f"{ones_digit} × {multiplier} = {ones_product}")
            steps.append(f"{tens_digit} × {multiplier} = {tens_product}")

        else:  # basic_two_digit_times_one
            multiplicand = problem.metadata.get('multiplicand', problem.operands[0])
            multiplier = problem.metadata.get('multiplier', problem.operands[1] if len(problem.operands) > 1 else problem.metadata.get('multiplier', problem.operands[0]))
            tens_digit = problem.metadata['tens_digit']
            ones_digit = problem.metadata['ones_digit']
            ones_product = problem.metadata['ones_product']
            tens_product = problem.metadata['tens_product']

            steps.append(f"{multiplicand} × {multiplier}")
            steps.append(f"{ones_digit} × {multiplier} = {ones_product}")
            steps.append(f"{tens_digit} × {multiplier} = {tens_product}")

        steps.append(f"Answer: {malrule_answer}")
        return steps

    def _generate_verbose_steps(self, problem: Problem, malrule_answer: str) -> list:
        """Generate verbose steps with full explanations."""
        template = problem.metadata.get('template', 'basic_two_digit_times_one')
        steps = []
        steps.append(f"Problem: {problem.text}")
        steps.append("")
        steps.append("MALRULE: Forget to add the carried value")
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

            steps.append(f"Step 1: Multiply ones place: {ones_digit} × {multiplier} = {ones_product}")
            steps.append(f"  Write {ones_result} in ones place, carry {carry_to_tens}")
            steps.append("")
            steps.append(f"Step 2: Multiply tens place: {tens_digit} × {multiplier} = {tens_product}")
            steps.append(f"  MALRULE: Student FORGETS to add carried {carry_to_tens}")
            steps.append(f"  (Should be: {tens_product} + {carry_to_tens} = {tens_product + carry_to_tens})")
            steps.append("")
            steps.append(f"Step 3: Continue with hundreds place...")

        elif template == 'two_digit_times_two':
            num1 = problem.metadata['num1']
            num2 = problem.metadata['num2']
            ones1 = problem.metadata.get('ones1', num1 % 10)
            tens1 = problem.metadata.get('tens1', num1 // 10)
            ones2 = problem.metadata['ones2']
            tens2 = problem.metadata.get('tens2', num2 // 10)

            # Compute values for explanation
            pp1_ones = ones1 * ones2
            pp1_ones_digit = pp1_ones % 10
            pp1_carry = pp1_ones // 10
            correct_pp1_tens = tens1 * ones2 + pp1_carry
            malrule_pp1_tens = tens1 * ones2  # Missing carry!
            malrule_pp1 = malrule_pp1_tens * 10 + pp1_ones_digit
            correct_pp1 = correct_pp1_tens * 10 + pp1_ones_digit
            partial_product_2 = num1 * tens2

            steps.append(f"Step 1: Multiply {num1} × {ones2} (ones digit of {num2})")
            steps.append(f"  {ones1} × {ones2} = {pp1_ones} → write {pp1_ones_digit}, carry {pp1_carry}")
            steps.append(f"  {tens1} × {ones2} = {tens1 * ones2}")
            steps.append("")
            steps.append(f"MALRULE: Student FORGETS to add carry {pp1_carry} to {tens1 * ones2}")
            steps.append(f"  Student gets partial product 1 = {malrule_pp1}")
            steps.append(f"  (Should be: {tens1 * ones2} + {pp1_carry} = {correct_pp1_tens}, giving {correct_pp1})")
            steps.append("")
            steps.append(f"Step 2: Multiply {num1} × {tens2} (tens digit of {num2})")
            steps.append(f"  Partial product 2: {partial_product_2} (shifted left)")
            steps.append("")
            steps.append(f"Step 3: Add partial products:")
            steps.append(f"  {malrule_pp1} + {partial_product_2}0 = {malrule_answer}")

        elif template == 'three_digit_times_two':
            num1 = problem.metadata['num1']
            num2 = problem.metadata['num2']
            hundreds = problem.metadata.get('hundreds', num1 // 100)
            tens = problem.metadata.get('tens', (num1 // 10) % 10)
            ones = problem.metadata.get('ones', num1 % 10)
            ones2 = problem.metadata['ones2']
            tens2 = problem.metadata.get('tens2', num2 // 10)

            # Compute values for explanation
            pp1_ones = ones * ones2
            pp1_ones_result = pp1_ones % 10
            pp1_carry = pp1_ones // 10
            correct_pp1_tens = tens * ones2 + pp1_carry
            malrule_pp1_tens = tens * ones2  # Missing carry!
            malrule_pp1_tens_result = malrule_pp1_tens % 10
            malrule_pp1_carry = malrule_pp1_tens // 10
            malrule_pp1_hundreds = hundreds * ones2 + malrule_pp1_carry
            malrule_pp1 = malrule_pp1_hundreds * 100 + malrule_pp1_tens_result * 10 + pp1_ones_result
            partial_product_2 = num1 * tens2

            steps.append(f"Step 1: Multiply {num1} × {ones2} (ones digit of {num2})")
            steps.append(f"  {ones} × {ones2} = {pp1_ones} → write {pp1_ones_result}, carry {pp1_carry}")
            steps.append(f"  {tens} × {ones2} = {tens * ones2}")
            steps.append("")
            steps.append(f"MALRULE: Student FORGETS to add carry {pp1_carry} to {tens * ones2}")
            steps.append(f"  Student gets partial product 1 = {malrule_pp1}")
            steps.append(f"  (Should add carry: {tens * ones2} + {pp1_carry} = {correct_pp1_tens})")
            steps.append("")
            steps.append(f"Step 2: Multiply {num1} × {tens2} (tens digit of {num2})")
            steps.append(f"  Partial product 2: {partial_product_2} (shifted left)")
            steps.append("")
            steps.append(f"Step 3: Add partial products:")
            steps.append(f"  {malrule_pp1} + {partial_product_2}0 = {malrule_answer}")

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
            steps.append(f"  MALRULE: Student FORGETS to add carried {carry}")
            steps.append(f"  (Should be: {tens_product} + {carry} = {tens_product + carry})")

        else:  # basic_two_digit_times_one
            multiplicand = problem.metadata.get('multiplicand', problem.operands[0])
            multiplier = problem.metadata.get('multiplier', problem.operands[1] if len(problem.operands) > 1 else problem.metadata.get('multiplier', problem.operands[0]))
            tens_digit = problem.metadata['tens_digit']
            ones_digit = problem.metadata['ones_digit']
            ones_product = problem.metadata['ones_product']
            ones_result = problem.metadata['ones_result']
            carry = problem.metadata['carry']
            tens_product = problem.metadata['tens_product']

            steps.append(f"Step 1: Multiply ones place")
            steps.append(f"  {ones_digit} × {multiplier} = {ones_product}")
            steps.append(f"  Write {ones_result} in ones place, carry {carry}")
            steps.append("")
            steps.append(f"Step 2: Multiply tens place")
            steps.append(f"  {tens_digit} × {multiplier} = {tens_product}")
            steps.append("")
            steps.append("MALRULE: Student FORGETS to add the carried value!")
            steps.append(f"  Student writes {tens_product} in tens place")
            steps.append(f"  (Should add carry: {tens_product} + {carry} = {tens_product + carry})")

        steps.append("")
        steps.append(f"Student's answer: {malrule_answer}")
        steps.append("")
        steps.append(
            "The student multiplied correctly but FORGOT to add the carried value, "
            "leading to an incorrect answer."
        )

        return steps

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the forget-to-add-carried-number malrule.

        Args:
            problem: The multiplication problem
            verbose: If True, generate verbose steps; if False, generate concise steps

        Returns:
            Solution showing forgotten carry
        """
        # Use calculate_expected_answer to compute the malrule result
        malrule_answer = self.calculate_expected_answer(problem)

        if verbose:
            steps = self._generate_verbose_steps(problem, malrule_answer)
        else:
            steps = self._generate_concise_steps(problem, malrule_answer)

        return Solution(
            answer=str(malrule_answer),
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
