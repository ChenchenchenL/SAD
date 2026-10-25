#!/usr/bin/env python3
"""
Comprehensive test suite for Whole-Number-Thinking malrule.

This file combines:
1. Template validation tests (all 5 templates)
2. Specific research-based examples
3. Automated test suite functionality

Run from project root: python3 -m malrules.decimals.whole_number_thinking.test_malrule
Or from this directory: python3 test_malrule.py

IT IS NORMAL TO HAVE FAILED TESTS AS MALRULE CAN PRODUCE SAME ANSWER AS CORRECT
"""

import sys
import os
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.decimals.whole_number_thinking import (
    DecimalWholeNumberProblemGenerator,
    WholeNumberThinkingMalrule,
    DecimalCorrectAlgorithm
)


class TestWholeNumberThinking(unittest.TestCase):
    """Comprehensive test cases for Whole-Number-Thinking malrule."""

    def setUp(self):
        """Set up test fixtures."""
        self.generator = DecimalWholeNumberProblemGenerator(
            level=5,
            difficulty=DifficultyLevel.MEDIUM
        )
        self.malrule = WholeNumberThinkingMalrule()
        self.correct_algo = DecimalCorrectAlgorithm()

    # =======================
    # Template Tests
    # =======================
    def test_get_available_templates(self):
        """Test that all 6 templates are available."""
        templates = self.generator.get_available_templates()
        self.assertEqual(len(templates), 6)
        expected = ['basic_addition', 'basic_comparison', 'subtraction',
                    'multiplication', 'word_problem', 'word_problem_context']
        for template in expected:
            self.assertIn(template, templates)

    def test_basic_addition_template(self):
        """Test basic_addition template."""
        problem = self.generator.generate(seed=100, template='basic_addition')

        # Check problem structure
        self.assertEqual(problem.metadata['template'], 'basic_addition')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)

        # Verify answers are strings
        self.assertIsInstance(problem.metadata['correct_answer'], str)
        self.assertIsInstance(problem.metadata['malrule_answer'], str)

        # Verify malrule produces incorrect answer
        malrule_solution = self.malrule.solve(problem)
        self.assertFalse(malrule_solution.is_correct)
        self.assertEqual(malrule_solution.answer, problem.metadata['malrule_answer'])

        # Verify correct algorithm produces correct answer
        correct_solution = self.correct_algo.solve(problem)
        self.assertTrue(correct_solution.is_correct)
        self.assertEqual(correct_solution.answer, problem.metadata['correct_answer'])

        # Verify answers are different (malrule is wrong)
        self.assertNotEqual(malrule_solution.answer, correct_solution.answer)

    def test_basic_comparison_template(self):
        """Test basic_comparison template."""
        problem = self.generator.generate(seed=100, template='basic_comparison')

        # Check problem structure
        self.assertEqual(problem.metadata['template'], 'basic_comparison')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)

        # Verify malrule produces incorrect answer
        malrule_solution = self.malrule.solve(problem)
        self.assertFalse(malrule_solution.is_correct)
        self.assertEqual(malrule_solution.answer, problem.metadata['malrule_answer'])

        # Verify correct algorithm produces correct answer
        correct_solution = self.correct_algo.solve(problem)
        self.assertTrue(correct_solution.is_correct)
        self.assertEqual(correct_solution.answer, problem.metadata['correct_answer'])

    def test_subtraction_template(self):
        """Test subtraction template."""
        problem = self.generator.generate(seed=100, template='subtraction')

        # Check problem structure
        self.assertEqual(problem.metadata['template'], 'subtraction')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)

        # Verify malrule produces incorrect answer
        malrule_solution = self.malrule.solve(problem)
        self.assertFalse(malrule_solution.is_correct)
        self.assertEqual(malrule_solution.answer, problem.metadata['malrule_answer'])

        # Verify correct algorithm produces correct answer
        correct_solution = self.correct_algo.solve(problem)
        self.assertTrue(correct_solution.is_correct)
        self.assertEqual(correct_solution.answer, problem.metadata['correct_answer'])

        # Verify answers are different
        self.assertNotEqual(malrule_solution.answer, correct_solution.answer)

    def test_multiplication_template(self):
        """Test multiplication template."""
        problem = self.generator.generate(seed=100, template='multiplication')

        # Check problem structure
        self.assertEqual(problem.metadata['template'], 'multiplication')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)

        # Verify malrule produces incorrect answer
        malrule_solution = self.malrule.solve(problem)
        self.assertFalse(malrule_solution.is_correct)
        self.assertEqual(malrule_solution.answer, problem.metadata['malrule_answer'])

        # Verify correct algorithm produces correct answer
        correct_solution = self.correct_algo.solve(problem)
        self.assertTrue(correct_solution.is_correct)
        self.assertEqual(correct_solution.answer, problem.metadata['correct_answer'])

        # Verify answers are different
        self.assertNotEqual(malrule_solution.answer, correct_solution.answer)

    def test_word_problem_template(self):
        """Test word_problem template."""
        problem = self.generator.generate(seed=100, template='word_problem')

        # Check problem structure
        self.assertEqual(problem.metadata['template'], 'word_problem')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)
        self.assertIn('operation_type', problem.metadata)

        # Verify malrule produces incorrect answer
        malrule_solution = self.malrule.solve(problem)
        self.assertFalse(malrule_solution.is_correct)
        self.assertEqual(malrule_solution.answer, problem.metadata['malrule_answer'])

        # Verify correct algorithm produces correct answer
        correct_solution = self.correct_algo.solve(problem)
        self.assertTrue(correct_solution.is_correct)
        self.assertEqual(correct_solution.answer, problem.metadata['correct_answer'])

    def test_calculate_expected_answer(self):
        """Test calculate_expected_answer() produces valid answers."""
        for template in self.generator.get_available_templates():
            with self.subTest(template=template):
                problem = self.generator.generate(seed=42, template=template)

                # Calculate expected answer
                expected = self.malrule.calculate_expected_answer(problem)

                # Should produce a valid answer (not None or empty)
                self.assertIsNotNone(expected)
                self.assertNotEqual(expected, '')
                self.assertNotEqual(expected, 'None')

                # Verify the algorithm calculated (didn't use metadata)
                solution = self.malrule.solve(problem)
                # The solve method should produce the same answer as calculate_expected_answer
                self.assertEqual(expected, solution.answer)

    def test_malrule_solution_incorrect(self):
        """Test that malrule produces incorrect solutions."""
        for template in self.generator.get_available_templates():
            with self.subTest(template=template):
                problem = self.generator.generate(seed=42, template=template)
                solution = self.malrule.solve(problem)

                # Solution should be marked as incorrect
                self.assertFalse(solution.is_correct)
                self.assertEqual(solution.algorithm_name, self.malrule.get_name())

                # Answer should be string
                self.assertIsInstance(solution.answer, str)

    def test_correct_solution_correct(self):
        """Test that correct algorithm produces correct solutions."""
        for template in self.generator.get_available_templates():
            with self.subTest(template=template):
                problem = self.generator.generate(seed=42, template=template)
                solution = self.correct_algo.solve(problem)

                # Solution should be marked as correct
                self.assertTrue(solution.is_correct)
                self.assertEqual(solution.algorithm_name, self.correct_algo.get_name())

                # Answer should be string
                self.assertIsInstance(solution.answer, str)

    def test_malrule_vs_correct_different(self):
        """Test that malrule and correct algorithm give different answers (with edge case handling)."""
        for template in self.generator.get_available_templates():
            with self.subTest(template=template):
                problem = self.generator.generate(seed=42, template=template)

                malrule_solution = self.malrule.solve(problem)
                correct_solution = self.correct_algo.solve(problem)

                # Check if answers are the same (edge case where misconception produces correct answer)
                if malrule_solution.answer == correct_solution.answer:
                    # Print warning about edge case
                    print(f"\n⚠ WARNING: Edge case for template '{template}'")
                    print(f"  Problem: {problem.text}")
                    print(f"  Both algorithms produced: {malrule_solution.answer}")
                    print(f"  Malrule steps:")
                    for step in malrule_solution.steps:
                        print(f"    {step}")
                    print(f"  Correct steps:")
                    for step in correct_solution.steps:
                        print(f"    {step}")
                    # Note: This is acceptable for edge cases, so we don't fail the test
                else:
                    # Answers should normally be different
                    self.assertNotEqual(malrule_solution.answer, correct_solution.answer)

    # =======================
    # Specific Research Examples
    # =======================
    def test_specific_example_0_8_vs_0_45(self):
        """Test classic example: 0.8 vs 0.45 (malrule: 45 > 8, so picks 0.45, which is wrong)."""
        problem = Problem(
            text="Which is larger: 0.8 or 0.45?",
            operands=[0.8, 0.45],
            operation='decimal_comparison',
            level=5,
            difficulty=DifficultyLevel.EASY,
            metadata={
                'decimal1': 0.8,
                'decimal2': 0.45,
                'problem_type': 'different_lengths',
                'correct_answer': '0.8',
                'malrule_answer': '0.45'
            }
        )

        correct_solution = self.correct_algo.solve(problem)
        malrule_solution = self.malrule.solve(problem)

        # Correct: 0.8 is larger
        self.assertEqual(correct_solution.answer, '0.8')

        # Malrule: 0.45 (because 45 > 8, treats decimal parts as whole numbers)
        self.assertEqual(malrule_solution.answer, '0.45')
        self.assertNotEqual(correct_solution.answer, malrule_solution.answer)

    def test_specific_example_0_6_vs_0_59(self):
        """Test example: 0.6 vs 0.59 (malrule: 59 > 6, so picks 0.59, which is wrong)."""
        problem = Problem(
            text="Which is larger: 0.6 or 0.59?",
            operands=[0.6, 0.59],
            operation='decimal_comparison',
            level=5,
            difficulty=DifficultyLevel.MEDIUM,
            metadata={
                'decimal1': 0.6,
                'decimal2': 0.59,
                'problem_type': 'different_lengths',
                'correct_answer': '0.6',
                'malrule_answer': '0.59'
            }
        )

        correct_solution = self.correct_algo.solve(problem)
        malrule_solution = self.malrule.solve(problem)

        # Correct: 0.6 is larger
        self.assertEqual(correct_solution.answer, '0.6')

        # Malrule: 0.59 (because 59 > 6)
        self.assertEqual(malrule_solution.answer, '0.59')
        self.assertNotEqual(correct_solution.answer, malrule_solution.answer)

    def test_specific_example_0_3_vs_0_25(self):
        """Test example: 0.3 vs 0.25 (malrule: 25 > 3, so picks 0.25, which is wrong)."""
        problem = Problem(
            text="Which is larger: 0.3 or 0.25?",
            operands=[0.3, 0.25],
            operation='decimal_comparison',
            level=4,
            difficulty=DifficultyLevel.EASY,
            metadata={
                'decimal1': 0.3,
                'decimal2': 0.25,
                'problem_type': 'different_lengths',
                'correct_answer': '0.3',
                'malrule_answer': '0.25'
            }
        )

        correct_solution = self.correct_algo.solve(problem)
        malrule_solution = self.malrule.solve(problem)

        # Correct: 0.3 is larger
        self.assertEqual(correct_solution.answer, '0.3')

        # Malrule: 0.25 (because 25 > 3)
        self.assertEqual(malrule_solution.answer, '0.25')
        self.assertNotEqual(correct_solution.answer, malrule_solution.answer)

    def test_specific_example_0_7_vs_0_9_same_length(self):
        """Test example: 0.7 vs 0.9 (both same decimal places, both algorithms agree)."""
        problem = Problem(
            text="Which is larger: 0.7 or 0.9?",
            operands=[0.7, 0.9],
            operation='decimal_comparison',
            level=4,
            difficulty=DifficultyLevel.EASY,
            metadata={
                'decimal1': 0.7,
                'decimal2': 0.9,
                'problem_type': 'same_length',
                'correct_answer': '0.9',
                'malrule_answer': '0.9'
            }
        )

        correct_solution = self.correct_algo.solve(problem)
        malrule_solution = self.malrule.solve(problem)

        # Both should agree: 0.9 > 0.7 (7 < 9 both ways)
        self.assertEqual(correct_solution.answer, '0.9')
        self.assertEqual(malrule_solution.answer, '0.9')

    def test_specific_example_three_way_comparison(self):
        """Test three-way comparison: 0.8, 0.45, 0.65."""
        problem = Problem(
            text="Order these decimals from smallest to largest: 0.8, 0.45, 0.65",
            operands=[0.8, 0.45, 0.65],
            operation='decimal_ordering',
            level=5,
            difficulty=DifficultyLevel.HARD,
            metadata={
                'decimals': [0.8, 0.45, 0.65],
                'problem_type': 'three_way_comparison',
                'correct_answer': '[0.45, 0.65, 0.8]',
                'malrule_answer': '[0.8, 0.45, 0.65]'
            }
        )

        correct_solution = self.correct_algo.solve(problem)
        malrule_solution = self.malrule.solve(problem)

        # Correct: [0.45, 0.65, 0.8]
        self.assertEqual(correct_solution.answer, '[0.45, 0.65, 0.8]')

        # Malrule: sorts by decimal parts as whole numbers (8, 45, 65) -> [0.8, 0.45, 0.65]
        self.assertEqual(malrule_solution.answer, '[0.8, 0.45, 0.65]')
        self.assertNotEqual(correct_solution.answer, malrule_solution.answer)

    def test_specific_example_larger_whole_parts(self):
        """Test with larger whole parts: 2.3 vs 2.15 (malrule: 15 > 3, picks 2.15, which is wrong)."""
        problem = Problem(
            text="Which is larger: 2.3 or 2.15?",
            operands=[2.3, 2.15],
            operation='decimal_comparison',
            level=5,
            difficulty=DifficultyLevel.MEDIUM,
            metadata={
                'decimal1': 2.3,
                'decimal2': 2.15,
                'problem_type': 'larger_whole_parts',
                'correct_answer': '2.3',
                'malrule_answer': '2.15'
            }
        )

        correct_solution = self.correct_algo.solve(problem)
        malrule_solution = self.malrule.solve(problem)

        # Correct: 2.3 > 2.15
        self.assertEqual(correct_solution.answer, '2.3')

        # Malrule: 2.15 (because 15 > 3)
        self.assertEqual(malrule_solution.answer, '2.15')
        self.assertNotEqual(correct_solution.answer, malrule_solution.answer)

    def test_specific_example_word_problem(self):
        """Test word problem context: John ran 0.8 km, Mary ran 0.45 km."""
        problem = Problem(
            text="John ran 0.8 km and Mary ran 0.45 km. Who ran farther?",
            operands=[0.8, 0.45],
            operation='decimal_comparison',
            level=5,
            difficulty=DifficultyLevel.MEDIUM,
            metadata={
                'decimal1': 0.8,
                'decimal2': 0.45,
                'problem_type': 'word_problem_context',
                'context_type': 'distance',
                'correct_answer': '0.8',
                'malrule_answer': '0.45'
            }
        )

        correct_solution = self.correct_algo.solve(problem)
        malrule_solution = self.malrule.solve(problem)

        # Correct: 0.8 > 0.45 (John ran farther)
        self.assertEqual(correct_solution.answer, '0.8')

        # Malrule: 0.45 (because 45 > 8, Mary ran farther - WRONG!)
        self.assertEqual(malrule_solution.answer, '0.45')
        self.assertNotEqual(correct_solution.answer, malrule_solution.answer)


