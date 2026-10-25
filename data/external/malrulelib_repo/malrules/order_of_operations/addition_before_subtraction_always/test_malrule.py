#!/usr/bin/env python3
"""
Comprehensive test suite for Addition Before Subtraction Always malrule.

This file combines:
1. Template validation tests (all templates)
2. Automated test suite functionality

Run from project root: python3 -m malrules.order_of_operations.addition_before_subtraction_always.test_malrule
Or from this directory: python3 test_malrule.py
"""

import sys
import os
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.order_of_operations.addition_before_subtraction_always import (
    AdditionSubtractionOrderProblemGenerator,
    AdditionBeforeSubtractionAlwaysMalrule,
    AddSubOrderCorrectAlgorithm
)


class TestAdditionBeforeSubtractionAlwaysTemplates(unittest.TestCase):
    """Test all 5 templates for Addition-Before-Subtraction-Always malrule."""

    def setUp(self):
        """Set up test fixtures."""
        self.generator = AdditionSubtractionOrderProblemGenerator(
            level=7,
            difficulty=DifficultyLevel.MEDIUM
        )
        self.malrule = AdditionBeforeSubtractionAlwaysMalrule()
        self.correct_algo = AddSubOrderCorrectAlgorithm()

    # Template 1: simple_expression
    def test_simple_expression_template(self):
        """Test simple_expression template generates valid problems."""
        problem = self.generator.generate(seed=100, template='simple_expression')

        self.assertEqual(problem.metadata['template'], 'simple_expression')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)
        self.assertIn('a', problem.metadata)
        self.assertIn('b', problem.metadata)
        self.assertIn('c', problem.metadata)
        self.assertIn('expression', problem.metadata)

        # Verify expression format: a - b + c
        expression = problem.metadata['expression']
        self.assertIn('-', expression)
        self.assertIn('+', expression)

    def test_simple_expression_malrule_vs_correct(self):
        """Test simple_expression: malrule gives wrong answer, correct gives right answer."""
        problem = self.generator.generate(seed=101, template='simple_expression')

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        self.assertFalse(malrule_solution.is_correct)
        self.assertTrue(correct_solution.is_correct)

        self.assertEqual(malrule_solution.answer, str(problem.metadata['malrule_answer']))
        self.assertEqual(correct_solution.answer, str(problem.metadata['correct_answer']))

        # Malrule should give different answer than correct (because it does addition first)
        self.assertNotEqual(malrule_solution.answer, correct_solution.answer)

    def test_simple_expression_calculate_expected_answer(self):
        """Test calculate_expected_answer for simple_expression template."""
        problem = self.generator.generate(seed=102, template='simple_expression')

        expected_answer = self.malrule.calculate_expected_answer(problem)
        malrule_solution = self.malrule.solve(problem)

        self.assertEqual(expected_answer, malrule_solution.answer)
        self.assertEqual(expected_answer, str(problem.metadata['malrule_answer']))

    # Template 2: money_transaction
    def test_money_transaction_template(self):
        """Test money_transaction template generates valid problems."""
        problem = self.generator.generate(seed=200, template='money_transaction')

        self.assertEqual(problem.metadata['template'], 'money_transaction')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)

        # Should mention money context
        self.assertTrue(
            any(word in problem.text.lower() for word in ['$', 'money', 'spend', 'earn', 'account', 'balance', 'withdraw', 'deposit', 'savings', 'bill', 'refund'])
        )

        # Answers should have $ symbol
        self.assertTrue(problem.metadata['correct_answer'].startswith('$'))
        self.assertTrue(problem.metadata['malrule_answer'].startswith('$'))

    def test_money_transaction_malrule_vs_correct(self):
        """Test money_transaction: malrule incorrectly does addition before subtraction."""
        problem = self.generator.generate(seed=201, template='money_transaction')

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        self.assertFalse(malrule_solution.is_correct)
        self.assertTrue(correct_solution.is_correct)

        self.assertEqual(malrule_solution.answer, str(problem.metadata['malrule_answer']))
        self.assertEqual(correct_solution.answer, str(problem.metadata['correct_answer']))

        # Malrule should give different answer than correct
        self.assertNotEqual(malrule_solution.answer, correct_solution.answer)

    def test_money_transaction_calculate_expected_answer(self):
        """Test calculate_expected_answer for money_transaction template."""
        problem = self.generator.generate(seed=202, template='money_transaction')

        expected_answer = self.malrule.calculate_expected_answer(problem)
        malrule_solution = self.malrule.solve(problem)

        self.assertEqual(expected_answer, malrule_solution.answer)
        self.assertEqual(expected_answer, str(problem.metadata['malrule_answer']))

    # Template 3: temperature_change
    def test_temperature_change_template(self):
        """Test temperature_change template generates valid problems."""
        problem = self.generator.generate(seed=300, template='temperature_change')

        self.assertEqual(problem.metadata['template'], 'temperature_change')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)
        self.assertIn('unit', problem.metadata)

        # Should mention temperature context
        self.assertTrue(
            any(word in problem.text.lower() for word in ['temperature', 'temp', 'drop', 'rise', 'decrease', 'increase', 'fall', 'climb'])
        )

        # Answers should have degree symbol
        self.assertTrue('°' in problem.metadata['correct_answer'])
        self.assertTrue('°' in problem.metadata['malrule_answer'])

    def test_temperature_change_malrule_vs_correct(self):
        """Test temperature_change: malrule misapplies rule in temperature context."""
        problem = self.generator.generate(seed=301, template='temperature_change')

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        self.assertFalse(malrule_solution.is_correct)
        self.assertTrue(correct_solution.is_correct)

        self.assertEqual(malrule_solution.answer, str(problem.metadata['malrule_answer']))
        self.assertEqual(correct_solution.answer, str(problem.metadata['correct_answer']))

        # Malrule should give different answer than correct
        self.assertNotEqual(malrule_solution.answer, correct_solution.answer)

    def test_temperature_change_calculate_expected_answer(self):
        """Test calculate_expected_answer for temperature_change template."""
        problem = self.generator.generate(seed=302, template='temperature_change')

        expected_answer = self.malrule.calculate_expected_answer(problem)
        malrule_solution = self.malrule.solve(problem)

        # Both should match
        self.assertEqual(expected_answer, malrule_solution.answer)
        self.assertEqual(expected_answer, str(problem.metadata['malrule_answer']))

    # Template 4: elevation_change
    def test_elevation_change_template(self):
        """Test elevation_change template generates valid problems."""
        problem = self.generator.generate(seed=400, template='elevation_change')

        self.assertEqual(problem.metadata['template'], 'elevation_change')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)
        self.assertIn('unit', problem.metadata)

        # Should mention elevation/altitude context
        self.assertTrue(
            any(word in problem.text.lower() for word in ['elevation', 'altitude', 'height', 'descend', 'climb', 'down', 'up', 'drone', 'ascend'])
        )

        # Answers should have elevation unit (m, ft, meters, feet)
        unit = problem.metadata['unit']
        self.assertTrue(problem.metadata['correct_answer'].endswith(unit))
        self.assertTrue(problem.metadata['malrule_answer'].endswith(unit))

    def test_elevation_change_malrule_vs_correct(self):
        """Test elevation_change: malrule misapplies rule in elevation context."""
        problem = self.generator.generate(seed=401, template='elevation_change')

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        self.assertFalse(malrule_solution.is_correct)
        self.assertTrue(correct_solution.is_correct)

        self.assertEqual(malrule_solution.answer, str(problem.metadata['malrule_answer']))
        self.assertEqual(correct_solution.answer, str(problem.metadata['correct_answer']))

        # Malrule should give different answer than correct
        self.assertNotEqual(malrule_solution.answer, correct_solution.answer)

    def test_elevation_change_calculate_expected_answer(self):
        """Test calculate_expected_answer for elevation_change template."""
        problem = self.generator.generate(seed=402, template='elevation_change')

        expected_answer = self.malrule.calculate_expected_answer(problem)
        malrule_solution = self.malrule.solve(problem)

        # Both should match
        self.assertEqual(expected_answer, malrule_solution.answer)
        self.assertEqual(expected_answer, str(problem.metadata['malrule_answer']))

    # Template 5: score_tracking
    def test_score_tracking_template(self):
        """Test score_tracking template generates valid problems."""
        problem = self.generator.generate(seed=500, template='score_tracking')

        self.assertEqual(problem.metadata['template'], 'score_tracking')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)

        # Should mention score/points context
        self.assertTrue(
            any(word in problem.text.lower() for word in ['score', 'points', 'point', 'lose', 'gain', 'penalty', 'bonus', 'deduct', 'award'])
        )

        # Answers should have " points" suffix
        self.assertTrue(problem.metadata['correct_answer'].endswith(' points'))
        self.assertTrue(problem.metadata['malrule_answer'].endswith(' points'))

    def test_score_tracking_malrule_vs_correct(self):
        """Test score_tracking: malrule misapplies rule in score context."""
        problem = self.generator.generate(seed=501, template='score_tracking')

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        self.assertFalse(malrule_solution.is_correct)
        self.assertTrue(correct_solution.is_correct)

        self.assertEqual(malrule_solution.answer, str(problem.metadata['malrule_answer']))
        self.assertEqual(correct_solution.answer, str(problem.metadata['correct_answer']))

        # Malrule should give different answer than correct
        self.assertNotEqual(malrule_solution.answer, correct_solution.answer)

    def test_score_tracking_calculate_expected_answer(self):
        """Test calculate_expected_answer for score_tracking template."""
        problem = self.generator.generate(seed=502, template='score_tracking')

        expected_answer = self.malrule.calculate_expected_answer(problem)
        malrule_solution = self.malrule.solve(problem)

        # Both should match
        self.assertEqual(expected_answer, malrule_solution.answer)
        self.assertEqual(expected_answer, str(problem.metadata['malrule_answer']))



class TestAdditionBeforeSubtractionAlwaysAutomated(unittest.TestCase):
    """Automated test suite runner."""

    def test_automated_suite(self):
        """Run the automated test suite."""
        problem_gen = AdditionSubtractionOrderProblemGenerator(
            level=5,
            difficulty=DifficultyLevel.MEDIUM
        )
        malrule = AdditionBeforeSubtractionAlwaysMalrule()
        correct = AddSubOrderCorrectAlgorithm()

        test_suite = MalruleTest(malrule, correct, problem_gen)
        results = test_suite.run_all_tests(verbose=False)

        all_passed = all(r.passed for r in results)
        self.assertTrue(all_passed,
                       f"Automated tests failed: {[r.message for r in results if not r.passed]}")


def main():
    """Main entry point for standalone execution."""
    print("\n╔" + "═"*68 + "╗")
    print("║" + "  VERIFICATION TEST: Addition Before Subtraction Always  ".center(70) + "║")
    print("╚" + "═"*68 + "╝\n")

    # Run unittest
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestAdditionBeforeSubtractionAlwaysTemplates))
    suite.addTests(loader.loadTestsFromTestCase(TestAdditionBeforeSubtractionAlwaysAutomated))

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
