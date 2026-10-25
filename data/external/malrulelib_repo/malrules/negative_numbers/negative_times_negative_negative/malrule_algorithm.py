"""
Malrule algorithm for Negative-Times-Negative-Negative error.

Students incorrectly apply reversed sign rules, believing that
negative × negative = negative (instead of positive).
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import Dict, List, Any
from utils import Malrule, Problem, Solution

class NegativeTimesNegativeNegativeMalrule(Malrule):
    """
    Implements the Negative-Times-Negative-Negative malrule.

    Students incorrectly believe that multiplying two negative numbers
    gives a negative result, reversing the correct sign rule.

    Example: -3 × -2
    Correct: -3 × -2 = +6 (negative × negative = positive)
    Malrule: -3 × -2 = -6 (student thinks it stays negative)
    """

    def get_name(self) -> str:
        return "Negative-Times-Negative-Negative (Reversed Sign Rule)"

    def get_description(self) -> str:
        return (
            "Students incorrectly believe that multiplying two negative numbers gives a "
            "negative result, reversing the correct sign rule. Altiparmak & Özdoğan (2010) "
            "identified this as one of the difficulties 'students face with regard to "
            "arithmetic operations' with negative numbers. Students may conflate the "
            "multiplication rule with the addition rule (where two negatives do produce "
            "a more negative result), or they may reason that 'negative is a property that "
            "accumulates' rather than understanding multiplication as directional transformation."
        )

    def calculate_expected_answer(self, problem: Problem):
        """
        Calculate the expected incorrect answer for this malrule.

        For Negative-Times-Negative-Negative:
        - If both numbers are negative:
          * MALRULE: negative × negative = negative (wrong!)
        - Otherwise: Apply correct sign rules

        Args:
            problem: Multiplication/division problem with negative numbers

        Returns:
            Expected incorrect answer as string
        """
        # Backwards compatibility: calculate for old problems
        a = problem.metadata['a']
        b = problem.metadata['b']
        operation = problem.operation

        # Check for special templates
        template = problem.metadata.get('template', 'basic_multiplication')

        if template == 'multi_step_multiplication':
            # Three operands: (-a) × (-b) × (-c)
            c = problem.metadata['c']
            # MALRULE: thinks all negatives = negative
            magnitude = abs(a) * abs(b) * abs(c)
            # Student thinks: negative × negative × negative = negative (wrong!)
            return str(-magnitude)

        elif template == 'mixed_operations':
            # Mixed: (-a) × (-b) + c
            c = problem.metadata['c']
            # MALRULE: (-a) × (-b) = negative (wrong!)
            mult_magnitude = abs(a) * abs(b)
            mult_result = -mult_magnitude  # Malrule thinks neg×neg = neg
            return str(mult_result + c)

        elif operation == 'division':
            # Division: negative ÷ negative
            magnitude = abs(a) // abs(b)
            if a < 0 and b < 0:
                # MALRULE: negative ÷ negative = negative (wrong!)
                return str(-magnitude)
            elif (a < 0 and b >= 0) or (a >= 0 and b < 0):
                # Correct: negative ÷ positive = negative
                return str(-magnitude)
            else:
                # Correct: positive ÷ positive = positive
                return str(magnitude)
        else:
            # Basic multiplication with two operands
            magnitude = abs(a) * abs(b)

            # Apply REVERSED sign rule for neg × neg
            if a < 0 and b < 0:
                # MALRULE: negative × negative = negative (wrong!)
                return str(-magnitude)
            elif (a < 0 and b >= 0) or (a >= 0 and b < 0):
                # Correct: negative × positive = negative
                return str(-magnitude)
            else:
                # Correct: positive × positive = positive
                return str(magnitude)

    def generate_concise_steps(self, problem: Problem, malrule_answer: str) -> List[str]:
        """
        Generate concise steps for the malrule solution.

        Format: [Question, formula extraction (for word problems), calculation steps, answer]
        Only includes formula and values, no explanations.
        """
        a = problem.metadata['a']
        b = problem.metadata['b']
        a_abs = abs(a)
        b_abs = abs(b)
        template = problem.metadata.get('template', 'basic_multiplication')
        operation = problem.operation
        steps = []

        steps.append(f"Question: {problem.text}")

        if template == 'word_problem_multi_step':
            c = problem.metadata['c']
            malrule_first = -(a_abs * b_abs)
            result = malrule_first * c
            steps.append(f"Formula: ({a}) × ({b}) × {c}")
            steps.append(f"({a}) × ({b}) = {malrule_first}")
            steps.append(f"{malrule_first} × {c} = {result}")
            steps.append(f"Answer: {result}")

        elif template == 'word_problem_mixed_operations':
            c = problem.metadata['c']
            mult_result = -(a_abs * b_abs)
            result = mult_result + c
            steps.append(f"Formula: ({a}) × ({b}) + {c}")
            steps.append(f"({a}) × ({b}) = {mult_result}")
            steps.append(f"{mult_result} + {c} = {result}")
            steps.append(f"Answer: {result}")

        elif template == 'word_problem_distributive':
            c = problem.metadata['c']
            pattern = problem.metadata.get('pattern', 'both_positive')
            if pattern == 'both_negative':
                term1 = -(a_abs * abs(b))
                term2 = -(a_abs * abs(c))
            else:
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
            result = -magnitude
            steps.append(f"Formula: ({a}) × ({b})")
            steps.append(f"{a_abs} × {b_abs} = {magnitude}")
            steps.append(f"Answer: {result}°")

        elif template == 'word_problem_debt':
            magnitude = a_abs * b_abs
            result = -magnitude
            steps.append(f"Formula: ({a}) × ({b})")
            steps.append(f"{a_abs} × {b_abs} = {magnitude}")
            steps.append(f"Answer: ${result}")

        elif template == 'equation_solving':
            x = problem.metadata.get('x', -1)
            result = abs(x)
            steps.append(f"Formula: ({a}) × x = {b}")
            steps.append(f"x = {b} ÷ ({a})")
            steps.append(f"x = {result}")
            steps.append(f"Answer: x = {result}")

        elif template == 'pattern_completion':
            b_val = b
            magnitude = 2 * abs(b_val)
            result = -magnitude
            steps.append(f"Formula: (-2) × ({b_val})")
            steps.append(f"2 × {abs(b_val)} = {magnitude}")
            steps.append(f"Answer: {result}")

        elif template == 'multi_step_multiplication':
            c = problem.metadata['c']
            c_abs = abs(c)
            magnitude = a_abs * b_abs * c_abs
            result = -magnitude
            steps.append(f"Formula: ({a}) × ({b}) × ({c})")
            steps.append(f"|{a}| × |{b}| × |{c}| = {a_abs} × {b_abs} × {c_abs} = {magnitude}")
            steps.append(f"Answer: {result}")

        elif template == 'mixed_operations':
            c = problem.metadata['c']
            mult_magnitude = a_abs * b_abs
            mult_result = -mult_magnitude
            result = mult_result + c
            steps.append(f"Formula: ({a}) × ({b}) + ({c})")
            steps.append(f"|{a}| × |{b}| = {mult_magnitude}")
            steps.append(f"{mult_result} + ({c}) = {result}")
            steps.append(f"Answer: {result}")

        elif operation == 'division':
            magnitude = a_abs // b_abs
            a_sign = "negative" if a < 0 else "positive"
            b_sign = "negative" if b < 0 else "positive"
            if a_sign == "negative" and b_sign == "negative":
                result = -magnitude
            else:
                result = -magnitude if (a < 0) != (b < 0) else magnitude
            steps.append(f"Formula: ({a}) ÷ ({b})")
            steps.append(f"|{a}| ÷ |{b}| = {a_abs} ÷ {b_abs} = {magnitude}")
            steps.append(f"Answer: {result}")

        else:  # basic_multiplication
            magnitude = a_abs * b_abs
            a_sign = "negative" if a < 0 else "positive"
            b_sign = "negative" if b < 0 else "positive"
            if a_sign == "negative" and b_sign == "negative":
                result = -magnitude
            elif a_sign == "negative" or b_sign == "negative":
                result = -magnitude
            else:
                result = magnitude
            steps.append(f"Formula: {a} × {b}")
            steps.append(f"|{a}| × |{b}| = {a_abs} × {b_abs} = {magnitude}")
            steps.append(f"Answer: {result}")

        return steps

    def generate_verbose_steps(self, problem: Problem, malrule_answer: str) -> List[str]:
        """
        Generate verbose steps for the malrule solution (original detailed format).

        Includes full explanations, rules, and reasoning.
        """
        a = problem.metadata['a']
        b = problem.metadata['b']
        a_abs = abs(a)
        b_abs = abs(b)
        template = problem.metadata.get('template', 'basic_multiplication')
        operation = problem.operation
        steps = []

        if template == 'word_problem_multi_step':
            c = problem.metadata['c']
            steps.append(f"Problem: {problem.text}")
            steps.append("")
            steps.append("Step 1: Identify the operation")
            steps.append(f"  Operation: ({a}) × ({b}) × {c}")
            steps.append("")
            steps.append("Step 2: Apply multiplication (MALRULE)")
            steps.append(f"  First: ({a}) × ({b})")
            steps.append(f"  MALRULE: negative × negative = NEGATIVE")
            steps.append(f"  MALRULE REASONING: 'Both numbers are negative, so result is negative'")
            steps.append(f"  (WRONG! Correct rule: negative × negative = positive)")
            malrule_first = -(a_abs * b_abs)
            steps.append(f"  Malrule result: {malrule_first}")
            steps.append("")
            steps.append("Step 3: Multiply by third number")
            result = malrule_first * c
            steps.append(f"  {malrule_first} × {c} = {result}")
            steps.append("")
            steps.append(f"Final Answer: {result} (INCORRECT)")

        elif template == 'word_problem_mixed_operations':
            c = problem.metadata['c']
            steps.append(f"Problem: {problem.text}")
            steps.append("")
            steps.append("Step 1: Identify the operations")
            steps.append(f"  First multiply: ({a}) × ({b}), then add {c}")
            steps.append("")
            steps.append("Step 2: Perform multiplication (MALRULE)")
            steps.append(f"  ({a}) × ({b})")
            steps.append(f"  MALRULE: negative × negative = NEGATIVE")
            steps.append(f"  MALRULE REASONING: 'Both numbers are negative, so result is negative'")
            steps.append(f"  (WRONG! Correct rule: negative × negative = positive)")
            mult_result = -(a_abs * b_abs)
            steps.append(f"  {a_abs} × {b_abs} = {-mult_result}, with negative sign: {mult_result}")
            steps.append("")
            steps.append(f"Step 3: Add the second term")
            result = mult_result + c
            steps.append(f"  {mult_result} + {c} = {result}")
            steps.append("")
            steps.append(f"Final Answer: {result} (INCORRECT)")

        elif template == 'word_problem_distributive':
            c = problem.metadata['c']
            pattern = problem.metadata.get('pattern', 'both_positive')
            steps.append(f"Problem: {problem.text}")
            steps.append("")
            steps.append("Step 1: Identify the distributive property")
            if pattern == 'both_negative':
                steps.append(f"  Expression: ({a}) × (({b}) + ({c}))")
                steps.append(f"  Distribute: ({a}) × ({b}) + ({a}) × ({c})")
            else:
                steps.append(f"  Expression: ({a}) × ({b} + {c})")
                steps.append(f"  Distribute: ({a}) × {b} + ({a}) × {c}")
            steps.append("")
            steps.append("Step 2: Apply multiplication (MALRULE)")
            if pattern == 'both_negative':
                steps.append(f"  ({a}) × ({b}): MALRULE says negative × negative = NEGATIVE")
                steps.append(f"  ({a}) × ({c}): MALRULE says negative × negative = NEGATIVE")
                steps.append(f"  (WRONG! Both should be positive)")
                term1 = -(a_abs * abs(b))
                term2 = -(a_abs * abs(c))
                steps.append(f"  Term 1: {term1}")
                steps.append(f"  Term 2: {term2}")
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
            steps.append(f"Final Answer: {result}" + (" (INCORRECT)" if pattern == 'both_negative' else ""))

        elif template == 'word_problem_temperature':
            drop_amount = problem.metadata.get('drop_amount', a_abs)
            num_reversals = problem.metadata.get('num_reversals', b_abs)
            steps.append(f"Problem: {problem.text}")
            steps.append("")
            steps.append("Step 1: Identify the operation")
            steps.append(f"  We are reversing a {drop_amount} degree drop {num_reversals} times")
            steps.append(f"  This is ({a}) × ({b})")
            steps.append("")
            steps.append("Step 2: Apply sign rule")
            steps.append(f"  MALRULE: negative × negative = NEGATIVE")
            steps.append(f"  MALRULE REASONING: 'Both numbers are negative, so the result is negative'")
            steps.append(f"  (WRONG! Correct rule: negative × negative = positive)")
            steps.append("")
            steps.append("Step 3: Calculate magnitude")
            magnitude = a_abs * b_abs
            steps.append(f"  {a_abs} × {b_abs} = {magnitude}")
            steps.append("")
            result = -magnitude
            steps.append(f"Final Answer: {result}° (INCORRECT)")

        elif template == 'word_problem_debt':
            debt_amount = problem.metadata.get('debt_amount', a_abs)
            num_debts = problem.metadata.get('num_debts', b_abs)
            steps.append(f"Problem: {problem.text}")
            steps.append("")
            steps.append("Step 1: Identify the operation")
            steps.append(f"  Removing {num_debts} debts of ${debt_amount}")
            steps.append(f"  This is ({a}) × ({b})")
            steps.append("")
            steps.append("Step 2: Apply sign rule")
            steps.append(f"  MALRULE: negative × negative = NEGATIVE")
            steps.append(f"  MALRULE REASONING: 'Both are negative, so result is negative'")
            steps.append(f"  (WRONG! Correct: removing debts is a positive gain!)")
            steps.append("")
            steps.append("Step 3: Calculate magnitude")
            magnitude = a_abs * b_abs
            steps.append(f"  ${a_abs} × {b_abs} = ${magnitude}")
            steps.append("")
            result = -magnitude
            steps.append(f"Final Answer: ${result} (INCORRECT)")

        elif template == 'equation_solving':
            x = problem.metadata.get('x', -1)
            result = abs(x)
            steps.append(f"Problem: {problem.text}")
            steps.append("")
            steps.append("Step 1: Set up the equation")
            steps.append(f"  ({a}) × x = {b}")
            steps.append("")
            steps.append("Step 2: Divide both sides by ({a})")
            steps.append(f"  x = {b} ÷ ({a})")
            steps.append("")
            steps.append("Step 3: Apply sign rule")
            steps.append(f"  MALRULE: positive ÷ negative = negative, BUT...")
            steps.append(f"  MALRULE REASONING: 'The answer should be positive because ({a}) × positive = positive'")
            steps.append(f"  (WRONG! Student confuses the sign rule)")
            steps.append("")
            steps.append(f"Final Answer: x = {result} (INCORRECT)")

        elif template == 'pattern_completion':
            b_val = b
            pattern = problem.metadata.get('pattern', '')
            steps.append("Problem: Complete the pattern")
            steps.append(pattern)
            steps.append("")
            steps.append("Step 1: Observe the pattern")
            steps.append(f"  As the first number decreases, the product increases")
            steps.append(f"  When first number is 0: 0 × ({b_val}) = 0")
            steps.append("")
            steps.append("Step 2: Continue the pattern (MALRULE)")
            steps.append(f"  (-1) × ({b_val}) = ?")
            steps.append(f"  MALRULE REASONING: 'Both negative, so result is negative'")
            steps.append(f"  (WRONG! Pattern should continue: products increase)")
            steps.append("")
            steps.append("Step 3: Calculate (-2) × ({b_val})")
            steps.append(f"  MALRULE: negative × negative = NEGATIVE")
            magnitude = 2 * abs(b_val)
            result = -magnitude
            steps.append(f"  2 × {abs(b_val)} = {magnitude}, with negative sign: {result}")
            steps.append("")
            steps.append(f"Final Answer: (-2) × ({b_val}) = {result} (INCORRECT)")

        elif template == 'multi_step_multiplication':
            c = problem.metadata['c']
            c_abs = abs(c)
            steps.append(f"Problem: ({a}) × ({b}) × ({c})")
            steps.append("")
            steps.append("Step 1: Identify all signs")
            steps.append(f"  All three numbers are negative")
            steps.append("")
            steps.append("Step 2: Apply sign rule")
            steps.append(f"  MALRULE: negative × negative × negative = NEGATIVE")
            steps.append(f"  MALRULE REASONING: 'All negatives together make negative'")
            steps.append(f"  (WRONG! Correct: odd number of negatives = negative, but reasoning is wrong)")
            steps.append("")
            steps.append("Step 3: Multiply magnitudes")
            magnitude = a_abs * b_abs * c_abs
            steps.append(f"  |{a}| × |{b}| × |{c}| = {a_abs} × {b_abs} × {c_abs} = {magnitude}")
            steps.append("")
            result = -magnitude
            steps.append(f"Final Answer: {result} (INCORRECT reasoning!)")

        elif template == 'mixed_operations':
            c = problem.metadata['c']
            steps.append(f"Problem: ({a}) × ({b}) + ({c})")
            steps.append("")
            steps.append("Step 1: First multiply ({a}) × ({b})")
            steps.append(f"  Both numbers are negative")
            steps.append(f"  MALRULE: negative × negative = NEGATIVE")
            steps.append(f"  MALRULE REASONING: 'Two negatives together make negative'")
            steps.append(f"  (WRONG! Correct rule: negative × negative = positive)")
            steps.append("")
            mult_magnitude = a_abs * b_abs
            mult_result = -mult_magnitude
            steps.append(f"  |{a}| × |{b}| = {a_abs} × {b_abs} = {mult_magnitude}")
            steps.append(f"  With negative sign: {mult_result}")
            steps.append("")
            steps.append(f"Step 2: Add {c}")
            result = mult_result + c
            steps.append(f"  {mult_result} + ({c}) = {result}")
            steps.append("")
            steps.append(f"Final Answer: {result} (INCORRECT)")

        elif operation == 'division':
            steps.append(f"Problem: ({a}) ÷ ({b})")
            steps.append("")
            a_sign = "negative" if a < 0 else "positive"
            b_sign = "negative" if b < 0 else "positive"
            steps.append("Step 1: Identify signs")
            steps.append(f"  First number: {a} is {a_sign}")
            steps.append(f"  Second number: {b} is {b_sign}")
            steps.append("")
            steps.append("Step 2: Apply sign rule for division")
            if a_sign == "negative" and b_sign == "negative":
                result_sign = "negative"
                steps.append(f"  MALRULE: negative ÷ negative = NEGATIVE")
                steps.append(f"  MALRULE REASONING: 'Two negatives make negative'")
                steps.append(f"  (WRONG! Correct rule: negative ÷ negative = positive)")
            else:
                result_sign = "negative" if (a < 0) != (b < 0) else "positive"
                steps.append(f"  Rule: {a_sign} ÷ {b_sign} = {result_sign.upper()}")
            steps.append("")
            steps.append("Step 3: Divide magnitudes")
            magnitude = a_abs // b_abs
            steps.append(f"  |{a}| ÷ |{b}| = {a_abs} ÷ {b_abs} = {magnitude}")
            steps.append("")
            if result_sign == "positive":
                result = magnitude
            else:
                result = -magnitude
            steps.append(f"Final Answer: {result}" + (" (INCORRECT)" if a_sign == "negative" and b_sign == "negative" else ""))

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
                result_sign = "negative"
                steps.append(f"  MALRULE: negative × negative = NEGATIVE")
                steps.append(f"  MALRULE REASONING: 'Two negatives together make negative'")
                steps.append(f"  (WRONG! Correct rule: negative × negative = positive)")
            elif a_sign == "negative" and b_sign == "positive":
                result_sign = "negative"
                steps.append(f"  Rule: negative × positive = NEGATIVE")
            elif a_sign == "positive" and b_sign == "negative":
                result_sign = "negative"
                steps.append(f"  Rule: positive × negative = NEGATIVE")
            else:
                result_sign = "positive"
                steps.append(f"  Rule: positive × positive = POSITIVE")
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
            if a_sign == "negative" and b_sign == "negative":
                steps.append(f"Final Answer: {result} (INCORRECT)")
            else:
                steps.append(f"Final Answer: {result}")

        return steps

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the reversed sign rule malrule.

        Students incorrectly compute negative × negative as negative.

        Args:
            problem: Problem instance with operands
            verbose: If True, generate verbose steps; if False, generate concise steps (default: False)

        Returns:
            Solution with incorrect answer (as string) and student's reasoning
        """
        a = problem.metadata['a']
        b = problem.metadata['b']
        a_abs = abs(a)
        b_abs = abs(b)
        template = problem.metadata.get('template', 'basic_multiplication')
        operation = problem.operation

        # Calculate the malrule answer
        malrule_answer = self.calculate_expected_answer(problem)

        # Generate steps based on verbose flag
        if verbose:
            steps = self.generate_verbose_steps(problem, malrule_answer)
        else:
            steps = self.generate_concise_steps(problem, malrule_answer)

        # Determine the final answer format based on template
        if template == 'word_problem_temperature':
            magnitude = a_abs * b_abs
            result = -magnitude
            final_answer = str(result) + '°'
        elif template == 'word_problem_debt':
            magnitude = a_abs * b_abs
            result = -magnitude
            final_answer = '$' + str(result)
        elif template == 'equation_solving':
            x = problem.metadata.get('x', -1)
            final_answer = str(abs(x))
        else:
            final_answer = malrule_answer

        return Solution(
            answer=final_answer,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
