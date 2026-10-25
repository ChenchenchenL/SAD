"""
Testing framework for malrule implementations.

Provides utilities for testing problem generators, algorithms,
and validating malrule implementations.
"""

from typing import List, Dict, Any, Callable
from dataclasses import dataclass
from .malrule_base import (
    Problem, Solution, ProblemGenerator,
    Algorithm, Malrule, CorrectAlgorithm,
    MalruleComparison
)


@dataclass
class TestResult:
    """Results from a malrule test."""
    passed: bool
    message: str
    details: Dict[str, Any] = None

    def __post_init__(self):
        if self.details is None:
            self.details = {}


class MalruleTest:
    """
    Test suite for a malrule implementation.
    """

    def __init__(self, malrule: Malrule, correct_algo: CorrectAlgorithm,
                 problem_generator: ProblemGenerator):
        """
        Initialize test suite.

        Args:
            malrule: Malrule to test
            correct_algo: Correct algorithm for comparison
            problem_generator: Problem generator
        """
        self.malrule = malrule
        self.correct_algo = correct_algo
        self.problem_generator = problem_generator

    def test_generates_incorrect_answer(self, num_problems: int = 10) -> TestResult:
        """
        Test that malrule produces the expected incorrect answers.

        This test validates that:
        1. Malrule answer != correct answer
        2. Malrule answer == expected malrule answer (based on calculate_expected_answer)

        Args:
            num_problems: Number of test problems to generate

        Returns:
            TestResult indicating if malrule produces expected incorrect answers
        """
        mismatches = []

        for i in range(num_problems):
            problem = self.problem_generator.generate()
            correct_solution = self.correct_algo.solve(problem)
            malrule_solution = self.malrule.solve(problem)
            expected_malrule_answer = self.malrule.calculate_expected_answer(problem)

            # Normalize answers for comparison (convert to string for comparison)
            correct_answer_str = str(correct_solution.answer)
            malrule_answer_str = str(malrule_solution.answer)
            expected_malrule_str = str(expected_malrule_answer)

            # Check 1: Malrule should produce different answer than correct
            if correct_answer_str == malrule_answer_str:
                mismatches.append({
                    'problem_num': i + 1,
                    'error': 'Malrule produced same answer as correct algorithm',
                    'problem': problem.text,
                    'answer': malrule_answer_str,
                    'correct_steps': correct_solution.steps,
                    'malrule_steps': malrule_solution.steps
                })
                continue

            # Check 2: Malrule should produce the EXPECTED wrong answer
            if malrule_answer_str != expected_malrule_str:
                mismatches.append({
                    'problem_num': i + 1,
                    'error': 'Malrule answer does not match expected malrule answer',
                    'problem': problem.text,
                    'actual_malrule_answer': malrule_answer_str,
                    'expected_malrule_answer': expected_malrule_str,
                    'correct_answer': correct_answer_str,
                    'correct_steps': correct_solution.steps,
                    'malrule_steps': malrule_solution.steps
                })

        if mismatches:
            return TestResult(
                passed=False,
                message=f"Malrule validation failed on {len(mismatches)}/{num_problems} problems",
                details={'mismatches': mismatches[:3]}  # Show first 3 failures
            )

        return TestResult(
            passed=True,
            message=f"Malrule produced expected incorrect answers in {num_problems}/{num_problems} cases",
            details={
                'problems_tested': num_problems,
                'all_matched_expected': True
            }
        )

    def test_solution_has_steps(self) -> TestResult:
        """Test that solutions include step-by-step explanations."""
        problem = self.problem_generator.generate()
        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        if not malrule_solution.steps:
            return TestResult(
                passed=False,
                message="Malrule solution has no steps"
            )

        if not correct_solution.steps:
            return TestResult(
                passed=False,
                message="Correct solution has no steps"
            )

        return TestResult(
            passed=True,
            message="Both solutions include step-by-step explanations",
            details={
                'malrule_steps': len(malrule_solution.steps),
                'correct_steps': len(correct_solution.steps)
            }
        )

    def test_malrule_metadata(self) -> TestResult:
        """Test that malrule provides required metadata."""
        errors = []

        try:
            name = self.malrule.get_name()
            if not name or not isinstance(name, str):
                errors.append("Invalid name")
        except Exception as e:
            errors.append(f"get_name() error: {e}")

        try:
            description = self.malrule.get_description()
            if not description or not isinstance(description, str):
                errors.append("Invalid description")
        except Exception as e:
            errors.append(f"get_description() error: {e}")

        try:
            description = self.malrule.get_description()
            if not isinstance(description, str):
                errors.append("description must be a string")
        except Exception as e:
            errors.append(f"get_description() error: {e}")


        if errors:
            return TestResult(
                passed=False,
                message="Malrule metadata incomplete or invalid",
                details={'errors': errors}
            )

        return TestResult(
            passed=True,
            message="All required malrule metadata present and valid"
        )

    def test_problem_generator(self, num_problems: int = 10) -> TestResult:
        """
        Test that problem generator works correctly.

        Args:
            num_problems: Number of problems to generate and test

        Returns:
            TestResult
        """
        errors = []

        for i in range(num_problems):
            try:
                problem = self.problem_generator.generate(seed=i)

                if not problem.text:
                    errors.append(f"Problem {i}: No text")

                if not problem.operands:
                    errors.append(f"Problem {i}: No operands")

                if not problem.operation:
                    errors.append(f"Problem {i}: No operation")

            except Exception as e:
                errors.append(f"Problem {i}: Generation error: {e}")

        if errors:
            return TestResult(
                passed=False,
                message=f"Problem generator failed",
                details={'errors': errors[:5]}  # Limit to first 5 errors
            )

        return TestResult(
            passed=True,
            message=f"Successfully generated {num_problems} problems"
        )

    def test_deterministic_with_seed(self) -> TestResult:
        """Test that problem generation is deterministic when seed is provided."""
        problem1 = self.problem_generator.generate(seed=42)
        problem2 = self.problem_generator.generate(seed=42)

        if problem1.text != problem2.text or problem1.operands != problem2.operands:
            return TestResult(
                passed=False,
                message="Problem generation not deterministic with same seed",
                details={
                    'problem1': problem1.text,
                    'problem2': problem2.text
                }
            )

        return TestResult(
            passed=True,
            message="Problem generation is deterministic with seed"
        )

    def run_all_tests(self, verbose: bool = True) -> List[TestResult]:
        """
        Run all tests.

        Args:
            verbose: If True, print results as tests run

        Returns:
            List of TestResults
        """
        tests = [
            ("Problem Generator", self.test_problem_generator),
            ("Deterministic Generation", self.test_deterministic_with_seed),
            ("Malrule Metadata", self.test_malrule_metadata),
            ("Solution Steps", self.test_solution_has_steps),
            ("Incorrect Answers", self.test_generates_incorrect_answer),
        ]

        results = []
        for test_name, test_func in tests:
            if verbose:
                print(f"\nRunning: {test_name}...")

            result = test_func()
            results.append(result)

            if verbose:
                status = "✓ PASS" if result.passed else "✗ FAIL"
                print(f"  {status}: {result.message}")
                if result.details and not result.passed:
                    print(f"  Details: {result.details}")

        if verbose:
            print("\n" + "="*70)
            passed = sum(1 for r in results if r.passed)
            total = len(results)
            print(f"Tests passed: {passed}/{total}")
            print("="*70 + "\n")

        return results


