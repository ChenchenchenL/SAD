"""
Malrule algorithm for Sign-Errors-In-Factoring.

Students make sign errors when factoring quadratics, especially in decomposition method.
"""

import sys
import math
import random
sys.path.append('/home/user/malrule-coding')

from utils import Malrule, Problem, Solution

class SignErrorsInFactoringMalrule(Malrule):
    """Student makes sign errors when factoring quadratics."""

    def get_name(self):
        return "Sign-Errors-In-Factoring"

    def _generate_concise_steps(self, quadratic_str, problem_type, a, b, c, malrule_factored, **kwargs):
        """Generate concise steps with only formulas and values."""
        steps = []
        steps.append(f"Factor: {quadratic_str}")

        if problem_type == 'difference_of_squares':
            k = kwargs.get('k', 0)
            steps.append(f"x² - {k**2} pattern recognized")
            steps.append(f"Wrong sign: (x + {k})(x + {k})")
        elif problem_type == 'perfect_square_trinomial':
            k = kwargs.get('k', 0)
            steps.append(f"Perfect square pattern recognized")
            steps.append(f"Wrong sign used")
        elif problem_type == 'leading_coefficient_not_one':
            p = kwargs.get('p', 0)
            q = kwargs.get('q', 0)
            steps.append(f"Numbers: {p} and {q}")
            steps.append(f"Wrong sign pattern applied")
        else:  # standard factoring
            p = kwargs.get('p', 0)
            q = kwargs.get('q', 0)
            if c > 0:
                steps.append(f"p × q = {c}, p + q = {abs(b)}")
            else:
                steps.append(f"p × q = {abs(c)}, numbers found")
            steps.append(f"Wrong sign pattern applied")

        steps.append(f"{malrule_factored}")
        return steps

    def _generate_verbose_steps(self, quadratic_str, problem_type, a, b, c, malrule_factored, **kwargs):
        """Generate verbose steps with full explanations (original format)."""
        steps = []
        steps.append(f"Problem: Factor {quadratic_str}")
        steps.append("")

        if problem_type == 'difference_of_squares':
            k = kwargs.get('k', 0)
            steps.append("MALRULE: Student uses wrong signs in difference of squares")
            steps.append(f"  Student recognizes x² - {k**2} pattern")
            steps.append(f"  But uses wrong sign combination")
            steps.append(f"  Student's answer: {malrule_factored}")
            steps.append("")
            steps.append("The student didn't remember that a² - b² = (a-b)(a+b) requires ONE minus and ONE plus.")

        elif problem_type == 'perfect_square_trinomial':
            k = kwargs.get('k', 0)
            steps.append("MALRULE: Student uses wrong sign in perfect square")
            steps.append(f"  Student recognizes perfect square pattern")
            steps.append(f"  But uses opposite sign")
            steps.append(f"  Student's answer: {malrule_factored}")
            steps.append("")
            steps.append("The student didn't match the sign of the middle term.")

        elif problem_type == 'leading_coefficient_not_one':
            p = kwargs.get('p', 0)
            q = kwargs.get('q', 0)
            steps.append(f"MALRULE: Student uses wrong signs with a = {a}")
            steps.append(f"  Student finds correct numbers: {p} and {q}")
            steps.append(f"  But applies wrong sign pattern")
            steps.append(f"  Student's answer: {malrule_factored}")
            steps.append("")
            steps.append("The student didn't check their work by expanding.")

        else:  # standard factoring
            p = kwargs.get('p', 0)
            q = kwargs.get('q', 0)

            if c > 0 and b > 0:
                steps.append(f"Find two numbers that multiply to {c} and add to {b}")
                steps.append(f"  Numbers: {p} and {q}")
                steps.append(f"  Check: {p} × {q} = {p*q}, {p} + {q} = {p+q}")
                steps.append("")
                steps.append("MALRULE: Student uses wrong sign pattern")
                steps.append(f"  Student sees positive constant ({c})")
                steps.append(f"  But uses BOTH NEGATIVE signs incorrectly")
                steps.append(f"  Factors as: {malrule_factored}")
            elif c > 0 and b < 0:
                steps.append(f"Find two numbers that multiply to {c} and add to {abs(b)}")
                steps.append(f"  Numbers: {p} and {q}")
                steps.append(f"  Check: {p} × {q} = {p*q}, {p} + {q} = {p+q}")
                steps.append("")
                steps.append("MALRULE: Student uses wrong sign pattern")
                steps.append(f"  Student sees negative middle term (-{abs(b)}x)")
                steps.append(f"  But uses BOTH POSITIVE signs incorrectly")
                steps.append(f"  Factors as: {malrule_factored}")
            else:  # c < 0
                steps.append(f"Find two numbers that multiply to {abs(c)}")
                steps.append(f"  Numbers: {p} and {q}")
                steps.append(f"  Check: {p} × {q} = {p*q}")
                steps.append("")
                steps.append("MALRULE: Student swaps which factor gets the negative sign")
                steps.append(f"  Factors as: {malrule_factored}")

            steps.append("")
            steps.append(f"Student's answer: {malrule_factored}")
            steps.append("")
            steps.append(
                f"The student found the correct numbers but used the "
                f"wrong sign pattern. They didn't check their work by expanding, "
                f"which would reveal the sign error."
            )

        return steps

    def get_description(self):
        return (
            "Students make sign errors when factoring quadratics, selecting incorrect signs "
            "for the binomial factors. This is classified as a procedural error involving "
            "mishandling of signs (Tendere & Mutambara, 2020). Research indicates this is "
            "one of the most common errors in quadratic equation solving, with students "
            "finding the correct factor magnitudes but applying incorrect sign patterns."
        )

    def calculate_expected_answer(self, problem: Problem):
        """Calculate the expected malrule answer (incorrect) for this problem."""
        # Use the malrule logic to compute the answer
        solution = self._apply_malrule(problem)
        return solution.answer

    def _find_factors(self, product, sum_val):
        """
        Find two positive integers p and q such that p*q = product and p+q = sum_val.
        Returns (p, q) or None if not found.
        """
        product = abs(product)
        sum_val = abs(sum_val)

        for p in range(1, product + 1):
            if product % p == 0:
                q = product // p
                if p + q == sum_val:
                    return (p, q)

        return None

    def _find_factors_with_diff(self, product, diff_val):
        """
        Find two positive integers p and q such that p*q = product and |p-q| = diff_val.
        Returns (p, q) where p >= q, or None if not found.
        """
        product = abs(product)
        diff_val = abs(diff_val)

        for p in range(1, product + 1):
            if product % p == 0:
                q = product // p
                if abs(p - q) == diff_val:
                    # Return with p as the larger value
                    if p >= q:
                        return (p, q)
                    else:
                        return (q, p)

        return None

    def _handle_difference_of_squares(self, a, b, c, quadratic_str) -> Solution:
        """Handle difference of squares with malrule: use wrong sign combination."""
        # c should be negative, find k where k² = -c
        k_squared = -c
        k = int(math.sqrt(k_squared))

        # Verify it's a perfect square
        if k * k != k_squared:
            raise ValueError(f"Not a perfect square: {k_squared}")

        # MALRULE: Use both positive instead of one of each (most common student error)
        malrule_factored = f"(x + {k})(x + {k})"

        steps = []
        steps.append(f"Problem: Factor {quadratic_str}")
        steps.append("")
        steps.append("MALRULE: Student uses wrong signs in difference of squares")
        steps.append(f"  Student recognizes x² - {k_squared} pattern")
        steps.append(f"  But uses wrong sign combination")
        steps.append(f"  Student's answer: {malrule_factored}")
        steps.append("")
        steps.append("The student didn't remember that a² - b² = (a-b)(a+b) requires ONE minus and ONE plus.")

        return Solution(
            answer=malrule_factored,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _handle_perfect_square_trinomial(self, a, b, c, quadratic_str) -> Solution:
        """Handle perfect square trinomial with malrule: use opposite sign."""
        # c = k², so find k
        k_squared = c
        k = int(math.sqrt(k_squared))

        # Verify it's a perfect square
        if k * k != k_squared:
            raise ValueError(f"Not a perfect square: {k_squared}")

        # Check if middle term matches 2k
        if abs(b) != 2 * k:
            raise ValueError(f"Middle term {b} doesn't match 2*{k} = {2*k}")

        # MALRULE: Use opposite sign from what b indicates
        if b > 0:
            malrule_factored = f"(x - {k})²"  # Should be +, but student uses -
        else:
            malrule_factored = f"(x + {k})²"  # Should be -, but student uses +

        steps = []
        steps.append(f"Problem: Factor {quadratic_str}")
        steps.append("")
        steps.append("MALRULE: Student uses wrong sign in perfect square")
        steps.append(f"  Student recognizes perfect square pattern")
        steps.append(f"  But uses opposite sign")
        steps.append(f"  Student's answer: {malrule_factored}")
        steps.append("")
        steps.append("The student didn't match the sign of the middle term.")

        return Solution(
            answer=malrule_factored,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _handle_leading_coefficient_not_one(self, a, b, c, quadratic_str) -> Solution:
        """Handle leading coefficient ≠ 1 with malrule: use wrong signs."""
        # Find the correct factorization first
        for p in range(1, abs(c) + 1):
            if c % p == 0:
                q = c // p
                if a * q + p == b:
                    # Found correct factors, now apply MALRULE: flip all signs
                    malrule_factored = f"({a}x - {p})(x - {q})"

                    steps = []
                    steps.append(f"Problem: Factor {quadratic_str}")
                    steps.append("")
                    steps.append(f"MALRULE: Student uses wrong signs with a = {a}")
                    steps.append(f"  Student finds correct numbers: {p} and {q}")
                    steps.append(f"  But applies wrong sign pattern")
                    steps.append(f"  Student's answer: {malrule_factored}")
                    steps.append("")
                    steps.append("The student didn't check their work by expanding.")

                    return Solution(
                        answer=malrule_factored,
                        steps=steps,
                        is_correct=False,
                        algorithm_name=self.get_name()
                    )

        raise ValueError(f"Cannot factor {quadratic_str}")

    def _handle_standard_factoring(self, a, b, c, quadratic_str) -> Solution:
        """Handle standard factoring with malrule: apply sign errors."""
        steps = []
        steps.append(f"Problem: Factor {quadratic_str}")
        steps.append("")

        # Determine sign pattern based on b and c (same as correct algorithm)
        if c > 0 and b > 0:
            # Correct would be: both_positive (x + p)(x + q)
            factors = self._find_factors(c, b)
            if factors is None:
                raise ValueError(f"Cannot find factors for c={c}, sum={b}")
            p, q = factors

            # MALRULE: Student uses both negative instead
            malrule_factored = f"(x - {p})(x - {q})"

            steps.append(f"Find two numbers that multiply to {c} and add to {b}")
            steps.append(f"  Numbers: {p} and {q}")
            steps.append(f"  Check: {p} × {q} = {p*q}, {p} + {q} = {p+q}")
            steps.append("")
            steps.append("MALRULE: Student uses wrong sign pattern")
            steps.append(f"  Student sees positive constant ({c})")
            steps.append(f"  But uses BOTH NEGATIVE signs incorrectly")
            steps.append(f"  Factors as: {malrule_factored}")

        elif c > 0 and b < 0:
            # Correct would be: both_negative (x - p)(x - q)
            factors = self._find_factors(c, -b)
            if factors is None:
                raise ValueError(f"Cannot find factors for c={c}, sum={-b}")
            p, q = factors

            # MALRULE: Student uses both positive instead
            malrule_factored = f"(x + {p})(x + {q})"

            steps.append(f"Find two numbers that multiply to {c} and add to {abs(b)}")
            steps.append(f"  Numbers: {p} and {q}")
            steps.append(f"  Check: {p} × {q} = {p*q}, {p} + {q} = {p+q}")
            steps.append("")
            steps.append("MALRULE: Student uses wrong sign pattern")
            steps.append(f"  Student sees negative middle term (-{abs(b)}x)")
            steps.append(f"  But uses BOTH POSITIVE signs incorrectly")
            steps.append(f"  Factors as: {malrule_factored}")

        else:  # c < 0
            # Correct would be: one_negative (x + p)(x - q)
            factors = self._find_factors_with_diff(-c, abs(b))
            if factors is None:
                raise ValueError(f"Cannot find factors for product={-c}, difference={abs(b)}")

            # factors returns (larger, smaller)
            larger, smaller = factors

            # Determine correct assignment based on b
            if b >= 0:
                # Correct: p is larger
                p, q = larger, smaller
            else:
                # Correct: q is larger
                p, q = smaller, larger

            # MALRULE: Swap the signs
            malrule_factored = f"(x - {p})(x + {q})"

            steps.append(f"Find two numbers that multiply to {abs(c)}")
            steps.append(f"  Numbers: {p} and {q}")
            steps.append(f"  Check: {p} × {q} = {p*q}")
            steps.append("")
            steps.append("MALRULE: Student swaps which factor gets the negative sign")
            steps.append(f"  Factors as: {malrule_factored}")

        steps.append("")
        steps.append(f"Student's answer: {malrule_factored}")
        steps.append("")
        steps.append(
            f"The student found the correct numbers but used the "
            f"wrong sign pattern. They didn't check their work by expanding, "
            f"which would reveal the sign error."
        )

        return Solution(
            answer=malrule_factored,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )

    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply the sign-errors-in-factoring malrule.

        Args:
            problem: The quadratic factoring problem
            verbose: If True, generate verbose steps; if False, generate concise steps (default)

        Returns:
            Solution showing incorrect sign usage
        """
        # Extract coefficients from operands (they should be [a, b, c])
        if len(problem.operands) >= 3:
            a, b, c = problem.operands[0], problem.operands[1], problem.operands[2]
        else:
            a = problem.metadata.get('a', 1)
            b = problem.metadata.get('b', 0)
            c = problem.metadata.get('c', 0)

        # Get quadratic string from metadata for display
        quadratic_str = problem.metadata.get('quadratic', f"{a}x² + {b}x + {c}")

        # Get problem type to determine which method to use
        problem_type = problem.metadata.get('problem_type', None)

        kwargs = {}

        # Determine the malrule answer and kwargs based on problem characteristics
        if problem_type == 'difference_of_squares' or (a == 1 and b == 0 and c < 0):
            problem_type = 'difference_of_squares'
            k = int(math.sqrt(-c))
            malrule_factored = f"(x + {k})(x + {k})"
            kwargs['k'] = k

        elif problem_type == 'perfect_square_trinomial':
            k = int(math.sqrt(c))
            if b > 0:
                malrule_factored = f"(x - {k})²"
            else:
                malrule_factored = f"(x + {k})²"
            kwargs['k'] = k

        elif problem_type == 'leading_coefficient_not_one' or a != 1:
            problem_type = 'leading_coefficient_not_one'
            # Find the correct factors then flip signs for malrule
            for p in range(1, abs(c) + 1):
                if c % p == 0:
                    q = c // p
                    if a * q + p == b:
                        malrule_factored = f"({a}x - {p})(x - {q})"
                        kwargs.update({'p': p, 'q': q})
                        break

        else:  # Standard factoring
            problem_type = 'standard'
            if c > 0 and b > 0:
                factors = self._find_factors(c, b)
                p, q = factors if factors else (0, 0)
                malrule_factored = f"(x - {p})(x - {q})"
                kwargs.update({'p': p, 'q': q})
            elif c > 0 and b < 0:
                factors = self._find_factors(c, -b)
                p, q = factors if factors else (0, 0)
                malrule_factored = f"(x + {p})(x + {q})"
                kwargs.update({'p': p, 'q': q})
            else:  # c < 0
                factors = self._find_factors_with_diff(-c, abs(b))
                if factors:
                    larger, smaller = factors
                    if b >= 0:
                        p, q = larger, smaller
                    else:
                        p, q = smaller, larger
                else:
                    p, q = 0, 0
                malrule_factored = f"(x - {p})(x + {q})"
                kwargs.update({'p': p, 'q': q})

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(quadratic_str, problem_type, a, b, c, malrule_factored, **kwargs)
        else:
            steps = self._generate_concise_steps(quadratic_str, problem_type, a, b, c, malrule_factored, **kwargs)

        return Solution(
            answer=malrule_factored,
            steps=steps,
            is_correct=False,
            algorithm_name=self.get_name()
        )
