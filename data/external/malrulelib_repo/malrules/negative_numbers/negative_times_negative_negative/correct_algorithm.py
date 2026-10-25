"""
Correct algorithm for negative number multiplication.

Implements proper sign rules:
- Positive × Positive = Positive
- Positive × Negative = Negative
- Negative × Positive = Negative
- Negative × Negative = Positive
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import List
from utils import CorrectAlgorithm, Problem, Solution


class NegativeMultiplicationCorrectAlgorithm(CorrectAlgorithm):
    """
    Implements correct negative number multiplication with proper sign rules.

    Applies the correct mathematical rules for determining the sign of
    the product based on the signs of the operands.
    """

    def get_name(self) -> str:
        return "Correct Negative Number Multiplication"

    def get_description(self) -> str:
        return (
            "Standard multiplication algorithm with correct sign rules: "
            "negative × negative = positive, negative × positive = negative, "
            "positive × positive = positive."
        )

    def generate_concise_steps(self, problem: Problem, correct_answer, answer_str: str) -> List[str]:
        """
        Generate concise steps for the solution.

        Format: [Question, formula extraction (for word problems), calculation steps, answer]
        Only includes formula and values, no explanations.
        """
        template = problem.metadata.get('template', 'basic_multiplication')
        operands = problem.operands
        a = operands[0]
        b = operands[1] if len(operands) >= 2 else 0
        a_abs = abs(a)
        b_abs = abs(b)
        steps = []

        steps.append(f"Question: {problem.text}")

        if template == 'word_problem_multi_step':
            c = problem.metadata['c']
            first_product = a * b
            result = first_product * c
            steps.append(f"Formula: ({a}) × ({b}) × {c}")
            steps.append(f"({a}) × ({b}) = {first_product}")
            steps.append(f"{first_product} × {c} = {result}")
            steps.append(f"Answer: {result}")

        elif template == 'word_problem_mixed_operations':
            c = problem.metadata['c']
            mult_result = a * b
            result = mult_result + c
            steps.append(f"Formula: ({a}) × ({b}) + {c}")
            steps.append(f"({a}) × ({b}) = {mult_result}")
            steps.append(f"{mult_result} + {c} = {result}")
            steps.append(f"Answer: {result}")

        elif template == 'word_problem_distributive':
            c = problem.metadata['c']
            pattern = problem.metadata.get('pattern', 'both_positive')
            term1 = a * b
            term2 = a * c
            result = term1 + term2
            if pattern == 'both_negative':
                steps.append(f"Formula: ({a}) × (({b}) + ({c}))")
            else:
                steps.append(f"Formula: ({a}) × ({b} + {c})")
            steps.append(f"({a}) × ({b}) = {term1}")
            steps.append(f"({a}) × ({c}) = {term2}")
            steps.append(f"{term1} + {term2} = {result}")
            steps.append(f"Answer: {result}")

        elif template == 'word_problem_temperature':
            magnitude = a_abs * b_abs
            result = magnitude
            steps.append(f"Formula: ({a}) × ({b})")
            steps.append(f"{a_abs} × {b_abs} = {magnitude}")
            steps.append(f"Answer: +{result}°")

        elif template == 'word_problem_debt':
            magnitude = a_abs * b_abs
            result = magnitude
            steps.append(f"Formula: ({a}) × ({b})")
            steps.append(f"{a_abs} × {b_abs} = {magnitude}")
            steps.append(f"Answer: +${result}")

        elif template == 'equation_solving':
            x = problem.metadata.get('x', -1)
            steps.append(f"Formula: ({a}) × x = {b}")
            steps.append(f"x = {b} ÷ ({a})")
            steps.append(f"x = {x}")
            steps.append(f"Answer: x = {x}")

        elif template == 'pattern_completion':
            b_val = b
            result_neg1 = (-1) * b_val
            magnitude = 2 * abs(b_val)
            result = magnitude
            steps.append(f"Formula: (-2) × ({b_val})")
            steps.append(f"(-1) × ({b_val}) = {result_neg1}")
            steps.append(f"(-2) × ({b_val}) = {result}")
            steps.append(f"Answer: {result}")

        else:  # basic_multiplication
            magnitude = a_abs * b_abs
            a_sign = "negative" if a < 0 else "positive"
            b_sign = "negative" if b < 0 else "positive"
            if a_sign == "negative" and b_sign == "negative":
                result = magnitude
            elif a_sign == "negative" or b_sign == "negative":
                result = -magnitude
            else:
                result = magnitude
            steps.append(f"Formula: {a} × {b}")
            steps.append(f"|{a}| × |{b}| = {a_abs} × {b_abs} = {magnitude}")
            steps.append(f"Answer: {result}")

        return steps

    def generate_verbose_steps(self, problem: Problem, correct_answer, answer_str: str) -> List[str]:
        """
        Generate verbose steps for the solution (original detailed format).

        Includes full explanations, rules, and reasoning.
        """
        template = problem.metadata.get('template', 'basic_multiplication')
        operands = problem.operands
        a = operands[0]
        b = operands[1] if len(operands) >= 2 else 0
        a_abs = abs(a)
        b_abs = abs(b)
        steps = []

        if template == 'word_problem_multi_step':
            c = problem.metadata['c']
            steps.append(f"Problem: {problem.text}")
            steps.append("")
            steps.append("Step 1: Identify the operation")
            steps.append(f"  This involves: ({a}) × ({b}) × {c}")
            steps.append("")
            steps.append("Step 2: Apply sign rules step by step")
            steps.append(f"  First: ({a}) × ({b})")
            first_product = a * b
            steps.append(f"  Rule: negative × negative = POSITIVE")
            steps.append(f"  ({a}) × ({b}) = {first_product}")
            steps.append("")
            steps.append(f"Step 3: Multiply result by third number")
            steps.append(f"  Now: {first_product} × {c}")
            steps.append(f"  Rule: positive × positive = POSITIVE")
            result = first_product * c
            steps.append(f"  {first_product} × {c} = {result}")
            steps.append("")
            steps.append(f"Final Answer: {result}")

        elif template == 'word_problem_mixed_operations':
            c = problem.metadata['c']
            steps.append(f"Problem: {problem.text}")
            steps.append("")
            steps.append("Step 1: Identify the operations")
            steps.append(f"  First multiply: ({a}) × ({b}), then add {c}")
            steps.append("")
            steps.append("Step 2: Perform multiplication")
            steps.append(f"  ({a}) × ({b})")
            steps.append(f"  Rule: negative × negative = POSITIVE")
            mult_result = a * b
            steps.append(f"  {a_abs} × {b_abs} = {mult_result}")
            steps.append("")
            steps.append(f"Step 3: Add the second term")
            result = mult_result + c
            steps.append(f"  {mult_result} + {c} = {result}")
            steps.append("")
            steps.append(f"Final Answer: {result}")

        elif template == 'word_problem_distributive':
            c = problem.metadata['c']
            pattern = problem.metadata.get('pattern', 'both_positive')
            steps.append(f"Problem: {problem.text}")
            steps.append("")
            steps.append("Step 1: Identify the distributive property")
            if pattern == 'both_negative':
                steps.append(f"  Expression: ({a}) × (({b}) + ({c}))")
                steps.append(f"  This equals: ({a}) × ({b}) + ({a}) × ({c})")
            else:
                steps.append(f"  Expression: ({a}) × ({b} + {c})")
                steps.append(f"  This equals: ({a}) × {b} + ({a}) × {c}")
            steps.append("")
            steps.append("Step 2: Distribute and multiply")
            if pattern == 'both_negative':
                term1 = a * b
                term2 = a * c
                steps.append(f"  ({a}) × ({b}) = {term1} (negative × negative = positive)")
                steps.append(f"  ({a}) × ({c}) = {term2} (negative × negative = positive)")
            else:
                term1 = a * b
                term2 = a * c
                steps.append(f"  ({a}) × {b} = {term1}")
                steps.append(f"  ({a}) × {c} = {term2}")
            steps.append("")
            steps.append("Step 3: Add the results")
            result = term1 + term2
            steps.append(f"  {term1} + {term2} = {result}")
            steps.append("")
            steps.append(f"Final Answer: {result}")

        elif template == 'word_problem_temperature':
            drop_amount = problem.metadata.get('drop_amount', a_abs)
            num_reversals = problem.metadata.get('num_reversals', b_abs)
            steps.append(f"Problem: {problem.text}")
            steps.append("")
            steps.append("Step 1: Identify the operation")
            steps.append(f"  Reversing a {drop_amount} degree drop {num_reversals} times")
            steps.append(f"  This is ({a}) × ({b})")
            steps.append("")
            steps.append("Step 2: Apply correct sign rule")
            steps.append(f"  Rule: negative × negative = POSITIVE")
            steps.append(f"  Explanation: Reversing a drop is a rise!")
            steps.append("")
            steps.append("Step 3: Calculate magnitude")
            magnitude = a_abs * b_abs
            steps.append(f"  {a_abs} × {b_abs} = {magnitude}")
            steps.append("")
            result = magnitude
            steps.append(f"Final Answer: +{result}°")

        elif template == 'word_problem_debt':
            debt_amount = problem.metadata.get('debt_amount', a_abs)
            num_debts = problem.metadata.get('num_debts', b_abs)
            steps.append(f"Problem: {problem.text}")
            steps.append("")
            steps.append("Step 1: Identify the operation")
            steps.append(f"  Removing {num_debts} debts of ${debt_amount}")
            steps.append(f"  This is ({a}) × ({b})")
            steps.append("")
            steps.append("Step 2: Apply correct sign rule")
            steps.append(f"  Rule: negative × negative = POSITIVE")
            steps.append(f"  Explanation: Removing debts is a gain!")
            steps.append("")
            steps.append("Step 3: Calculate magnitude")
            magnitude = a_abs * b_abs
            steps.append(f"  ${a_abs} × {b_abs} = ${magnitude}")
            steps.append("")
            result = magnitude
            steps.append(f"Final Answer: +${result}")

        elif template == 'equation_solving':
            x = problem.metadata.get('x', -1)
            steps.append(f"Problem: {problem.text}")
            steps.append("")
            steps.append("Step 1: Set up the equation")
            steps.append(f"  ({a}) × x = {b}")
            steps.append("")
            steps.append("Step 2: Divide both sides by ({a})")
            steps.append(f"  x = {b} ÷ ({a})")
            steps.append("")
            steps.append("Step 3: Apply correct sign rule")
            steps.append(f"  positive ÷ negative = negative")
            steps.append(f"  {b} ÷ ({a}) = {x}")
            steps.append("")
            steps.append(f"Final Answer: x = {x}")

        elif template == 'pattern_completion':
            b_val = b
            pattern = problem.metadata.get('pattern', '')
            steps.append("Problem: Complete the pattern")
            steps.append(pattern)
            steps.append("")
            steps.append("Step 1: Observe the pattern")
            steps.append(f"  As the first number decreases, the product increases")
            steps.append(f"  Pattern increases by {abs(b_val)} each time")
            steps.append("")
            steps.append("Step 2: Continue the pattern correctly")
            result_neg1 = (-1) * b_val
            steps.append(f"  (-1) × ({b_val}) = {result_neg1}")
            steps.append("")
            steps.append("Step 3: Calculate (-2) × ({b_val})")
            steps.append(f"  Rule: negative × negative = POSITIVE")
            magnitude = 2 * abs(b_val)
            result = magnitude
            steps.append(f"  2 × {abs(b_val)} = {result}")
            steps.append("")
            steps.append(f"Final Answer: (-2) × ({b_val}) = {result}")

        else:  # basic_multiplication
            steps.append(f"Problem: {a} × {b}")
            steps.append("")
            a_sign = "negative" if a < 0 else "positive"
            b_sign = "negative" if b < 0 else "positive"
            steps.append("Step 1: Identify signs")
            steps.append(f"  First number: {a} is {a_sign}")
            steps.append(f"  Second number: {b} is {b_sign}")
            steps.append("")
            steps.append("Step 2: Apply sign rule")
            if a_sign == "negative" and b_sign == "negative":
                result_sign = "positive"
                steps.append(f"  Rule: negative × negative = POSITIVE")
                steps.append(f"  Why: Two negatives make a positive")
                steps.append(f"  Explanation: Negative means 'opposite', so opposite of opposite is back to positive")
            elif a_sign == "negative" and b_sign == "positive":
                result_sign = "negative"
                steps.append(f"  Rule: negative × positive = NEGATIVE")
                steps.append(f"  Why: Negative times positive stays negative")
            elif a_sign == "positive" and b_sign == "negative":
                result_sign = "negative"
                steps.append(f"  Rule: positive × negative = NEGATIVE")
                steps.append(f"  Why: Positive times negative is negative")
            else:
                result_sign = "positive"
                steps.append(f"  Rule: positive × positive = POSITIVE")
                steps.append(f"  Why: No negatives means positive result")
            steps.append("")
            steps.append("Step 3: Multiply magnitudes (absolute values)")
            magnitude = a_abs * b_abs
            steps.append(f"  |{a}| × |{b}| = {a_abs} × {b_abs} = {magnitude}")
            steps.append("")
            steps.append("Step 4: Apply sign to magnitude")
            if result_sign == "positive":
                result = magnitude
                steps.append(f"  Sign: positive, so answer is +{magnitude}")
            else:
                result = -magnitude
                steps.append(f"  Sign: negative, so answer is {result}")
            steps.append("")
            steps.append(f"Final Answer: {result}")

        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply correct multiplication with proper sign handling.

        Args:
            problem: Problem instance with operands
            verbose: If True, generate verbose steps; if False, generate concise steps (default: False)

        Returns:
            Solution with correct answer (as string) and detailed steps
        """
        template = problem.metadata.get('template', 'basic_multiplication')
        operands = problem.operands

        # COMPUTE the correct answer from operands - never use metadata
        if len(operands) >= 3:
            # multi_step or distributive: a * b * c or a * (b + c)
            a, b, c = operands[0], operands[1], operands[2]
            if template == 'word_problem_distributive' or template == 'distributive':
                correct_answer = a * (b + c)
            else:
                # multi_step or mixed_operations
                if template == 'word_problem_mixed_operations' or template == 'mixed_operations':
                    correct_answer = a * b + c
                else:
                    correct_answer = a * b * c
        elif len(operands) == 2:
            a, b = operands[0], operands[1]
            if problem.operation == 'division':
                correct_answer = a // b
            elif problem.operation == 'equation':
                # For equation solving, b is the result, a is the coefficient
                # We need to find x where a * x = b
                correct_answer = b // a
            else:
                correct_answer = a * b
        else:
            a = operands[0]
            correct_answer = a

        # For word problems with units, check metadata for answer format
        answer_str = str(correct_answer)
        if template == 'word_problem_temperature':
            # Check if metadata has specific format
            if correct_answer > 0:
                answer_str = f'+{correct_answer}°'
            else:
                answer_str = f'{correct_answer}°'
        elif template == 'word_problem_debt':
            if correct_answer > 0:
                answer_str = f'+${correct_answer}'
            else:
                answer_str = f'${correct_answer}'

        # Generate steps based on verbose flag
        if verbose:
            steps = self.generate_verbose_steps(problem, correct_answer, answer_str)
        else:
            steps = self.generate_concise_steps(problem, correct_answer, answer_str)

        return Solution(
            answer=answer_str if template in ['word_problem_temperature', 'word_problem_debt'] else str(correct_answer),
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
