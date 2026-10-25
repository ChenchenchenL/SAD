#!/usr/bin/env python3
"""
Comprehensive test suite for Right Align Decimals malrule.

This file combines:
1. Template validation tests (all templates)
2. Automated test suite functionality

Run from project root: python3 -m malrules.decimals.right_align_decimals.test_malrule
Or from this directory: python3 test_malrule.py
"""

import sys
import os
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.decimals.right_align_decimals import (
    RightAlignDecimalsProblemGenerator,
    RightAlignDecimalsMalrule,
    DecimalAdditionCorrectAlgorithm
)


class TestRightAlignDecimalsTemplates(unittest.TestCase):
    """Test all 5 templates for Right-Align-Decimals malrule."""

    def setUp(self):
        """Set up test fixtures."""
        self.generator = RightAlignDecimalsProblemGenerator(
            level=5,
            difficulty=DifficultyLevel.MEDIUM
        )
        self.malrule = RightAlignDecimalsMalrule()
        self.correct_algo = DecimalAdditionCorrectAlgorithm()

    # Template 1: basic_addition
    def test_basic_addition_template(self):
        """Test basic_addition template generates valid problems."""
        problem = self.generator.generate(seed=100, template='basic_addition')

        self.assertEqual(problem.metadata['template'], 'basic_addition')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)
        self.assertIn('num1', problem.metadata)
        self.assertIn('num2', problem.metadata)

        # Should have 1 and 2 decimal places
        self.assertEqual(problem.metadata['num1_decimal_places'], 1)
        self.assertEqual(problem.metadata['num2_decimal_places'], 2)

    def test_basic_addition_malrule_vs_correct(self):
        """Test basic_addition: malrule gives wrong answer, correct gives right answer."""
        problem = self.generator.generate(seed=101, template='basic_addition')

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        self.assertFalse(malrule_solution.is_correct)
        self.assertTrue(correct_solution.is_correct)

        # Answers should match metadata
        self.assertEqual(malrule_solution.answer, problem.metadata['malrule_answer'])
        self.assertEqual(correct_solution.answer, problem.metadata['correct_answer'])

    def test_basic_addition_calculate_expected_answer(self):
        """Test calculate_expected_answer for basic_addition template."""
        problem = self.generator.generate(seed=102, template='basic_addition')

        expected_answer = self.malrule.calculate_expected_answer(problem)
        malrule_solution = self.malrule.solve(problem)

        self.assertEqual(expected_answer, malrule_solution.answer)
        self.assertEqual(expected_answer, problem.metadata['malrule_answer'])

    # Template 2: basic_subtraction
    def test_basic_subtraction_template(self):
        """Test basic_subtraction template generates valid problems."""
        problem = self.generator.generate(seed=200, template='basic_subtraction')

        self.assertEqual(problem.metadata['template'], 'basic_subtraction')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)

        # Should have 2 and 1 decimal places
        self.assertEqual(problem.metadata['num1_decimal_places'], 2)
        self.assertEqual(problem.metadata['num2_decimal_places'], 1)

        # Should be subtraction
        self.assertEqual(problem.operation, 'subtraction')
        self.assertEqual(problem.metadata['operation_symbol'], '-')

    def test_basic_subtraction_malrule_vs_correct(self):
        """Test basic_subtraction: malrule incorrectly aligns decimals."""
        problem = self.generator.generate(seed=201, template='basic_subtraction')

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        self.assertFalse(malrule_solution.is_correct)
        self.assertTrue(correct_solution.is_correct)

        # Malrule answer should differ from correct answer
        self.assertNotEqual(malrule_solution.answer, correct_solution.answer)

    def test_basic_subtraction_calculate_expected_answer(self):
        """Test calculate_expected_answer for basic_subtraction template."""
        problem = self.generator.generate(seed=202, template='basic_subtraction')

        expected_answer = self.malrule.calculate_expected_answer(problem)
        malrule_solution = self.malrule.solve(problem)

        self.assertEqual(expected_answer, malrule_solution.answer)

    # Template 3: money_word_problem
    def test_money_word_problem_template(self):
        """Test money_word_problem template generates valid problems."""
        problem = self.generator.generate(seed=300, template='money_word_problem')

        self.assertEqual(problem.metadata['template'], 'money_word_problem')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)

        # Should have money context
        self.assertEqual(problem.metadata['context'], 'money')

        # Answers should have $ symbol
        self.assertTrue(problem.metadata['correct_answer'].startswith('$'))
        self.assertTrue(problem.metadata['malrule_answer'].startswith('$'))

        # Should mention money-related terms
        self.assertTrue(
            any(word in problem.text.lower() for word in ['$', 'money', 'cost', 'earned', 'receives'])
        )

    def test_money_word_problem_malrule_vs_correct(self):
        """Test money_word_problem: malrule misapplies rule in money context."""
        problem = self.generator.generate(seed=301, template='money_word_problem')

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        self.assertFalse(malrule_solution.is_correct)
        self.assertTrue(correct_solution.is_correct)

        # Numeric parts should differ
        malrule_numeric = malrule_solution.answer
        correct_numeric = correct_solution.answer
        self.assertNotEqual(malrule_numeric, correct_numeric)

    def test_money_word_problem_calculate_expected_answer(self):
        """Test calculate_expected_answer for money_word_problem template."""
        problem = self.generator.generate(seed=302, template='money_word_problem')

        expected_answer = self.malrule.calculate_expected_answer(problem)
        malrule_solution = self.malrule.solve(problem)

        # Both should match (numeric part)
        self.assertEqual(expected_answer, malrule_solution.answer)

    # Template 4: measurement_word_problem
    def test_measurement_word_problem_template(self):
        """Test measurement_word_problem template generates valid problems."""
        problem = self.generator.generate(seed=400, template='measurement_word_problem')

        self.assertEqual(problem.metadata['template'], 'measurement_word_problem')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)

        # Should have measurement context
        self.assertEqual(problem.metadata['context'], 'measurement')
        self.assertIn('unit', problem.metadata)

        # Answers should have units
        unit = problem.metadata['unit']
        self.assertTrue(problem.metadata['correct_answer'].endswith(unit))
        self.assertTrue(problem.metadata['malrule_answer'].endswith(unit))

        # Should mention measurement-related terms
        self.assertTrue(
            any(word in problem.text.lower() for word in ['rope', 'container', 'piece', 'measures', 'm', 'kg', 'cm', 'l'])
        )

    def test_measurement_word_problem_malrule_vs_correct(self):
        """Test measurement_word_problem: malrule misapplies rule in measurement context."""
        problem = self.generator.generate(seed=401, template='measurement_word_problem')

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        self.assertFalse(malrule_solution.is_correct)
        self.assertTrue(correct_solution.is_correct)

        # Numeric parts should differ
        self.assertNotEqual(malrule_solution.answer, correct_solution.answer)

    def test_measurement_word_problem_calculate_expected_answer(self):
        """Test calculate_expected_answer for measurement_word_problem template."""
        problem = self.generator.generate(seed=402, template='measurement_word_problem')

        expected_answer = self.malrule.calculate_expected_answer(problem)
        malrule_solution = self.malrule.solve(problem)

        # Both should match (numeric part)
        self.assertEqual(expected_answer, malrule_solution.answer)

    # Template 5: three_number_mixed
    def test_three_number_mixed_template(self):
        """Test three_number_mixed template generates valid problems."""
        problem = self.generator.generate(seed=500, template='three_number_mixed')

        self.assertEqual(problem.metadata['template'], 'three_number_mixed')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)

        # Should have 3 operands
        self.assertEqual(len(problem.operands), 3)
        self.assertEqual(problem.metadata['num_count'], 3)

        # Should be mixed operation
        self.assertEqual(problem.operation, 'mixed')
        self.assertIn('num3', problem.metadata)

    def test_three_number_mixed_malrule_vs_correct(self):
        """Test three_number_mixed: malrule misapplies rule in multi-step operations."""
        problem = self.generator.generate(seed=501, template='three_number_mixed')

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        self.assertFalse(malrule_solution.is_correct)
        self.assertTrue(correct_solution.is_correct)

        # Answers should match metadata
        self.assertEqual(malrule_solution.answer, problem.metadata['malrule_answer'])
        self.assertEqual(correct_solution.answer, problem.metadata['correct_answer'])

    def test_three_number_mixed_calculate_expected_answer(self):
        """Test calculate_expected_answer for three_number_mixed template."""
        problem = self.generator.generate(seed=502, template='three_number_mixed')

        expected_answer = self.malrule.calculate_expected_answer(problem)
        malrule_solution = self.malrule.solve(problem)

        self.assertEqual(expected_answer, malrule_solution.answer)

    # Additional edge case tests
    def test_all_templates_available(self):
        """Test that get_available_templates returns exactly 6 templates."""
        templates = self.generator.get_available_templates()

        self.assertEqual(len(templates), 6)
        self.assertIn('basic_addition', templates)
        self.assertIn('basic_subtraction', templates)
        self.assertIn('money_word_problem', templates)
        self.assertIn('measurement_word_problem', templates)
        self.assertIn('three_number_mixed', templates)
        self.assertIn('word_problem_context', templates)

    def test_random_template_selection(self):
        """Test that generate() works without explicit template."""
        problem = self.generator.generate(seed=999)

        self.assertIn('template', problem.metadata)
        self.assertIn(problem.metadata['template'], self.generator.get_available_templates())

    def test_invalid_template_raises_error(self):
        """Test that invalid template raises ValueError."""
        with self.assertRaises(ValueError):
            self.generator.generate(seed=1000, template='invalid_template')



class TestRightAlignDecimalsAutomated(unittest.TestCase):
    """Automated test suite runner."""

    def test_automated_suite(self):
        """Run the automated test suite."""
        problem_gen = RightAlignDecimalsProblemGenerator(
            level=5,
            difficulty=DifficultyLevel.MEDIUM
        )
        malrule = RightAlignDecimalsMalrule()
        correct = DecimalAdditionCorrectAlgorithm()

        test_suite = MalruleTest(malrule, correct, problem_gen)
        results = test_suite.run_all_tests(verbose=False)

        all_passed = all(r.passed for r in results)
        self.assertTrue(all_passed,
                       f"Automated tests failed: {[r.message for r in results if not r.passed]}")


def main():
    """Main entry point for standalone execution."""
    print("\n╔" + "═"*68 + "╗")
    print("║" + "  VERIFICATION TEST: Right Align Decimals  ".center(70) + "║")
    print("╚" + "═"*68 + "╝\n")

    # Run unittest
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestRightAlignDecimalsTemplates))
    suite.addTests(loader.loadTestsFromTestCase(TestRightAlignDecimalsAutomated))

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
