"""
Malrule algorithm for Each-Fraction-Digit-Is-Ratio error.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import Dict, List, Any
from math import gcd
from utils import Malrule, Problem, Solution

class EachFractionDigitIsRatioMalrule(Malrule):
    """
    Students treat multi-digit numerators/denominators as separate single-digit ratios.

    Example: Simplify 12/34
    Student processes digit-by-digit:
    - 1/3 (can't simplify) → 1/3
    - 2/4 (simplifies to 1/2) → 1/2
    - Concatenate: 11/32 (wrong!)
    Correct: 12/34 = 6/17 (divide both by GCD of 2)
    """

    def get_name(self) -> str:
        return "Whole Number Bias in Fraction Components"

    def get_description(self) -> str:
        return (
            "Student treats the numerator and denominator as independent whole numbers "
            "rather than as components of a single rational number. When simplifying "
            "multi-digit fractions, the student processes each digit position separately "
            "as if it were an independent ratio."
        )

    def calculate_expected_answer(self, problem: Problem):
        """Calculate the expected malrule answer (incorrect) for this problem."""
        # Compute by treating each digit as separate ratio
        from math import gcd
        numerator = problem.metadata['numerator']
        denominator = problem.metadata['denominator']
        
        num_str = str(numerator)
        den_str = str(denominator)
        max_len = max(len(num_str), len(den_str))
        num_str = num_str.zfill(max_len)
        den_str = den_str.zfill(max_len)
        
        result_num_digits = []
        result_den_digits = []
        
        for i in range(max_len):
            digit_num = int(num_str[i])
            digit_den = int(den_str[i])
            
            if digit_den == 0:
                digit_den = 1
            
            if digit_num == 0:
                simp_num = 0
                simp_den = 1
            else:
                digit_gcd = gcd(digit_num, digit_den)
                simp_num = digit_num // digit_gcd
                simp_den = digit_den // digit_gcd
            
            result_num_digits.append(simp_num)
            result_den_digits.append(simp_den)
        
        malrule_num = int(''.join(str(d) for d in result_num_digits))
        malrule_den = int(''.join(str(d) for d in result_den_digits))
        
        return f"{malrule_num}:{malrule_den}"

    def _generate_concise_steps(self, problem: Problem, malrule_num: int, malrule_den: int,
                                result_num_digits: List[int], result_den_digits: List[int]) -> List[str]:
        """Generate concise steps showing only formula and values."""
        steps = []
        numerator = problem.metadata['numerator']
        denominator = problem.metadata['denominator']
        template = problem.metadata.get('template', 'basic_two_digit')

        # Add question
        if template == 'word_problem_context':
            steps.append(f"Question: {problem.text}")
        else:
            steps.append(f"Question: Simplify {numerator}:{denominator}")

        steps.append(f"Formula: Simplify each digit pair separately, then concatenate")

        # Show digit simplifications
        num_str = str(numerator)
        den_str = str(denominator)
        max_len = max(len(num_str), len(den_str))
        num_str = num_str.zfill(max_len)
        den_str = den_str.zfill(max_len)

        for i in range(max_len):
            digit_num = int(num_str[i])
            digit_den = int(den_str[i])
            steps.append(f"Step {i+1}: {digit_num}/{digit_den} → {result_num_digits[i]}/{result_den_digits[i]}")

        steps.append(f"Step {max_len+1}: Concatenate: {malrule_num}:{malrule_den}")
        steps.append(f"Answer: {malrule_num}:{malrule_den}")
        return steps

    def _generate_verbose_steps(self, problem: Problem, malrule_num: int, malrule_den: int,
                                result_num_digits: List[int], result_den_digits: List[int]) -> List[str]:
        """Generate verbose steps with full explanations (original format)."""
        steps = []
        numerator = problem.metadata['numerator']
        denominator = problem.metadata['denominator']
        template = problem.metadata.get('template', 'basic_two_digit')

        # Template-specific introduction
        if template == 'word_problem_context':
            context_type = problem.metadata.get('context_type', 'ratio')
            steps.append(f"Problem: {problem.text[:80]}...")
            steps.append(f"  Context: {problem.metadata.get('context_desc', 'ratio problem')}")
        else:
            steps.append(f"Problem: Simplify {numerator}:{denominator}")

        steps.append("")
        steps.append("MALRULE: Treat each digit as a separate ratio")
        steps.append(f"  MALRULE REASONING: 'Each digit pair is its own fraction'")
        steps.append(f"                     'Simplify each pair, then combine'")
        steps.append("")

        # Show digit-by-digit processing
        num_str = str(numerator)
        den_str = str(denominator)
        max_len = max(len(num_str), len(den_str))
        num_str = num_str.zfill(max_len)
        den_str = den_str.zfill(max_len)

        steps.append(f"Step 1: Break into digit pairs")
        for i in range(max_len):
            steps.append(f"  Position {i+1}: {num_str[i]}/{den_str[i]}")
        steps.append("")

        steps.append(f"Step 2: Simplify each digit pair independently")

        for i in range(max_len):
            digit_num = int(num_str[i])
            digit_den = int(den_str[i])

            if digit_den == 0:
                digit_den = 1

            if digit_num == 0:
                simp_num = 0
                simp_den = 1
                digit_gcd = 1
            else:
                digit_gcd = gcd(digit_num, digit_den)
                simp_num = digit_num // digit_gcd
                simp_den = digit_den // digit_gcd

            if digit_gcd > 1:
                steps.append(f"  {digit_num}/{digit_den} ÷ {digit_gcd} = {simp_num}/{simp_den}")
            else:
                steps.append(f"  {digit_num}/{digit_den} (can't simplify)")

        steps.append("")
        steps.append(f"Step 3: Concatenate simplified digits")
        steps.append(f"  Numerators: {' and '.join(str(d) for d in result_num_digits)} → {malrule_num}")
        steps.append(f"  Denominators: {' and '.join(str(d) for d in result_den_digits)} → {malrule_den}")
        steps.append("")
        steps.append(f"Final Answer: {malrule_num}:{malrule_den} (INCORRECT!)")
        steps.append("")
        steps.append(f"WHY WRONG: {numerator} is not '{num_str[0]} and {num_str[1]}', it's {numerator}!")
        steps.append(f"           Correct: {numerator}:{denominator} = {problem.metadata['correct_num']}:{problem.metadata['correct_den']}")

        return steps

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the each-fraction-digit-is-ratio malrule.

        Students incorrectly treat each digit position as a separate ratio.

        Args:
            problem: Problem instance with numerator and denominator
            verbose: If True, generate verbose explanatory steps; if False, generate concise steps

        Returns:
            Solution with incorrect answer and student's reasoning
        """
        numerator = problem.metadata['numerator']
        denominator = problem.metadata['denominator']

        # MALRULE: Treat each digit as separate ratio
        # Compute it here (same logic as calculate_expected_answer)
        from math import gcd
        num_str = str(numerator)
        den_str = str(denominator)
        max_len = max(len(num_str), len(den_str))
        num_str = num_str.zfill(max_len)
        den_str = den_str.zfill(max_len)

        result_num_digits = []
        result_den_digits = []

        for i in range(max_len):
            digit_num = int(num_str[i])
            digit_den = int(den_str[i])
            if digit_den == 0:
                digit_den = 1
            if digit_num == 0:
                result_num_digits.append(0)
                result_den_digits.append(1)
            else:
                digit_gcd = gcd(digit_num, digit_den)
                result_num_digits.append(digit_num // digit_gcd)
                result_den_digits.append(digit_den // digit_gcd)

        malrule_num = int(''.join(str(d) for d in result_num_digits))
        malrule_den = int(''.join(str(d) for d in result_den_digits))

        if verbose:
            steps = self._generate_verbose_steps(problem, malrule_num, malrule_den, result_num_digits, result_den_digits)
        else:
            steps = self._generate_concise_steps(problem, malrule_num, malrule_den, result_num_digits, result_den_digits)

        # Return the malrule answer as a string "num:den"
        return Solution(
            answer=f"{malrule_num}:{malrule_den}",
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
