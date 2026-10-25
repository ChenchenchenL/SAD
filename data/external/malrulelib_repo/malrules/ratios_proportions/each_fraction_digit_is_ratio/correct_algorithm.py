"""
Correct algorithm for simplifying ratios.
"""

import sys
sys.path.append('/home/user/malrule-coding')

from typing import List
from math import gcd
from utils import CorrectAlgorithm, Problem, Solution


class RatioSimplificationCorrectAlgorithm(CorrectAlgorithm):
    """Correctly simplifies ratios using GCD of complete numbers."""

    def get_name(self) -> str:
        return "Correct Ratio Simplification"

    def get_description(self) -> str:
        return "Correctly simplifies ratios by dividing both terms by their GCD."

    def _generate_concise_steps(self, problem: Problem, correct_num: int, correct_den: int, ratio_gcd: int) -> List[str]:
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

        steps.append(f"Formula: Find GCD and divide both terms")
        steps.append(f"Step 1: GCD({numerator}, {denominator}) = {ratio_gcd}")
        steps.append(f"Step 2: {numerator} ÷ {ratio_gcd} = {correct_num}")
        steps.append(f"Step 3: {denominator} ÷ {ratio_gcd} = {correct_den}")
        steps.append(f"Answer: {correct_num}:{correct_den}")
        return steps

    def _generate_verbose_steps(self, problem: Problem, correct_num: int, correct_den: int, ratio_gcd: int) -> List[str]:
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
            steps.append(f"  Ratio to simplify: {numerator}:{denominator}")
        else:
            steps.append(f"Problem: Simplify {numerator}:{denominator}")

        steps.append("")
        steps.append("CORRECT METHOD: Find GCD and divide both terms")
        steps.append("")

        steps.append(f"Step 1: Find the GCD of {numerator} and {denominator}")
        steps.append(f"  Method: Prime factorization or Euclidean algorithm")

        # Show prime factorization if numbers are small enough
        if numerator <= 100 and denominator <= 100:
            steps.append(f"  Factors of {numerator}: {self._get_factors(numerator)}")
            steps.append(f"  Factors of {denominator}: {self._get_factors(denominator)}")
            steps.append(f"  Common factors: {self._get_common_factors(numerator, denominator)}")

        steps.append(f"  GCD({numerator}, {denominator}) = {ratio_gcd}")
        steps.append("")

        steps.append(f"Step 2: Divide both terms by the GCD")
        steps.append(f"  {numerator} ÷ {ratio_gcd} = {correct_num}")
        steps.append(f"  {denominator} ÷ {ratio_gcd} = {correct_den}")
        steps.append("")

        steps.append(f"Step 3: Write simplified ratio")
        steps.append(f"  {numerator}:{denominator} = {correct_num}:{correct_den}")
        steps.append("")

        steps.append(f"Final Answer: {correct_num}:{correct_den} ✓")
        steps.append("")

        steps.append(f"Check: {correct_num} × {ratio_gcd} = {numerator} ✓")
        steps.append(f"       {correct_den} × {ratio_gcd} = {denominator} ✓")

        if gcd(correct_num, correct_den) == 1:
            steps.append(f"       GCD({correct_num}, {correct_den}) = 1 (fully simplified) ✓")

        return steps

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the correct ratio simplification algorithm.

        Args:
            problem: Problem instance with numerator and denominator
            verbose: If True, generate verbose explanatory steps; if False, generate concise steps

        Returns:
            Solution with correct answer and detailed steps
        """
        numerator = problem.metadata['numerator']
        denominator = problem.metadata['denominator']

        # CORRECT: Compute using GCD
        from math import gcd
        ratio_gcd = gcd(numerator, denominator)
        correct_num = numerator // ratio_gcd
        correct_den = denominator // ratio_gcd

        if verbose:
            steps = self._generate_verbose_steps(problem, correct_num, correct_den, ratio_gcd)
        else:
            steps = self._generate_concise_steps(problem, correct_num, correct_den, ratio_gcd)

        # Return the correct answer as a string "num:den"
        return Solution(
            answer=f"{correct_num}:{correct_den}",
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _get_factors(self, n: int) -> str:
        """Get all factors of n as a string."""
        factors = []
        for i in range(1, min(n + 1, 101)):
            if n % i == 0:
                factors.append(i)
        if n > 100:
            return f"[too many to list]"
        return ', '.join(str(f) for f in factors)

    def _get_common_factors(self, a: int, b: int) -> str:
        """Get common factors of a and b."""
        factors_a = set()
        factors_b = set()

        for i in range(1, min(a + 1, 101)):
            if a % i == 0:
                factors_a.add(i)

        for i in range(1, min(b + 1, 101)):
            if b % i == 0:
                factors_b.add(i)

        common = sorted(factors_a & factors_b)
        if not common or (a > 100 or b > 100):
            return str(gcd(a, b))

        return ', '.join(str(f) for f in common)
