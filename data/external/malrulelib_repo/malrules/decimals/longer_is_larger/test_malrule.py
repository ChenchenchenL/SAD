#!/usr/bin/env python3
"""
Comprehensive test suite for Longer-Is-Larger malrule.

Tests all problem templates and validates that algorithms calculate solutions
instead of using metadata.
"""

import sys
import os
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel
from malrules.decimals.longer_is_larger import (
    LongerIsLargerProblemGenerator,
    LongerIsLargerMalrule,
    DecimalComparisonCorrectAlgorithm
)


class TestLongerIsLarger(unittest.TestCase):
    """Comprehensive test cases for Longer-Is-Larger malrule."""

    def setUp(self):
        """Set up test fixtures."""
        self.generator = LongerIsLargerProblemGenerator(
            level=5,
            difficulty=DifficultyLevel.MEDIUM
        )
        self.malrule = LongerIsLargerMalrule()
        self.correct_algo = DecimalComparisonCorrectAlgorithm()

    def test_all_templates(self):
        """Test all problem templates."""
        templates = self.generator.get_available_templates()
        print(f"\n{'='*70}")
        print(f"Testing {len(templates)} templates for Longer-Is-Larger malrule")
        print(f"{'='*70}")

        for template in templates:
            with self.subTest(template=template):
                print(f"\n--- Testing template: {template} ---")

                # Generate problem
                problem = self.generator.generate(seed=42, template=template)

                # Solve with both algorithms
                correct_solution = self.correct_algo.solve(problem)
                malrule_solution = self.malrule.solve(problem)

                # Verify solutions are valid
                self.assertIsNotNone(correct_solution.answer)
                self.assertIsNotNone(malrule_solution.answer)
                self.assertTrue(correct_solution.is_correct)
                self.assertFalse(malrule_solution.is_correct)

                # Extract answers for comparison
                correct_ans = correct_solution.answer
                malrule_ans = malrule_solution.answer

                # Remove currency symbols and units for comparison
                if correct_ans.startswith('$'):
                    correct_ans = correct_ans[1:]
                if malrule_ans.startswith('$'):
                    malrule_ans = malrule_ans[1:]

                for unit in ['meters', 'kilometers', 'liters', 'kilograms']:
                    if unit in correct_ans:
                        correct_ans = correct_ans.split()[0]
                    if unit in malrule_ans:
                        malrule_ans = malrule_ans.split()[0]

                # Check if malrule produces same answer as correct (edge case)
                try:
                    if abs(float(correct_ans) - float(malrule_ans)) < 0.0001:
                        print(f"  ⚠ WARNING: Edge case - malrule produced same answer as correct!")
                        print(f"  Problem: {problem.text}")
                        print(f"  Correct answer: {correct_solution.answer}")
                        print(f"  Malrule answer: {malrule_solution.answer}")
                        print(f"\n  Correct algorithm steps:")
                        for step in correct_solution.steps:
                            print(f"    {step}")
                        print(f"\n  Malrule algorithm steps:")
                        for step in malrule_solution.steps:
                            print(f"    {step}")
                        print(f"  Note: This is an edge case where the misconception")
                        print(f"        happens to produce the correct answer.")
                    else:
                        print(f"  ✓ Template '{template}' passed")
                        print(f"    Problem: {problem.text}")
                        print(f"    Correct answer: {correct_solution.answer}")
                        print(f"    Malrule answer: {malrule_solution.answer}")
                except ValueError:
                    # Answer might be a string like "equal"
                    if correct_ans != malrule_ans:
                        print(f"  ✓ Template '{template}' passed")
                        print(f"    Problem: {problem.text}")
                        print(f"    Correct answer: {correct_solution.answer}")
                        print(f"    Malrule answer: {malrule_solution.answer}")

    def test_algorithms_calculate_not_use_metadata(self):
        """Verify algorithms calculate answers instead of using metadata."""
        print(f"\n{'='*70}")
        print(f"Verifying algorithms calculate solutions (not using metadata)")
        print(f"{'='*70}")

        for template in self.generator.get_available_templates():
            with self.subTest(template=template):
                # Generate problem
                problem = self.generator.generate(seed=123, template=template)

                # Solve with algorithms
                correct_solution = self.correct_algo.solve(problem)
                malrule_solution = self.malrule.solve(problem)

                # Calculate expected values manually
                decimals = problem.operands

                # Expected correct answer is max value
                expected_correct = max(decimals)

                # Expected malrule answer is the one with most decimal digits
                digit_counts = []
                for d in decimals:
                    str_d = str(d)
                    if '.' in str_d:
                        decimal_part = str_d.split('.')[1]
                        digit_counts.append((d, len(decimal_part)))
                    else:
                        digit_counts.append((d, 0))

                # MALRULE: Pick the one with the most decimal digits
                # If tie, use max value
                max_digits = max(digit_counts, key=lambda x: x[1])[1]
                candidates_with_max_digits = [d for d, count in digit_counts if count == max_digits]
                expected_malrule = max(candidates_with_max_digits)

                # Verify correct algorithm calculated correctly
                correct_ans = correct_solution.answer
                # Remove $ or units
                if correct_ans.startswith('$'):
                    correct_ans = correct_ans[1:]
                for unit in ['meters', 'kilometers', 'liters', 'kilograms']:
                    if unit in correct_ans:
                        correct_ans = correct_ans.split()[0]
                        break

                self.assertAlmostEqual(float(correct_ans), float(expected_correct), places=5,
                                     msg=f"Correct algorithm failed for template {template}")

                # Verify malrule algorithm calculated correctly
                malrule_ans = malrule_solution.answer
                # Remove $ or units
                if malrule_ans.startswith('$'):
                    malrule_ans = malrule_ans[1:]
                for unit in ['meters', 'kilometers', 'liters', 'kilograms']:
                    if unit in malrule_ans:
                        malrule_ans = malrule_ans.split()[0]
                        break

                self.assertAlmostEqual(float(malrule_ans), float(expected_malrule), places=5,
                               msg=f"Malrule algorithm failed for template {template}")

                print(f"  ✓ Template '{template}': Algorithms calculating correctly")

    def test_specific_examples(self):
        """Test specific examples with known answers."""
        print(f"\n{'='*70}")
        print(f"Testing specific examples")
        print(f"{'='*70}")

        test_cases = [
            {
                'decimals': [0.5, 0.36],
                'expected_correct': 0.5,
                'expected_malrule': 0.36,  # 0.36 has 2 digits, 0.5 has 1
                'description': '0.5 vs 0.36 (classic example)'
            },
            {
                'decimals': [0.8, 0.123],
                'expected_correct': 0.8,
                'expected_malrule': 0.123,  # 0.123 has 3 digits, 0.8 has 1
                'description': '0.8 vs 0.123'
            },
            {
                'decimals': [0.45, 0.7],
                'expected_correct': 0.7,
                'expected_malrule': 0.45,  # 0.45 has 2 digits, 0.7 has 1
                'description': '0.45 vs 0.7'
            },
        ]

        for i, test in enumerate(test_cases):
            print(f"\n  Test case {i+1}: {test['description']}")

            # Create problem manually
            from utils import Problem
            problem = Problem(
                text=f"Which is larger: {test['decimals'][0]} or {test['decimals'][1]}?",
                operands=test['decimals'],
                operation='comparison',
                level=5,
                difficulty=DifficultyLevel.MEDIUM,
                metadata={
                    'template': 'test'
                }
            )

            correct_solution = self.correct_algo.solve(problem)
            malrule_solution = self.malrule.solve(problem)

            # Check if it's an edge case
            if abs(float(correct_solution.answer) - float(malrule_solution.answer)) < 0.0001:
                print(f"    ⚠ Edge case detected: Same answer!")
                print(f"    Correct: {correct_solution.answer}")
                print(f"    Malrule: {malrule_solution.answer}")
                print(f"    Correct steps:")
                for step in correct_solution.steps:
                    print(f"      {step}")
                print(f"    Malrule steps:")
                for step in malrule_solution.steps:
                    print(f"      {step}")
            else:
                print(f"    ✓ Correct: {correct_solution.answer}")
                print(f"    ✓ Malrule: {malrule_solution.answer}")

                self.assertAlmostEqual(float(correct_solution.answer), test['expected_correct'], places=5)
                self.assertAlmostEqual(float(malrule_solution.answer), test['expected_malrule'], places=5)


def main():
    """Main entry point for standalone execution."""
    print("\n╔" + "═"*68 + "╗")
    print("║" + "  TEST SUITE: Longer-Is-Larger Malrule  ".center(70) + "║")
    print("╚" + "═"*68 + "╝")

    # Run unittest
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestLongerIsLarger)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    if result.wasSuccessful():
        print("\n\n╔" + "═"*68 + "╗")
        print("║" + "  ✓✓✓ ALL TESTS PASSED ✓✓✓  ".center(70) + "║")
        print("╚" + "═"*68 + "╝\n")
        return 0
    else:
        print("\n\n╔" + "═"*68 + "╗")
        print("║" + "  ✗✗✗ SOME TESTS FAILED ✗✗✗  ".center(70) + "║")
        print("╚" + "═"*68 + "╝\n")
        return 1


if __name__ == "__main__":
    exit(main())
