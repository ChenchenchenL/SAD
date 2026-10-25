#!/usr/bin/env python3
"""
Comprehensive test suite for Multiplication Before Division Always malrule.

This file combines:
1. Template validation tests (all templates)
2. Automated test suite functionality

Run from project root: python3 -m malrules.order_of_operations.multiplication_before_division_always.test_malrule
Or from this directory: python3 test_malrule.py
"""

import sys
import os
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.order_of_operations.multiplication_before_division_always import (
    MultiplicationDivisionOrderProblemGenerator,
    MultiplicationBeforeDivisionAlwaysMalrule,
    OrderOfOperationsCorrectAlgorithm
)


class TestMultiplicationBeforeDivisionAlwaysTemplates(unittest.TestCase):
    """Test all 5 templates for Multiplication-Before-Division-Always malrule."""

    def setUp(self):
        """Set up test fixtures."""
        self.generator = MultiplicationDivisionOrderProblemGenerator(
            level=7,
            difficulty=DifficultyLevel.MEDIUM
        )
        self.malrule = MultiplicationBeforeDivisionAlwaysMalrule()
        self.correct_algo = OrderOfOperationsCorrectAlgorithm()

    # Template 1: basic_expression
    def test_basic_expression_template(self):
        """Test basic_expression template generates valid problems."""
        problem = self.generator.generate(seed=100, template='basic_expression')

        self.assertEqual(problem.metadata['template'], 'basic_expression')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)
        self.assertIn('expression', problem.metadata)
        self.assertIn('÷', problem.metadata['expression'])
        self.assertIn('×', problem.metadata['expression'])

    def test_basic_expression_malrule_vs_correct(self):
        """Test basic_expression: malrule gives wrong answer, correct gives right answer."""
        problem = self.generator.generate(seed=101, template='basic_expression')

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        self.assertFalse(malrule_solution.is_correct)
        self.assertTrue(correct_solution.is_correct)

        self.assertEqual(malrule_solution.answer, str(problem.metadata['malrule_answer']))
        self.assertEqual(correct_solution.answer, str(problem.metadata['correct_answer']))

        # Verify they give different answers (malrule is wrong)
        self.assertNotEqual(malrule_solution.answer, correct_solution.answer)

    def test_basic_expression_calculate_expected_answer(self):
        """Test calculate_expected_answer for basic_expression template."""
        problem = self.generator.generate(seed=102, template='basic_expression')

        expected_answer = self.malrule.calculate_expected_answer(problem)
        malrule_solution = self.malrule.solve(problem)

        self.assertEqual(expected_answer, malrule_solution.answer)
        self.assertEqual(expected_answer, str(problem.metadata['malrule_answer']))

    # Template 2: word_problem_sharing
    def test_word_problem_sharing_template(self):
        """Test word_problem_sharing template generates valid problems."""
        problem = self.generator.generate(seed=200, template='word_problem_sharing')

        self.assertEqual(problem.metadata['template'], 'word_problem_sharing')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)

        # Should mention sharing/dividing context
        self.assertTrue(
            any(word in problem.text.lower() for word in ['divided', 'split', 'shared', 'equally', 'groups', 'piles', 'children'])
        )

    def test_word_problem_sharing_malrule_vs_correct(self):
        """Test word_problem_sharing: malrule incorrectly does multiplication first."""
        problem = self.generator.generate(seed=201, template='word_problem_sharing')

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        self.assertFalse(malrule_solution.is_correct)
        self.assertTrue(correct_solution.is_correct)

        self.assertEqual(malrule_solution.answer, str(problem.metadata['malrule_answer']))
        self.assertEqual(correct_solution.answer, str(problem.metadata['correct_answer']))

        # Verify they give different answers
        self.assertNotEqual(malrule_solution.answer, correct_solution.answer)

    def test_word_problem_sharing_calculate_expected_answer(self):
        """Test calculate_expected_answer for word_problem_sharing template."""
        problem = self.generator.generate(seed=202, template='word_problem_sharing')

        expected_answer = self.malrule.calculate_expected_answer(problem)
        malrule_solution = self.malrule.solve(problem)

        self.assertEqual(expected_answer, malrule_solution.answer)

    # Template 3: word_problem_measurement
    def test_word_problem_measurement_template(self):
        """Test word_problem_measurement template generates valid problems."""
        problem = self.generator.generate(seed=300, template='word_problem_measurement')

        self.assertEqual(problem.metadata['template'], 'word_problem_measurement')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)
        self.assertIn('unit', problem.metadata)

        # Should mention measurement context
        self.assertTrue(
            any(word in problem.text.lower() for word in ['meters', 'feet', 'inches', 'liters', 'kilograms'])
        )

        # Answers should have units
        self.assertIn(problem.metadata['unit'], problem.metadata['correct_answer'])
        self.assertIn(problem.metadata['unit'], problem.metadata['malrule_answer'])

    def test_word_problem_measurement_malrule_vs_correct(self):
        """Test word_problem_measurement: malrule misapplies rule in measurement context."""
        problem = self.generator.generate(seed=301, template='word_problem_measurement')

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        self.assertFalse(malrule_solution.is_correct)
        self.assertTrue(correct_solution.is_correct)

        # Both should have units
        self.assertIn(problem.metadata['unit'], malrule_solution.answer)
        self.assertIn(problem.metadata['unit'], correct_solution.answer)

    def test_word_problem_measurement_calculate_expected_answer(self):
        """Test calculate_expected_answer for word_problem_measurement template."""
        problem = self.generator.generate(seed=302, template='word_problem_measurement')

        expected_answer = self.malrule.calculate_expected_answer(problem)
        malrule_solution = self.malrule.solve(problem)

        # Both should match (with unit)
        self.assertEqual(expected_answer, malrule_solution.answer)

    # Template 4: word_problem_money
    def test_word_problem_money_template(self):
        """Test word_problem_money template generates valid problems."""
        problem = self.generator.generate(seed=400, template='word_problem_money')

        self.assertEqual(problem.metadata['template'], 'word_problem_money')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)

        # Should mention money/currency context
        self.assertTrue(
            any(word in problem.text.lower() for word in ['$', 'dollar', 'money', 'prize', 'divide'])
        )

        # Answers should have $ symbol
        self.assertTrue(problem.metadata['correct_answer'].startswith('$'))
        self.assertTrue(problem.metadata['malrule_answer'].startswith('$'))

    def test_word_problem_money_malrule_vs_correct(self):
        """Test word_problem_money: malrule misapplies rule in money context."""
        problem = self.generator.generate(seed=401, template='word_problem_money')

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        self.assertFalse(malrule_solution.is_correct)
        self.assertTrue(correct_solution.is_correct)

        # Both should have $ symbol
        self.assertTrue(malrule_solution.answer.startswith('$'))
        self.assertTrue(correct_solution.answer.startswith('$'))

        # Verify they give different answers
        self.assertNotEqual(malrule_solution.answer, correct_solution.answer)

    def test_word_problem_money_calculate_expected_answer(self):
        """Test calculate_expected_answer for word_problem_money template."""
        problem = self.generator.generate(seed=402, template='word_problem_money')

        expected_answer = self.malrule.calculate_expected_answer(problem)
        malrule_solution = self.malrule.solve(problem)

        # Both should match (with $ symbol)
        self.assertEqual(expected_answer, malrule_solution.answer)

    # Template 5: multi_operation_chain
    def test_multi_operation_chain_template(self):
        """Test multi_operation_chain template generates valid problems."""
        problem = self.generator.generate(seed=500, template='multi_operation_chain')

        self.assertEqual(problem.metadata['template'], 'multi_operation_chain')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)

        # Should have 4 operands (a, d1, m, d2)
        self.assertEqual(len(problem.operands), 4)

        # Expression should have multiple operations
        expression = problem.metadata['expression']
        self.assertEqual(expression.count('÷'), 2)  # Two division operations
        self.assertEqual(expression.count('×'), 1)  # One multiplication operation

    def test_multi_operation_chain_malrule_vs_correct(self):
        """Test multi_operation_chain: malrule misapplies rule in multi-step operations."""
        problem = self.generator.generate(seed=501, template='multi_operation_chain')

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        self.assertFalse(malrule_solution.is_correct)
        self.assertTrue(correct_solution.is_correct)

        self.assertEqual(malrule_solution.answer, str(problem.metadata['malrule_answer']))
        self.assertEqual(correct_solution.answer, str(problem.metadata['correct_answer']))

        # Verify they give different answers
        self.assertNotEqual(malrule_solution.answer, correct_solution.answer)

    def test_multi_operation_chain_calculate_expected_answer(self):
        """Test calculate_expected_answer for multi_operation_chain template."""
        problem = self.generator.generate(seed=502, template='multi_operation_chain')

        expected_answer = self.malrule.calculate_expected_answer(problem)
        malrule_solution = self.malrule.solve(problem)

        self.assertEqual(expected_answer, malrule_solution.answer)

    # Additional test: verify all templates are available
    def test_get_available_templates(self):
        """Test that get_available_templates returns all 5 templates."""
        templates = self.generator.get_available_templates()

        self.assertEqual(len(templates), 5)
        self.assertIn('basic_expression', templates)
        self.assertIn('word_problem_sharing', templates)
        self.assertIn('word_problem_measurement', templates)
        self.assertIn('word_problem_money', templates)
        self.assertIn('multi_operation_chain', templates)

    # Additional test: verify template parameter works
    def test_template_parameter(self):
        """Test that specifying a template parameter works correctly."""
        for template in self.generator.get_available_templates():
            problem = self.generator.generate(seed=999, template=template)
            self.assertEqual(problem.metadata['template'], template)

    # Additional test: verify invalid template raises error
    def test_invalid_template_raises_error(self):
        """Test that specifying an invalid template raises ValueError."""
        with self.assertRaises(ValueError):
            self.generator.generate(seed=999, template='invalid_template_name')



class TestMultiplicationBeforeDivisionAlwaysAutomated(unittest.TestCase):
    """Automated test suite runner."""

    def test_automated_suite(self):
        """Run the automated test suite."""
        problem_gen = MultiplicationDivisionOrderProblemGenerator(
            level=5,
            difficulty=DifficultyLevel.MEDIUM
        )
        malrule = MultiplicationBeforeDivisionAlwaysMalrule()
        correct = OrderOfOperationsCorrectAlgorithm()

        test_suite = MalruleTest(malrule, correct, problem_gen)
        results = test_suite.run_all_tests(verbose=False)

        all_passed = all(r.passed for r in results)
        self.assertTrue(all_passed,
                       f"Automated tests failed: {[r.message for r in results if not r.passed]}")


def main():
    """Main entry point for standalone execution."""
    print("\n╔" + "═"*68 + "╗")
    print("║" + "  VERIFICATION TEST: Multiplication Before Division Always  ".center(70) + "║")
    print("╚" + "═"*68 + "╝\n")

    # Run unittest
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestMultiplicationBeforeDivisionAlwaysTemplates))
    suite.addTests(loader.loadTestsFromTestCase(TestMultiplicationBeforeDivisionAlwaysAutomated))

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
