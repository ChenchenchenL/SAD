#!/usr/bin/env python3
"""
Comprehensive test suite for Shorter-Is-Larger malrule.

This file combines:
1. Template validation tests (all 5 templates)
2. Specific research-based examples
3. Automated test suite functionality

Run from project root: python3 -m malrules.decimals.shorter_is_larger.test_malrule
Or from this directory: python3 test_malrule.py
"""

import sys
import os
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.decimals.shorter_is_larger import (
    ShorterIsLargerProblemGenerator,
    ShorterIsLargerMalrule,
    DecimalComparisonCorrectAlgorithm
)


class TestShorterIsLarger(unittest.TestCase):
    """Comprehensive test cases for Shorter-Is-Larger malrule."""

    def setUp(self):
        """Set up test fixtures."""
        self.generator = ShorterIsLargerProblemGenerator(
            level=5,
            difficulty=DifficultyLevel.MEDIUM
        )
        self.malrule = ShorterIsLargerMalrule()
        self.correct_algo = DecimalComparisonCorrectAlgorithm()

    # =======================
    # Template Tests
    # =======================
    def test_get_available_templates(self):
        """Test that all 6 templates are available."""
        templates = self.generator.get_available_templates()
        self.assertEqual(len(templates), 6)
        expected = ['basic_comparison', 'ordering', 'money_context',
                    'measurement_context', 'number_line', 'word_problem_context']
        for template in expected:
            self.assertIn(template, templates)

    def test_basic_comparison_template(self):
        """Test basic_comparison template."""
        problem = self.generator.generate(seed=100, template='basic_comparison')

        # Check problem structure
        self.assertEqual(problem.operation, 'comparison')
        self.assertIn('template', problem.metadata)
        self.assertEqual(problem.metadata['template'], 'basic_comparison')

        # Check metadata has required fields
        self.assertIn('shorter_decimal', problem.metadata)
        self.assertIn('longer_decimal', problem.metadata)
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)
        self.assertIn('shorter_places', problem.metadata)
        self.assertIn('longer_places', problem.metadata)

        # Verify answers are strings
        self.assertIsInstance(problem.metadata['correct_answer'], str)
        self.assertIsInstance(problem.metadata['malrule_answer'], str)

        # Verify the malrule answer is the shorter decimal
        shorter = problem.metadata['shorter_decimal']
        malrule_answer = problem.metadata['malrule_answer']
        self.assertEqual(str(shorter), malrule_answer)

        # Verify the correct answer is the longer decimal
        longer = problem.metadata['longer_decimal']
        correct_answer = problem.metadata['correct_answer']
        self.assertEqual(str(longer), correct_answer)

    def test_ordering_template(self):
        """Test ordering template."""
        problem = self.generator.generate(seed=200, template='ordering')

        self.assertEqual(problem.metadata['template'], 'ordering')
        self.assertEqual(problem.operation, 'comparison')
        self.assertIn('decimals', problem.metadata)
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)
        self.assertIn('num_count', problem.metadata)
        self.assertEqual(problem.metadata['num_count'], 3)

        # Verify we have 3 decimals
        decimals = problem.metadata['decimals']
        self.assertEqual(len(decimals), 3)

        # Verify malrule answer is the shortest (first decimal with 1 place)
        malrule_answer = problem.metadata['malrule_answer']
        self.assertEqual(str(decimals[0]), malrule_answer)

        # Verify correct answer is the longest (last decimal, largest value)
        correct_answer = problem.metadata['correct_answer']
        self.assertEqual(str(max(decimals)), correct_answer)

    def test_money_context_template(self):
        """Test money_context template."""
        problem = self.generator.generate(seed=300, template='money_context')

        self.assertEqual(problem.metadata['template'], 'money_context')
        self.assertIn('shorter_amount', problem.metadata)
        self.assertIn('longer_amount', problem.metadata)
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)
        self.assertIn('context', problem.metadata)
        self.assertEqual(problem.metadata['context'], 'money')

        # Verify answers have $ prefix
        self.assertTrue(problem.metadata['correct_answer'].startswith('$'))
        self.assertTrue(problem.metadata['malrule_answer'].startswith('$'))

        # Verify malrule answer is the shorter amount (with $)
        shorter = problem.metadata['shorter_amount']
        malrule_answer = problem.metadata['malrule_answer']
        self.assertEqual(f'${shorter}', malrule_answer)

        # Verify correct answer is the longer amount (with $)
        longer = problem.metadata['longer_amount']
        correct_answer = problem.metadata['correct_answer']
        self.assertEqual(f'${longer}', correct_answer)

    def test_measurement_context_template(self):
        """Test measurement_context template."""
        problem = self.generator.generate(seed=400, template='measurement_context')

        self.assertEqual(problem.metadata['template'], 'measurement_context')
        self.assertIn('shorter_measure', problem.metadata)
        self.assertIn('longer_measure', problem.metadata)
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)
        self.assertIn('context', problem.metadata)
        self.assertIn('unit', problem.metadata)
        self.assertEqual(problem.metadata['context'], 'measurement')

        # Verify malrule answer is the shorter measure
        shorter = problem.metadata['shorter_measure']
        malrule_answer = problem.metadata['malrule_answer']
        self.assertEqual(str(shorter), malrule_answer)

        # Verify correct answer is the longer measure
        longer = problem.metadata['longer_measure']
        correct_answer = problem.metadata['correct_answer']
        self.assertEqual(str(longer), correct_answer)

    def test_number_line_template(self):
        """Test number_line template."""
        problem = self.generator.generate(seed=500, template='number_line')

        self.assertEqual(problem.metadata['template'], 'number_line')
        self.assertIn('shorter_decimal', problem.metadata)
        self.assertIn('longer_decimal', problem.metadata)
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)

        # Verify malrule answer is the shorter decimal
        shorter = problem.metadata['shorter_decimal']
        malrule_answer = problem.metadata['malrule_answer']
        self.assertEqual(str(shorter), malrule_answer)

        # Verify correct answer is the longer decimal
        longer = problem.metadata['longer_decimal']
        correct_answer = problem.metadata['correct_answer']
        self.assertEqual(str(longer), correct_answer)

    def test_calculate_expected_answer(self):
        """Test calculate_expected_answer() for all templates."""
        for template in self.generator.get_available_templates():
            with self.subTest(template=template):
                problem = self.generator.generate(seed=42, template=template)

                # Calculate expected answer
                expected = self.malrule.calculate_expected_answer(problem)

                # Should match metadata malrule_answer (numeric part)
                metadata_answer = problem.metadata['malrule_answer']

                # Handle $ sign
                if metadata_answer.startswith('$'):
                    self.assertTrue(expected.startswith('$'))
                    self.assertEqual(expected, metadata_answer)
                else:
                    self.assertEqual(expected, metadata_answer)

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

                # Extract numeric parts for comparison
                malrule_answer = malrule_solution.answer
                correct_answer = correct_solution.answer

                # Remove $ for comparison
                if malrule_answer.startswith('$'):
                    malrule_answer = malrule_answer[1:]
                if correct_answer.startswith('$'):
                    correct_answer = correct_answer[1:]

                # Answers should be different
                self.assertNotEqual(malrule_answer, correct_answer,
                                  f"Malrule and correct should differ for {template}")

    # =======================
    # Specific Research Examples
    # =======================
    def test_specific_example_0_5_vs_0_36(self):
        """Test classic example: 0.5 vs 0.36 (malrule picks 0.5, which is accidentally correct)."""
        problem = Problem(
            text="Which is larger: 0.5 or 0.36?",
            operands=[0.5, 0.36],
            operation='comparison',
            level=5,
            difficulty=DifficultyLevel.MEDIUM,
            metadata={
                'num1': 0.5,
                'num2': 0.36,
                'correct_answer': '0.5',
                'malrule_answer': '0.5',
                'num1_decimal_places': 1,
                'num2_decimal_places': 2
            }
        )

        correct_solution = self.correct_algo.solve(problem)
        malrule_solution = self.malrule.solve(problem)

        # Correct: 0.5
        self.assertEqual(correct_solution.answer, '0.5')

        # Malrule: 0.5 (picks shorter, which is accidentally correct)
        self.assertEqual(malrule_solution.answer, '0.5')

    def test_specific_example_0_3_vs_0_42(self):
        """Test example: 0.3 vs 0.42 (malrule picks 0.3, which is wrong)."""
        problem = Problem(
            text="Which is larger: 0.3 or 0.42?",
            operands=[0.3, 0.42],
            operation='comparison',
            level=5,
            difficulty=DifficultyLevel.MEDIUM,
            metadata={
                'num1': 0.3,
                'num2': 0.42,
                'correct_answer': '0.42',
                'malrule_answer': '0.3',
                'num1_decimal_places': 1,
                'num2_decimal_places': 2
            }
        )

        correct_solution = self.correct_algo.solve(problem)
        malrule_solution = self.malrule.solve(problem)

        # Correct: 0.42
        self.assertEqual(correct_solution.answer, '0.42')

        # Malrule: 0.3 (picks shorter, which is wrong)
        self.assertEqual(malrule_solution.answer, '0.3')
        self.assertNotEqual(correct_solution.answer, malrule_solution.answer)

    def test_specific_example_0_8_vs_0_75(self):
        """Test example: 0.8 vs 0.75 (malrule picks 0.8, which is accidentally correct)."""
        problem = Problem(
            text="Which is larger: 0.8 or 0.75?",
            operands=[0.8, 0.75],
            operation='comparison',
            level=5,
            difficulty=DifficultyLevel.MEDIUM,
            metadata={
                'num1': 0.8,
                'num2': 0.75,
                'correct_answer': '0.8',
                'malrule_answer': '0.8',
                'num1_decimal_places': 1,
                'num2_decimal_places': 2
            }
        )

        correct_solution = self.correct_algo.solve(problem)
        malrule_solution = self.malrule.solve(problem)

        self.assertEqual(correct_solution.answer, '0.8')
        self.assertEqual(malrule_solution.answer, '0.8')

    def test_specific_example_0_2_vs_0_19(self):
        """Test example: 0.2 vs 0.19 (malrule picks 0.2, which is accidentally correct)."""
        problem = Problem(
            text="Which is larger: 0.2 or 0.19?",
            operands=[0.2, 0.19],
            operation='comparison',
            level=5,
            difficulty=DifficultyLevel.MEDIUM,
            metadata={
                'num1': 0.2,
                'num2': 0.19,
                'correct_answer': '0.2',
                'malrule_answer': '0.2',
                'num1_decimal_places': 1,
                'num2_decimal_places': 2
            }
        )

        correct_solution = self.correct_algo.solve(problem)
        malrule_solution = self.malrule.solve(problem)

        self.assertEqual(correct_solution.answer, '0.2')
        self.assertEqual(malrule_solution.answer, '0.2')

    def test_specific_example_three_decimals(self):
        """Test three-decimal comparison: 1.2, 1.35, 1.678 (malrule picks 1.2, which is wrong)."""
        problem = Problem(
            text="Which is the largest: 1.2, 1.35, or 1.678?",
            operands=[1.2, 1.35, 1.678],
            operation='comparison',
            level=5,
            difficulty=DifficultyLevel.MEDIUM,
            metadata={
                'num1': 1.2,
                'num2': 1.35,
                'num3': 1.678,
                'correct_answer': '1.678',
                'malrule_answer': '1.2',
                'num1_decimal_places': 1,
                'num2_decimal_places': 2,
                'num3_decimal_places': 3,
                'template': 'ordering',
                'num_count': 3,
                'decimals': [1.2, 1.35, 1.678]
            }
        )

        correct_solution = self.correct_algo.solve(problem)
        malrule_solution = self.malrule.solve(problem)

        self.assertEqual(correct_solution.answer, '1.678')  # Largest value
        self.assertEqual(malrule_solution.answer, '1.2')    # Shortest decimal (1 place)
        self.assertNotEqual(correct_solution.answer, malrule_solution.answer)

    def test_specific_example_various_lengths(self):
        """Test various lengths: 3.5 vs 3.8765 (malrule picks 3.5, which is wrong)."""
        problem = Problem(
            text="Which is larger: 3.5 or 3.8765?",
            operands=[3.5, 3.8765],
            operation='comparison',
            level=5,
            difficulty=DifficultyLevel.MEDIUM,
            metadata={
                'num1': 3.5,
                'num2': 3.8765,
                'correct_answer': '3.8765',
                'malrule_answer': '3.5',
                'num1_decimal_places': 1,
                'num2_decimal_places': 4
            }
        )

        correct_solution = self.correct_algo.solve(problem)
        malrule_solution = self.malrule.solve(problem)

        self.assertEqual(correct_solution.answer, '3.8765')
        self.assertEqual(malrule_solution.answer, '3.5')  # Shorter (1 place)
        self.assertNotEqual(correct_solution.answer, malrule_solution.answer)

    def test_specific_example_money_context(self):
        """Test money context: $5.2 vs $5.75 (malrule picks $5.2, which is wrong)."""
        problem = Problem(
            text="Which is more money: $5.2 or $5.75?",
            operands=[5.2, 5.75],
            operation='comparison',
            level=5,
            difficulty=DifficultyLevel.MEDIUM,
            metadata={
                'num1': 5.2,
                'num2': 5.75,
                'correct_answer': '5.75',
                'malrule_answer': '5.2',
                'num1_decimal_places': 1,
                'num2_decimal_places': 2,
                'template': 'money_context',
                'context': 'money'
            }
        )

        correct_solution = self.correct_algo.solve(problem)
        malrule_solution = self.malrule.solve(problem)

        self.assertEqual(correct_solution.answer, '5.75')
        # Malrule answer might have $ prefix for money context
        malrule_ans = malrule_solution.answer.lstrip('$')
        self.assertEqual(malrule_ans, '5.2')  # Shorter
        self.assertNotEqual(correct_solution.answer, malrule_solution.answer)

    def test_specific_example_measurement_context(self):
        """Test measurement context: 7.5 meters vs 7.125 meters (malrule picks 7.5, accidentally correct)."""
        problem = Problem(
            text="Which measurement is greater: 7.5 meters or 7.125 meters?",
            operands=[7.5, 7.125],
            operation='comparison',
            level=5,
            difficulty=DifficultyLevel.MEDIUM,
            metadata={
                'num1': 7.5,
                'num2': 7.125,
                'correct_answer': '7.5',
                'malrule_answer': '7.5',
                'num1_decimal_places': 1,
                'num2_decimal_places': 3,
                'template': 'measurement_context',
                'context': 'measurement',
                'unit': 'meters'
            }
        )

        correct_solution = self.correct_algo.solve(problem)
        malrule_solution = self.malrule.solve(problem)

        self.assertEqual(correct_solution.answer, '7.5')
        self.assertEqual(malrule_solution.answer, '7.5')  # Shorter - happens to be correct!


class TestShorterIsLargerAutomated(unittest.TestCase):
    """Automated test suite runner."""

    def test_automated_suite(self):
        """Run the automated test suite."""
        problem_gen = ShorterIsLargerProblemGenerator(
            level=5,
            difficulty=DifficultyLevel.MEDIUM
        )
        malrule = ShorterIsLargerMalrule()
        correct = DecimalComparisonCorrectAlgorithm()

        test_suite = MalruleTest(malrule, correct, problem_gen)
        results = test_suite.run_all_tests(verbose=False)

        all_passed = all(r.passed for r in results)
        self.assertTrue(all_passed,
                       f"Automated tests failed: {[r.message for r in results if not r.passed]}")


def main():
    """Main entry point for standalone execution."""
    print("\n╔" + "═"*68 + "╗")
    print("║" + "  VERIFICATION TEST: Shorter-Is-Larger  ".center(70) + "║")
    print("╚" + "═"*68 + "╝\n")

    # Run unittest
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestShorterIsLarger))
    suite.addTests(loader.loadTestsFromTestCase(TestShorterIsLargerAutomated))

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
