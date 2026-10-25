#!/usr/bin/env python3
"""
Comprehensive test suite for Strict Left To Right malrule.

This file combines:
1. Template validation tests (all templates)
2. Automated test suite functionality

Run from project root: python3 -m malrules.order_of_operations.strict_left_to_right.test_malrule
Or from this directory: python3 test_malrule.py
"""

import sys
import os
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.order_of_operations.strict_left_to_right import (
    OrderOfOperationsProblemGenerator,
    StrictLeftToRightMalrule,
    OrderOfOperationsCorrectAlgorithm
)


class TestStrictLeftToRightTemplates(unittest.TestCase):
    """Test all 5 templates for Strict-Left-To-Right malrule."""

    def setUp(self):
        """Set up test fixtures."""
        self.generator = OrderOfOperationsProblemGenerator(
            level=6,
            difficulty=DifficultyLevel.MEDIUM
        )
        self.malrule = StrictLeftToRightMalrule()
        self.correct_algo = OrderOfOperationsCorrectAlgorithm()

    # Template 1: add_mult
    def test_add_mult_template(self):
        """Test add_mult template generates valid problems."""
        problem = self.generator.generate(seed=100, template='add_mult')

        self.assertEqual(problem.metadata['template'], 'add_mult')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)
        self.assertEqual(problem.metadata['operations'], ['+', '×'])

    def test_add_mult_malrule_vs_correct(self):
        """Test add_mult: malrule evaluates left-to-right incorrectly."""
        problem = self.generator.generate(seed=101, template='add_mult')

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        self.assertFalse(malrule_solution.is_correct)
        self.assertTrue(correct_solution.is_correct)

        self.assertEqual(malrule_solution.answer, str(problem.metadata['malrule_answer']))
        self.assertEqual(correct_solution.answer, str(problem.metadata['correct_answer']))

    def test_add_mult_calculate_expected_answer(self):
        """Test calculate_expected_answer for add_mult template."""
        problem = self.generator.generate(seed=102, template='add_mult')

        expected_answer = self.malrule.calculate_expected_answer(problem)
        malrule_solution = self.malrule.solve(problem)

        self.assertEqual(expected_answer, malrule_solution.answer)

    # Template 2: sub_mult
    def test_sub_mult_template(self):
        """Test sub_mult template generates valid problems."""
        problem = self.generator.generate(seed=200, template='sub_mult')

        self.assertEqual(problem.metadata['template'], 'sub_mult')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)
        self.assertEqual(problem.metadata['operations'], ['-', '×'])

    def test_sub_mult_malrule_vs_correct(self):
        """Test sub_mult: malrule evaluates left-to-right incorrectly."""
        problem = self.generator.generate(seed=201, template='sub_mult')

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        self.assertFalse(malrule_solution.is_correct)
        self.assertTrue(correct_solution.is_correct)

    def test_sub_mult_calculate_expected_answer(self):
        """Test calculate_expected_answer for sub_mult template."""
        problem = self.generator.generate(seed=202, template='sub_mult')

        expected_answer = self.malrule.calculate_expected_answer(problem)
        malrule_solution = self.malrule.solve(problem)

        self.assertEqual(expected_answer, malrule_solution.answer)

    # Template 3: add_div
    def test_add_div_template(self):
        """Test add_div template generates valid problems."""
        problem = self.generator.generate(seed=300, template='add_div')

        self.assertEqual(problem.metadata['template'], 'add_div')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)
        self.assertEqual(problem.metadata['operations'], ['+', '÷'])

    def test_add_div_malrule_vs_correct(self):
        """Test add_div: malrule evaluates left-to-right incorrectly."""
        problem = self.generator.generate(seed=301, template='add_div')

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        self.assertFalse(malrule_solution.is_correct)
        self.assertTrue(correct_solution.is_correct)

    def test_add_div_calculate_expected_answer(self):
        """Test calculate_expected_answer for add_div template."""
        problem = self.generator.generate(seed=302, template='add_div')

        expected_answer = self.malrule.calculate_expected_answer(problem)
        malrule_solution = self.malrule.solve(problem)

        self.assertEqual(expected_answer, malrule_solution.answer)

    # Template 4: sub_div
    def test_sub_div_template(self):
        """Test sub_div template generates valid problems."""
        problem = self.generator.generate(seed=400, template='sub_div')

        self.assertEqual(problem.metadata['template'], 'sub_div')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)
        self.assertEqual(problem.metadata['operations'], ['-', '÷'])

    def test_sub_div_malrule_vs_correct(self):
        """Test sub_div: malrule evaluates left-to-right incorrectly."""
        problem = self.generator.generate(seed=401, template='sub_div')

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        self.assertFalse(malrule_solution.is_correct)
        self.assertTrue(correct_solution.is_correct)

    def test_sub_div_calculate_expected_answer(self):
        """Test calculate_expected_answer for sub_div template."""
        problem = self.generator.generate(seed=402, template='sub_div')

        expected_answer = self.malrule.calculate_expected_answer(problem)
        malrule_solution = self.malrule.solve(problem)

        self.assertEqual(expected_answer, malrule_solution.answer)

    # Template 5: word_problem
    def test_word_problem_template(self):
        """Test word_problem template generates valid problems."""
        problem = self.generator.generate(seed=500, template='word_problem')

        self.assertEqual(problem.metadata['template'], 'word_problem')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)

        # Should have word problem context
        self.assertIn('expression', problem.metadata)

    def test_word_problem_malrule_vs_correct(self):
        """Test word_problem: malrule evaluates left-to-right incorrectly."""
        problem = self.generator.generate(seed=501, template='word_problem')

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        self.assertFalse(malrule_solution.is_correct)
        self.assertTrue(correct_solution.is_correct)

    def test_word_problem_calculate_expected_answer(self):
        """Test calculate_expected_answer for word_problem template."""
        problem = self.generator.generate(seed=502, template='word_problem')

        expected_answer = self.malrule.calculate_expected_answer(problem)
        malrule_solution = self.malrule.solve(problem)

        self.assertEqual(expected_answer, malrule_solution.answer)



class TestStrictLeftToRightAutomated(unittest.TestCase):
    """Automated test suite runner."""

    def test_automated_suite(self):
        """Run the automated test suite."""
        problem_gen = OrderOfOperationsProblemGenerator(
            level=5,
            difficulty=DifficultyLevel.MEDIUM
        )
        malrule = StrictLeftToRightMalrule()
        correct = OrderOfOperationsCorrectAlgorithm()

        test_suite = MalruleTest(malrule, correct, problem_gen)
        results = test_suite.run_all_tests(verbose=False)

        all_passed = all(r.passed for r in results)
        self.assertTrue(all_passed,
                       f"Automated tests failed: {[r.message for r in results if not r.passed]}")


def main():
    """Main entry point for standalone execution."""
    print("\n╔" + "═"*68 + "╗")
    print("║" + "  VERIFICATION TEST: Strict Left To Right  ".center(70) + "║")
    print("╚" + "═"*68 + "╝\n")

    # Run unittest
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestStrictLeftToRightTemplates))
    suite.addTests(loader.loadTestsFromTestCase(TestStrictLeftToRightAutomated))

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