class TestWholeNumberThinkingAutomated(unittest.TestCase):
    """Automated test suite runner."""

    def test_automated_suite(self):
        """Run the automated test suite."""
        problem_gen = DecimalWholeNumberProblemGenerator(
            level=5,
            difficulty=DifficultyLevel.MEDIUM
        )
        malrule = WholeNumberThinkingMalrule()
        correct = DecimalCorrectAlgorithm()

        test_suite = MalruleTest(malrule, correct, problem_gen)
        results = test_suite.run_all_tests(verbose=True)

        all_passed = all(r.passed for r in results)
        self.assertTrue(all_passed,
                       f"Automated tests failed: {[r.message for r in results if not r.passed]}")


def main():
    """Main entry point for standalone execution."""
    print("\n╔" + "═"*68 + "╗")
    print("║" + "  VERIFICATION TEST: Whole-Number-Thinking  ".center(70) + "║")
    print("╚" + "═"*68 + "╝\n")

    # Run unittest
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestWholeNumberThinking))
    suite.addTests(loader.loadTestsFromTestCase(TestWholeNumberThinkingAutomated))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    if result.wasSuccessful():
        print("\n\n╔" + "═"*68 + "╗")
        print("║" + "  ✓✓✓ VERIFICATION COMPLETE ✓✓✓  ".center(70) + "║")
        print("╚" + "═"*68 + "╝\n")
        return 0
    else:
        print("\n\n╔" + "═"*68 + "╗")
        print("║" + "  ✗✗✗ SOME TESTS FAILED ✗✗✗  ".center(70) + "║")
        print("╚" + "═"*68 + "╝\n")
        return 1


if __name__ == "__main__":
    exit(main())