class InteractiveDemo:
    """
    Interactive demonstration of a malrule vs correct algorithm.
    """

    def __init__(self, malrule: Malrule, correct_algo: CorrectAlgorithm,
                 problem_generator: ProblemGenerator):
        """
        Initialize interactive demo.

        Args:
            malrule: Malrule to demonstrate
            correct_algo: Correct algorithm for comparison
            problem_generator: Problem generator
        """
        self.malrule = malrule
        self.correct_algo = correct_algo
        self.problem_generator = problem_generator

    def run_single_comparison(self, seed: int = None) -> str:
        """
        Generate and compare a single problem.

        Args:
            seed: Optional seed for reproducibility

        Returns:
            Formatted comparison string
        """
        problem = self.problem_generator.generate(seed=seed)
        comparison = MalruleComparison.compare(problem, self.correct_algo, self.malrule)
        return MalruleComparison.format_comparison(comparison)

    def run_multiple_comparisons(self, count: int = 3) -> str:
        """
        Generate and compare multiple problems.

        Args:
            count: Number of problems to compare

        Returns:
            Formatted comparisons string
        """
        output = "\n\n"
        output += "╔" + "═"*68 + "╗\n"
        output += "║" + f"{'MALRULE DEMONSTRATION':^68}" + "║\n"
        output += "║" + f"{self.malrule.get_name():^68}" + "║\n"
        output += "╚" + "═"*68 + "╝\n\n"

        output += "\n"

        for i in range(count):
            output += self.run_single_comparison(seed=i)
            output += "\n"

        return output

    def show_malrule_info(self) -> str:
        """Display comprehensive malrule information."""
        output = "\n\n"
        output += "╔" + "═"*68 + "╗\n"
        output += "║" + f"{'MALRULE INFORMATION':^68}" + "║\n"
        output += "╚" + "═"*68 + "╝\n\n"

        output += f"Name: {self.malrule.get_name()}\n\n"
        output += f"Description:\n{self.malrule.get_description()}\n\n"

        return output
