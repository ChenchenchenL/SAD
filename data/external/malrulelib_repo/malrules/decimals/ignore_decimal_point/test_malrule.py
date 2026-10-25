#!/usr/bin/env python3
"""
Comprehensive test suite for Ignore-Decimal-Point malrule.

Tests all problem templates and validates that algorithms calculate solutions
instead of using metadata.
"""

import sys
import os
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel
from malrules.decimals.ignore_decimal_point import (
    IgnoreDecimalPointProblemGenerator,
    IgnoreDecimalPointMalrule,
    DecimalArithmeticCorrectAlgorithm
)


class TestIgnoreDecimalPoint(unittest.TestCase):
    """Comprehensive test cases for Ignore-Decimal-Point malrule."""

    def setUp(self):
        """Set up test fixtures."""
        self.generator = IgnoreDecimalPointProblemGenerator(
            level=5,
            difficulty=DifficultyLevel.MEDIUM
        )
        self.malrule = IgnoreDecimalPointMalrule()
        self.correct_algo = DecimalArithmeticCorrectAlgorithm()

    def test_all_templates(self):
        """Test all problem templates."""
        templates = self.generator.get_available_templates()
        print(f"\n{'='*70}")
        print(f"Testing {len(templates)} templates for Ignore-Decimal-Point malrule")
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

                # Remove currency symbols for comparison
                if correct_ans.startswith('$'):
                    correct_ans = correct_ans[1:]
                if malrule_ans.startswith('$'):
                    malrule_ans = malrule_ans[1:]

                # Check if malrule produces same answer as correct (edge case)
                if correct_ans == malrule_ans or float(correct_ans) == float(malrule_ans):
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
                    # Still pass the test but warn about the edge case
                    print(f"  Note: This is an edge case where the misconception")
                    print(f"        happens to produce the correct answer.")
                else:
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

                # Save original metadata answers
                original_correct = problem.metadata.get('correct_answer', '')
                original_malrule = problem.metadata.get('malrule_answer', '')

                # Solve with algorithms
                correct_solution = self.correct_algo.solve(problem)
                malrule_solution = self.malrule.solve(problem)

                # Calculate expected values manually
                num1 = problem.metadata['num1']
                num2 = problem.metadata['num2']
                operation = problem.metadata['operation']

                # Calculate expected correct answer
                if operation == 'multiplication':
                    expected_correct = round(num1 * num2, 2)
                elif operation == 'division':
                    expected_correct = round(num1 / num2, 2)
                elif operation == 'addition':
                    expected_correct = round(num1 + num2, 2)
                elif operation == 'subtraction':
                    expected_correct = round(num1 - num2, 2)
                else:
                    expected_correct = round(num1 * num2, 2)

                # Calculate expected malrule answer
                num1_as_int = int(str(num1).replace('.', ''))
                num2_as_int = int(str(num2).replace('.', ''))

                if operation == 'multiplication':
                    expected_malrule = num1_as_int * num2_as_int
                elif operation == 'division':
                    expected_malrule = num1_as_int // num2_as_int if num2_as_int != 0 else num1_as_int
                elif operation == 'addition':
                    expected_malrule = num1_as_int + num2_as_int
                elif operation == 'subtraction':
                    expected_malrule = num1_as_int - num2_as_int
                else:
                    expected_malrule = num1_as_int * num2_as_int

                # Verify correct algorithm calculated correctly
                correct_ans = correct_solution.answer
                if correct_ans.startswith('$'):
                    correct_ans = correct_ans[1:]
                self.assertAlmostEqual(float(correct_ans), float(expected_correct), places=1,
                                     msg=f"Correct algorithm failed for template {template}")

                # Verify malrule algorithm calculated correctly
                malrule_ans = malrule_solution.answer
                if malrule_ans.startswith('$'):
                    malrule_ans = malrule_ans[1:]
                self.assertEqual(int(float(malrule_ans)), expected_malrule,
                               msg=f"Malrule algorithm failed for template {template}")

                print(f"  ✓ Template '{template}': Algorithms calculating correctly")

    def test_specific_examples(self):
        """Test specific examples with known answers."""
        print(f"\n{'='*70}")
        print(f"Testing specific examples")
        print(f"{'='*70}")

        test_cases = [
            {
                'num1': 2.3, 'num2': 1.5, 'operation': 'multiplication',
                'expected_correct': 3.45, 'expected_malrule': 345,
                'description': '2.3 × 1.5'
            },
            {
                'num1': 3.5, 'num2': 2.3, 'operation': 'addition',
                'expected_correct': 5.8, 'expected_malrule': 58,
                'description': '3.5 + 2.3'
            },
            {
                'num1': 10.5, 'num2': 2.1, 'operation': 'division',
                'expected_correct': 5.0, 'expected_malrule': 5,
                'description': '10.5 ÷ 2.1 (edge case: same answer)'
            },
        ]

        for i, test in enumerate(test_cases):
            print(f"\n  Test case {i+1}: {test['description']}")

            # Create problem manually
            from utils import Problem
            problem = Problem(
                text=f"Calculate: {test['num1']} {test['operation']} {test['num2']}",
                operands=[test['num1'], test['num2']],
                operation=test['operation'],
                level=5,
                difficulty=DifficultyLevel.MEDIUM,
                metadata={
                    'num1': test['num1'],
                    'num2': test['num2'],
                    'operator': '×' if test['operation'] == 'multiplication' else '÷' if test['operation'] == 'division' else '+',
                    'operation': test['operation'],
                    'template': 'test'
                }
            )

            correct_solution = self.correct_algo.solve(problem)
            malrule_solution = self.malrule.solve(problem)

            # Check if it's an edge case
            if abs(float(correct_solution.answer) - float(malrule_solution.answer)) < 0.01:
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

                self.assertAlmostEqual(float(correct_solution.answer), test['expected_correct'], places=1)
                self.assertEqual(int(float(malrule_solution.answer)), test['expected_malrule'])


def main():
    """Main entry point for standalone execution."""
    print("\n╔" + "═"*68 + "╗")
    print("║" + "  TEST SUITE: Ignore-Decimal-Point Malrule  ".center(70) + "║")
    print("╚" + "═"*68 + "╝")

    # Run unittest
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestIgnoreDecimalPoint)
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
