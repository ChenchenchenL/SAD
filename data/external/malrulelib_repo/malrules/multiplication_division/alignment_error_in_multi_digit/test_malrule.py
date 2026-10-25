#!/usr/bin/env python3
"""
Comprehensive test suite for Alignment Error In Multi Digit malrule.

This file combines:
1. Template validation tests (all templates)
2. Automated test suite functionality

Run from project root: python3 -m malrules.multiplication_division.alignment_error_in_multi_digit.test_malrule
Or from this directory: python3 test_malrule.py
"""

import sys
import os
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.multiplication_division.alignment_error_in_multi_digit import (
    AlignmentErrorProblemGenerator,
    AlignmentErrorMalrule,
    MultiDigitMultiplicationCorrectAlgorithm
)


class TestAlignmentErrorInMultiDigit(unittest.TestCase):
    """Test cases for Alignment-Error-In-Multi-Digit malrule."""

    def setUp(self):
        """Set up test fixtures."""
        self.generator = AlignmentErrorProblemGenerator(
            level=4,
            difficulty=DifficultyLevel.MEDIUM
        )
        self.malrule = AlignmentErrorMalrule()
        self.correct_algo = MultiDigitMultiplicationCorrectAlgorithm()

    def test_get_available_templates(self):
        """Test that all 10 templates are available."""
        templates = self.generator.get_available_templates()
        self.assertEqual(len(templates), 10)
        expected = ['basic_2x2', 'word_problem', 'three_digit',
                    'money_context', 'array_model', 'three_digit_times_three',
                    'perimeter_then_area', 'multi_item_purchase',
                    'tiling_problem', 'calendar_calculation']
        for template in expected:
            self.assertIn(template, templates)

    def test_basic_2x2_template(self):
        """Test basic_2x2 template."""
        problem = self.generator.generate(seed=42, template='basic_2x2')

        # Check problem structure
        self.assertEqual(problem.operation, 'multiplication')
        self.assertIn('template', problem.metadata)
        self.assertEqual(problem.metadata['template'], 'basic_2x2')

        # Check metadata has required fields
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)
        self.assertIn('num1', problem.metadata)
        self.assertIn('num2', problem.metadata)

        # Verify answers are strings
        self.assertIsInstance(problem.metadata['correct_answer'], str)
        self.assertIsInstance(problem.metadata['malrule_answer'], str)

    def test_word_problem_template(self):
        """Test word_problem template."""
        problem = self.generator.generate(seed=42, template='word_problem')

        self.assertEqual(problem.metadata['template'], 'word_problem')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)

        # Should have real-world context
        self.assertTrue(
            any(word in problem.text.lower() for word in ['classroom', 'box', 'garden', 'theater', 'row'])
        )

    def test_three_digit_template(self):
        """Test three_digit template."""
        problem = self.generator.generate(seed=42, template='three_digit')

        self.assertEqual(problem.metadata['template'], 'three_digit')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)
        self.assertIn('is_3digit', problem.metadata)
        self.assertTrue(problem.metadata['is_3digit'])

        # Should have 3-digit multiplication
        num2 = problem.metadata['num2']
        self.assertGreaterEqual(num2, 100)

    def test_money_context_template(self):
        """Test money_context template."""
        problem = self.generator.generate(seed=42, template='money_context')

        self.assertEqual(problem.metadata['template'], 'money_context')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)

        # Check that answers have dollar signs
        self.assertTrue(problem.metadata['correct_answer'].startswith('$'))
        self.assertTrue(problem.metadata['malrule_answer'].startswith('$'))

    def test_array_model_template(self):
        """Test array_model template."""
        problem = self.generator.generate(seed=42, template='array_model')

        self.assertEqual(problem.metadata['template'], 'array_model')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)

        # Should have array/area context
        self.assertTrue(
            any(word in problem.text.lower() for word in ['room', 'parking', 'array', 'row'])
        )

    def test_calculate_expected_answer(self):
        """Test calculate_expected_answer() for all templates."""
        for template in self.generator.get_available_templates():
            with self.subTest(template=template):
                problem = self.generator.generate(seed=42, template=template)

                # Calculate expected answer
                expected = self.malrule.calculate_expected_answer(problem)

                # Should match metadata malrule_answer
                metadata_answer = problem.metadata['malrule_answer']

                # Handle units ($ or context types with units at end)
                metadata_numeric = str(metadata_answer)
                if metadata_numeric.startswith('$'):
                    metadata_numeric = metadata_numeric[1:]
                # Strip units from end (e.g., " hours", " pages", " minutes")
                parts = metadata_numeric.split()
                if len(parts) > 1:
                    metadata_numeric = parts[0]

                self.assertEqual(expected, metadata_numeric)

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
        """Test that malrule and correct algorithm give different answers."""
        for template in self.generator.get_available_templates():
            with self.subTest(template=template):
                problem = self.generator.generate(seed=42, template=template)

                malrule_solution = self.malrule.solve(problem)
                correct_solution = self.correct_algo.solve(problem)

                # For money_context, extract numeric parts
                malrule_answer = malrule_solution.answer
                correct_answer = correct_solution.answer

                # Remove units for comparison
                if malrule_answer.startswith('$'):
                    malrule_answer = malrule_answer[1:]
                if correct_answer.startswith('$'):
                    correct_answer = correct_answer[1:]

                # Answers should be different
                self.assertNotEqual(malrule_answer, correct_answer,
                                  f"Malrule and correct should differ for {template}")

    def test_specific_example_23_times_14(self):
        """Test the classic example: 23 × 14 = 115 (malrule) vs 322 (correct)."""
        from utils import Problem

        # 23 × 14:
        # Correct: 23×4=92, 23×10=230, total=322
        # Malrule: 23×4=92, 23×1=23, total=115 (forgot to shift!)
        problem = Problem(
            text="Multiply 23 × 14",
            operands=[23, 14],
            operation='multiplication',
            level=4,
            difficulty=DifficultyLevel.MEDIUM,
            metadata={
                'num1': 23,
                'num2': 14,
                'num1_tens': 2,
                'num1_ones': 3,
                'num2_tens': 1,
                'num2_ones': 4,
                'correct_answer': '322',
                'malrule_answer': '115',
                'template': 'basic_2x2'
            }
        )

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        # Correct: 322
        self.assertEqual(correct_solution.answer, '322')

        # Malrule: 115 (misaligned partial products)
        self.assertEqual(malrule_solution.answer, '115')

    def test_backwards_compatibility(self):
        """Test that old problems without metadata still work."""
        from utils import Problem

        # Create old-style problem without template metadata
        old_problem = Problem(
            text="Multiply 23 × 14",
            operands=[23, 14],
            operation='multiplication',
            level=4,
            difficulty=DifficultyLevel.MEDIUM,
            metadata={}
        )

        # Should still work
        malrule_solution = self.malrule.solve(old_problem)
        correct_solution = self.correct_algo.solve(old_problem)

        self.assertIsInstance(malrule_solution.answer, str)
        self.assertIsInstance(correct_solution.answer, str)

    def test_alignment_error_behavior(self):
        """Test that malrule always misaligns (doesn't shift) partial products."""
        problem = self.generator.generate(seed=100, template='basic_2x2')

        num1 = problem.metadata['num1']
        num2 = problem.metadata['num2']
        num2_ones = num2 % 10
        num2_tens = num2 // 10

        # Get solutions
        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        # Malrule should compute: (num1 * num2_ones) + (num1 * num2_tens)
        expected_malrule = num1 * num2_ones + num1 * num2_tens
        self.assertEqual(malrule_solution.answer, str(expected_malrule))

        # Correct should compute: num1 * num2
        expected_correct = num1 * num2
        self.assertEqual(correct_solution.answer, str(expected_correct))

        # They should be different
        self.assertNotEqual(expected_malrule, expected_correct)



class TestAlignmentErrorAutomated(unittest.TestCase):
    """Automated test suite runner."""

    def test_automated_suite(self):
        """Run the automated test suite."""
        problem_gen = AlignmentErrorProblemGenerator(
            level=5,
            difficulty=DifficultyLevel.MEDIUM
        )
        malrule = AlignmentErrorMalrule()
        correct = MultiDigitMultiplicationCorrectAlgorithm()

        test_suite = MalruleTest(malrule, correct, problem_gen)
        results = test_suite.run_all_tests(verbose=False)

        all_passed = all(r.passed for r in results)
        self.assertTrue(all_passed,
                       f"Automated tests failed: {[r.message for r in results if not r.passed]}")


def main():
    """Main entry point for standalone execution."""
    print("\n╔" + "═"*68 + "╗")
    print("║" + "  VERIFICATION TEST: Alignment Error In Multi Digit  ".center(70) + "║")
    print("╚" + "═"*68 + "╝\n")

    # Run unittest
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestAlignmentErrorInMultiDigit))
    suite.addTests(loader.loadTestsFromTestCase(TestAlignmentErrorAutomated))

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
