"""
Correct algorithm for factoring quadratics.
"""

import sys
import math
sys.path.append('/home/user/malrule-coding')

from utils import CorrectAlgorithm, Problem, Solution


class QuadraticFactoringCorrectAlgorithm(CorrectAlgorithm):
    """Correctly factors quadratics with proper sign patterns."""

    def get_name(self):
        return "Correct Quadratic Factoring"

    def get_description(self):
        return "Factors quadratics by finding correct numbers AND using correct sign patterns"

    def _generate_concise_steps(self, quadratic_str, problem_type, a, b, c, correct_factored, **kwargs):
        """Generate concise steps with only formulas and values."""
        steps = []
        steps.append(f"Factor: {quadratic_str}")

        if problem_type == 'difference_of_squares':
            k = kwargs.get('k', 0)
            steps.append(f"x² - {k}² = (x - {k})(x + {k})")
        elif problem_type == 'perfect_square_trinomial':
            k = kwargs.get('k', 0)
            steps.append(f"x² ± 2({k})x + {k}² = (x ± {k})²")
        elif problem_type == 'leading_coefficient_not_one':
            p = kwargs.get('p', 0)
            q = kwargs.get('q', 0)
            steps.append(f"a × c = {a * c}")
            steps.append(f"({a}x + {p})(x + {q})")
        else:  # standard factoring
            p = kwargs.get('p', 0)
            q = kwargs.get('q', 0)
            sign_p = kwargs.get('sign_p', '+')
            sign_q = kwargs.get('sign_q', '+')
            if c > 0:
                steps.append(f"p × q = {abs(c)}, p + q = {abs(b)}")
            else:
                steps.append(f"p × q = {abs(c)}, |p - q| = {abs(b)}")
            steps.append(f"(x {sign_p} {p})(x {sign_q} {q})")

        steps.append(f"{correct_factored}")
        return steps

    def _generate_verbose_steps(self, quadratic_str, problem_type, a, b, c, correct_factored, **kwargs):
        """Generate verbose steps with full explanations (original format)."""
        steps = []
        steps.append(f"Problem: Factor {quadratic_str}")
        steps.append("")

        if problem_type == 'difference_of_squares':
            k = kwargs.get('k', 0)
            steps.append("CORRECT METHOD: Recognize difference of squares pattern")
            steps.append(f"  x² - {k**2} is a difference of squares")
            steps.append(f"  Pattern: a² - b² = (a - b)(a + b)")
            steps.append(f"  Here: x² - {k}² = (x - {k})(x + {k})")

        elif problem_type == 'perfect_square_trinomial':
            k = kwargs.get('k', 0)
            steps.append("CORRECT METHOD: Recognize perfect square trinomial")
            steps.append(f"  Pattern: x² ± 2kx + k² = (x ± k)²")
            steps.append(f"  Check: middle term = 2 × {k} × x = {2*k}x ✓")
            steps.append(f"  Check: last term = {k}² = {k**2} ✓")
            steps.append(f"  Therefore: {correct_factored}")

        elif problem_type == 'leading_coefficient_not_one':
            p = kwargs.get('p', 0)
            q = kwargs.get('q', 0)
            ac_product = a * c
            steps.append(f"CORRECT METHOD: Factor with a = {a} ≠ 1")
            steps.append(f"  Use trial and error or decomposition method")
            steps.append(f"  Look for factors of {a} × {c} = {ac_product} that add to {b}")
            steps.append(f"  Found: ({a}x + {p})(x + {q})")
            steps.append("")
            steps.append("Verify by expanding:")
            steps.append(f"  ({a}x + {p})(x + {q})")
            steps.append(f"  = {a}x² + {a*q}x + {p}x + {p*q}")
            steps.append(f"  = {a}x² + {a*q + p}x + {p*q}")
            steps.append(f"  = {quadratic_str} ✓")

        else:  # standard factoring
            p = kwargs.get('p', 0)
            q = kwargs.get('q', 0)
            sign_p = kwargs.get('sign_p', '+')
            sign_q = kwargs.get('sign_q', '+')

            steps.append("CORRECT METHOD: Find numbers and determine sign pattern")
            steps.append("")
            steps.append("Step 1: Identify coefficients")
            steps.append(f"  Middle term coefficient: b = {b}")
            steps.append(f"  Constant term: c = {c}")
            steps.append("")

            if c > 0 and b > 0:
                steps.append("Step 2: Find two numbers")
                steps.append(f"  Need: product = {c}, sum = {b}")
                steps.append(f"  Numbers: {p} and {q}")
                steps.append(f"  Check: {p} × {q} = {p*q}, {p} + {q} = {p+q}")
                steps.append("")
                steps.append("Step 3: Determine sign pattern")
                steps.append(f"  b > 0 and c > 0 → BOTH factors use +")
                steps.append(f"  (x + {p})(x + {q})")
                steps.append("")
                steps.append("Step 4: Verify by expanding")
                steps.append(f"  (x + {p})(x + {q})")
                steps.append(f"  = x² + {q}x + {p}x + {p*q}")
                steps.append(f"  = x² + {p+q}x + {p*q}")
                steps.append(f"  = {quadratic_str} ✓")

            elif c > 0 and b < 0:
                steps.append("Step 2: Find two numbers")
                steps.append(f"  Need: product = {c}, sum (magnitude) = {abs(b)}")
                steps.append(f"  Numbers: {p} and {q}")
                steps.append(f"  Check: {p} × {q} = {p*q}, {p} + {q} = {p+q}")
                steps.append("")
                steps.append("Step 3: Determine sign pattern")
                steps.append(f"  b < 0 and c > 0 → BOTH factors use -")
                steps.append(f"  (x - {p})(x - {q})")
                steps.append("")
                steps.append("Step 4: Verify by expanding")
                steps.append(f"  (x - {p})(x - {q})")
                steps.append(f"  = x² - {q}x - {p}x + {p*q}")
                steps.append(f"  = x² - {p+q}x + {p*q}")
                steps.append(f"  = {quadratic_str} ✓")

            else:  # c < 0
                steps.append("Step 2: Find two numbers")
                steps.append(f"  Need: product (magnitude) = {abs(c)}, difference = {abs(b)}")
                steps.append(f"  Numbers: {p} and {q}")
                steps.append(f"  Check: {p} × {q} = {p*q}, |{p} - {q}| = {abs(p-q)}")
                steps.append("")
                steps.append("Step 3: Determine sign pattern")
                steps.append(f"  c < 0 → ONE factor uses +, one uses -")
                steps.append(f"  Since b = {b}, the larger number gets the sign of b")
                steps.append(f"  {correct_factored}")
                steps.append("")
                steps.append("Step 4: Verify by expanding")
                steps.append(f"  {correct_factored}")
                steps.append(f"  = x² - {q}x + {p}x - {p*q}")
                steps.append(f"  = x² + {p-q}x - {p*q}")
                steps.append(f"  = {quadratic_str} ✓")

            steps.append("")
            steps.append(
                f"The key is understanding sign patterns: positive constant usually means "
                f"same signs, negative constant means different signs. Always verify by expanding!"
            )

        steps.append("")
        steps.append(f"Answer: {correct_factored}")

        return steps

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
        """Handle difference of squares problems: x² - k²."""
        # c should be negative, find k where k² = -c
        k_squared = -c
        k = int(math.sqrt(k_squared))

        # Verify it's a perfect square
        if k * k != k_squared:
            raise ValueError(f"Not a perfect square: {k_squared}")

        correct_factored = f"(x - {k})(x + {k})"

        steps = []
        steps.append(f"Problem: Factor {quadratic_str}")
        steps.append("")
        steps.append("CORRECT METHOD: Recognize difference of squares pattern")
        steps.append(f"  x² - {k_squared} is a difference of squares")
        steps.append(f"  Pattern: a² - b² = (a - b)(a + b)")
        steps.append(f"  Here: x² - {k}² = (x - {k})(x + {k})")
        steps.append("")
        steps.append(f"Answer: {correct_factored}")

        return Solution(
            answer=correct_factored,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _handle_perfect_square_trinomial(self, a, b, c, quadratic_str) -> Solution:
        """Handle perfect square trinomial: x² ± 2kx + k²."""
        # c = k², so find k
        k_squared = c
        k = int(math.sqrt(k_squared))

        # Verify it's a perfect square
        if k * k != k_squared:
            raise ValueError(f"Not a perfect square: {k_squared}")

        # Check if middle term matches 2k
        if abs(b) != 2 * k:
            raise ValueError(f"Middle term {b} doesn't match 2*{k} = {2*k}")

        # Determine sign from b
        if b > 0:
            correct_factored = f"(x + {k})²"
        else:
            correct_factored = f"(x - {k})²"

        steps = []
        steps.append(f"Problem: Factor {quadratic_str}")
        steps.append("")
        steps.append("CORRECT METHOD: Recognize perfect square trinomial")
        steps.append(f"  Pattern: x² ± 2kx + k² = (x ± k)²")
        steps.append(f"  Check: middle term = 2 × {k} × x = {2*k}x ✓")
        steps.append(f"  Check: last term = {k}² = {k_squared} ✓")
        steps.append(f"  Therefore: {correct_factored}")
        steps.append("")
        steps.append(f"Answer: {correct_factored}")

        return Solution(
            answer=correct_factored,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _handle_leading_coefficient_not_one(self, a, b, c, quadratic_str) -> Solution:
        """Handle factoring with leading coefficient ≠ 1: ax² + bx + c."""
        # Use AC method: find two numbers that multiply to a*c and add to b
        ac_product = a * c

        # Find factors of ac that add to b
        factors = self._find_factors(ac_product, b)

        if factors is None:
            raise ValueError(f"Cannot factor {quadratic_str}")

        m, n = factors

        # For (ax + p)(x + q), we have:
        # a*q + p = b
        # p*q = c
        # Try to find p and q
        # If a=2, b=7, c=3: (2x + 1)(x + 3)
        # We need p*q = c and a*q + p = b

        for p in range(1, abs(c) + 1):
            if c % p == 0:
                q = c // p
                if a * q + p == b:
                    correct_factored = f"({a}x + {p})(x + {q})"

                    steps = []
                    steps.append(f"Problem: Factor {quadratic_str}")
                    steps.append("")
                    steps.append(f"CORRECT METHOD: Factor with a = {a} ≠ 1")
                    steps.append(f"  Use trial and error or decomposition method")
                    steps.append(f"  Look for factors of {a} × {c} = {ac_product} that add to {b}")
                    steps.append(f"  Found: ({a}x + {p})(x + {q})")
                    steps.append("")
                    steps.append("Verify by expanding:")
                    steps.append(f"  ({a}x + {p})(x + {q})")
                    steps.append(f"  = {a}x² + {a*q}x + {p}x + {p*q}")
                    steps.append(f"  = {a}x² + {a*q + p}x + {p*q}")
                    steps.append(f"  = {quadratic_str} ✓")
                    steps.append("")
                    steps.append(f"Answer: {correct_factored}")

                    return Solution(
                        answer=correct_factored,
                        steps=steps,
                        is_correct=True,
                        algorithm_name=self.get_name()
                    )

        raise ValueError(f"Cannot factor {quadratic_str}")

    def _handle_standard_factoring(self, a, b, c, quadratic_str) -> Solution:
        """Handle standard factoring: x² + bx + c."""
        steps = []
        steps.append(f"Problem: Factor {quadratic_str}")
        steps.append("")
        steps.append("CORRECT METHOD: Find numbers and determine sign pattern")
        steps.append("")
        steps.append("Step 1: Identify coefficients")
        steps.append(f"  Middle term coefficient: b = {b}")
        steps.append(f"  Constant term: c = {c}")
        steps.append("")

        # Determine sign pattern based on b and c
        if c > 0 and b > 0:
            # both_positive: (x + p)(x + q) where p*q = c, p+q = b
            factors = self._find_factors(c, b)
            if factors is None:
                raise ValueError(f"Cannot find factors for c={c}, sum={b}")
            p, q = factors

            correct_factored = f"(x + {p})(x + {q})"

            steps.append("Step 2: Find two numbers")
            steps.append(f"  Need: product = {c}, sum = {b}")
            steps.append(f"  Numbers: {p} and {q}")
            steps.append(f"  Check: {p} × {q} = {p*q}, {p} + {q} = {p+q}")
            steps.append("")
            steps.append("Step 3: Determine sign pattern")
            steps.append(f"  b > 0 and c > 0 → BOTH factors use +")
            steps.append(f"  (x + {p})(x + {q})")
            steps.append("")
            steps.append("Step 4: Verify by expanding")
            steps.append(f"  (x + {p})(x + {q})")
            steps.append(f"  = x² + {q}x + {p}x + {p*q}")
            steps.append(f"  = x² + {p+q}x + {p*q}")
            steps.append(f"  = {quadratic_str} ✓")

        elif c > 0 and b < 0:
            # both_negative: (x - p)(x - q) where p*q = c, p+q = -b
            factors = self._find_factors(c, -b)
            if factors is None:
                raise ValueError(f"Cannot find factors for c={c}, sum={-b}")
            p, q = factors

            correct_factored = f"(x - {p})(x - {q})"

            steps.append("Step 2: Find two numbers")
            steps.append(f"  Need: product = {c}, sum (magnitude) = {abs(b)}")
            steps.append(f"  Numbers: {p} and {q}")
            steps.append(f"  Check: {p} × {q} = {p*q}, {p} + {q} = {p+q}")
            steps.append("")
            steps.append("Step 3: Determine sign pattern")
            steps.append(f"  b < 0 and c > 0 → BOTH factors use -")
            steps.append(f"  (x - {p})(x - {q})")
            steps.append("")
            steps.append("Step 4: Verify by expanding")
            steps.append(f"  (x - {p})(x - {q})")
            steps.append(f"  = x² - {q}x - {p}x + {p*q}")
            steps.append(f"  = x² - {p+q}x + {p*q}")
            steps.append(f"  = {quadratic_str} ✓")

        else:  # c < 0
            # one_negative: (x + p)(x - q) where p*q = -c
            # We need (x + p)(x - q) = x² + (p-q)x - pq
            # So p - q = b (if b >= 0, p > q; if b < 0, q > p)
            factors = self._find_factors_with_diff(-c, abs(b))
            if factors is None:
                raise ValueError(f"Cannot find factors for product={-c}, difference={abs(b)}")

            # factors returns (larger, smaller)
            larger, smaller = factors

            # Assign p and q based on the sign of b
            if b >= 0:
                # p - q = b, so p is larger
                p, q = larger, smaller
            else:
                # p - q = b (negative), so q is larger
                p, q = smaller, larger

            correct_factored = f"(x + {p})(x - {q})"

            steps.append("Step 2: Find two numbers")
            steps.append(f"  Need: product (magnitude) = {abs(c)}, difference = {abs(b)}")
            steps.append(f"  Numbers: {p} and {q}")
            steps.append(f"  Check: {p} × {q} = {p*q}, |{p} - {q}| = {abs(p-q)}")
            steps.append("")
            steps.append("Step 3: Determine sign pattern")
            steps.append(f"  c < 0 → ONE factor uses +, one uses -")
            steps.append(f"  Since b = {b}, the larger number gets the sign of b")
            steps.append(f"  {correct_factored}")
            steps.append("")
            steps.append("Step 4: Verify by expanding")
            steps.append(f"  {correct_factored}")
            steps.append(f"  = x² - {q}x + {p}x - {p*q}")
            steps.append(f"  = x² + {p-q}x - {p*q}")
            steps.append(f"  = {quadratic_str} ✓")

        steps.append("")
        steps.append(f"Answer: {correct_factored}")
        steps.append("")
        steps.append(
            f"The key is understanding sign patterns: positive constant usually means "
            f"same signs, negative constant means different signs. Always verify by expanding!"
        )

        return Solution(
            answer=correct_factored,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )

    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Apply correct quadratic factoring algorithm.

        Args:
            problem: The quadratic factoring problem
            verbose: If True, generate verbose steps; if False, generate concise steps (default)

        Returns:
            Solution showing correct factoring with proper signs
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

        # Determine the factoring method and correct answer based on problem characteristics
        if problem_type == 'difference_of_squares' or (a == 1 and b == 0 and c < 0):
            problem_type = 'difference_of_squares'
            k = int(math.sqrt(-c))
            correct_factored = f"(x - {k})(x + {k})"
            kwargs['k'] = k

        elif problem_type == 'perfect_square_trinomial':
            k = int(math.sqrt(c))
            if b > 0:
                correct_factored = f"(x + {k})²"
            else:
                correct_factored = f"(x - {k})²"
            kwargs['k'] = k

        elif problem_type == 'leading_coefficient_not_one' or a != 1:
            problem_type = 'leading_coefficient_not_one'
            # Find p and q for (ax + p)(x + q)
            p = problem.metadata.get('p', 0)
            q = problem.metadata.get('q', 0)
            if p == 0 or q == 0:
                # Try to find them
                for p_try in range(1, abs(c) + 1):
                    if c % p_try == 0:
                        q_try = c // p_try
                        if a * q_try + p_try == b:
                            p, q = p_try, q_try
                            break
            correct_factored = f"({a}x + {p})(x + {q})"
            kwargs['p'] = p
            kwargs['q'] = q

        else:  # Standard factoring
            problem_type = 'standard'
            if c > 0 and b > 0:
                factors = self._find_factors(c, b)
                p, q = factors if factors else (0, 0)
                correct_factored = f"(x + {p})(x + {q})"
                kwargs.update({'p': p, 'q': q, 'sign_p': '+', 'sign_q': '+'})
            elif c > 0 and b < 0:
                factors = self._find_factors(c, -b)
                p, q = factors if factors else (0, 0)
                correct_factored = f"(x - {p})(x - {q})"
                kwargs.update({'p': p, 'q': q, 'sign_p': '-', 'sign_q': '-'})
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
                correct_factored = f"(x + {p})(x - {q})"
                kwargs.update({'p': p, 'q': q, 'sign_p': '+', 'sign_q': '-'})

        # Generate steps based on verbose flag
        if verbose:
            steps = self._generate_verbose_steps(quadratic_str, problem_type, a, b, c, correct_factored, **kwargs)
        else:
            steps = self._generate_concise_steps(quadratic_str, problem_type, a, b, c, correct_factored, **kwargs)

        return Solution(
            answer=correct_factored,
            steps=steps,
            is_correct=True,
            algorithm_name=self.get_name()
        )
