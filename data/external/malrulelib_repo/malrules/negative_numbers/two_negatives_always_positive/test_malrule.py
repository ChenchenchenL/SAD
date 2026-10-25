#!/usr/bin/env python3
"""
Comprehensive test suite for Two Negatives Always Positive malrule.

This file combines:
1. Template validation tests (all templates)
2. Automated test suite functionality

Run from project root: python3 -m malrules.negative_numbers.two_negatives_always_positive.test_malrule
Or from this directory: python3 test_malrule.py
"""

import sys
import os
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.negative_numbers.two_negatives_always_positive import (
    NegativeSubtractionProblemGenerator,
    TwoNegativesAlwaysPositiveMalrule,
    NegativeSubtractionCorrectAlgorithm
)


class TestTwoNegativesAlwaysPositiveTemplates(unittest.TestCase):
    """Test all 5 templates for Two-Negatives-Always-Positive malrule."""

    def setUp(self):
        """Set up test fixtures."""
        self.generator = NegativeSubtractionProblemGenerator(
            level=7,
            difficulty=DifficultyLevel.MEDIUM
        )
        self.malrule = TwoNegativesAlwaysPositiveMalrule()
        self.correct_algo = NegativeSubtractionCorrectAlgorithm()

    # Template 1: basic_subtraction
    def test_basic_subtraction_template(self):
        """Test basic_subtraction template generates valid problems."""
        problem = self.generator.generate(seed=100, template='basic_subtraction')

        self.assertEqual(problem.metadata['template'], 'basic_subtraction')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)
        self.assertIn('num1', problem.metadata)
        self.assertIn('num2', problem.metadata)

    def test_basic_subtraction_malrule_vs_correct(self):
        """Test basic_subtraction: malrule gives wrong answer, correct gives right answer."""
        problem = self.generator.generate(seed=101, template='basic_subtraction')

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        self.assertFalse(malrule_solution.is_correct)
        self.assertTrue(correct_solution.is_correct)

        # Verify answers match metadata (to ensure algorithms compute correctly)
        expected_correct = str(problem.metadata['correct_answer'])
        expected_malrule = str(problem.metadata['malrule_answer'])

        if correct_solution.answer == expected_correct and malrule_solution.answer == expected_malrule:
            print(f"\n  ✓ basic_subtraction: Correct={correct_solution.answer}, Malrule={malrule_solution.answer}")
        else:
            print(f"\n  ✗ basic_subtraction FAILED:")
            print(f"    Problem: {problem.text}")
            print(f"    Expected correct: {expected_correct}, Got: {correct_solution.answer}")
            print(f"    Expected malrule: {expected_malrule}, Got: {malrule_solution.answer}")
            print(f"\n    Correct steps:")
            for step in correct_solution.steps:
                print(f"      {step}")
            print(f"\n    Malrule steps:")
            for step in malrule_solution.steps:
                print(f"      {step}")

        self.assertEqual(correct_solution.answer, expected_correct)
        self.assertEqual(malrule_solution.answer, expected_malrule)

        # Edge case: malrule accidentally gets correct answer
        if malrule_solution.answer == correct_solution.answer:
            print(f"    ⚠ WARNING: Malrule accidentally produced correct answer!")
            print(f"    Malrule steps:")
            for step in malrule_solution.steps:
                print(f"      {step}")
            self.fail("Malrule produced same answer as correct algorithm - this is an edge case")

    def test_basic_subtraction_calculate_expected_answer(self):
        """Test calculate_expected_answer for basic_subtraction template."""
        problem = self.generator.generate(seed=102, template='basic_subtraction')

        expected_answer = self.malrule.calculate_expected_answer(problem)
        malrule_solution = self.malrule.solve(problem)

        self.assertEqual(expected_answer, malrule_solution.answer)
        self.assertEqual(expected_answer, str(problem.metadata['malrule_answer']))

    # Template 2: addition_negatives
    def test_addition_negatives_template(self):
        """Test addition_negatives template generates valid problems."""
        problem = self.generator.generate(seed=200, template='addition_negatives')

        self.assertEqual(problem.metadata['template'], 'addition_negatives')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)

        # Should have two negative operands
        self.assertTrue(problem.operands[0] < 0)
        self.assertTrue(problem.operands[1] < 0)

    def test_addition_negatives_malrule_vs_correct(self):
        """Test addition_negatives: malrule incorrectly makes result positive."""
        problem = self.generator.generate(seed=201, template='addition_negatives')

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        self.assertFalse(malrule_solution.is_correct)
        self.assertTrue(correct_solution.is_correct)

        # Verify answers match metadata
        expected_correct = str(problem.metadata['correct_answer'])
        expected_malrule = str(problem.metadata['malrule_answer'])

        if correct_solution.answer == expected_correct and malrule_solution.answer == expected_malrule:
            print(f"\n  ✓ addition_negatives: Correct={correct_solution.answer}, Malrule={malrule_solution.answer}")
        else:
            print(f"\n  ✗ addition_negatives FAILED:")
            print(f"    Problem: {problem.text}")
            print(f"    Expected correct: {expected_correct}, Got: {correct_solution.answer}")
            print(f"    Expected malrule: {expected_malrule}, Got: {malrule_solution.answer}")
            print(f"\n    Correct steps:")
            for step in correct_solution.steps:
                print(f"      {step}")
            print(f"\n    Malrule steps:")
            for step in malrule_solution.steps:
                print(f"      {step}")

        self.assertEqual(correct_solution.answer, expected_correct)
        self.assertEqual(malrule_solution.answer, expected_malrule)

        # Edge case: malrule accidentally gets correct answer
        if malrule_solution.answer == correct_solution.answer:
            print(f"    ⚠ WARNING: Malrule accidentally produced correct answer!")
            print(f"    Malrule steps:")
            for step in malrule_solution.steps:
                print(f"      {step}")
            self.fail("Malrule produced same answer as correct algorithm - this is an edge case")

    def test_addition_negatives_calculate_expected_answer(self):
        """Test calculate_expected_answer for addition_negatives template."""
        problem = self.generator.generate(seed=202, template='addition_negatives')

        expected_answer = self.malrule.calculate_expected_answer(problem)
        malrule_solution = self.malrule.solve(problem)

        self.assertEqual(expected_answer, malrule_solution.answer)

    # Template 3: word_problem_temp
    def test_word_problem_temp_template(self):
        """Test word_problem_temp template generates valid problems."""
        problem = self.generator.generate(seed=300, template='word_problem_temp')

        self.assertEqual(problem.metadata['template'], 'word_problem_temp')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)

        # Should mention temperature context
        self.assertTrue(
            any(word in problem.text.lower() for word in ['temperature', 'temp', '°c', '°f', 'drop', 'decrease'])
        )

        # Answers should have degree symbol
        self.assertTrue('°' in problem.metadata['correct_answer'])
        self.assertTrue('°' in problem.metadata['malrule_answer'])

    def test_word_problem_temp_malrule_vs_correct(self):
        """Test word_problem_temp: malrule misapplies rule in temperature context."""
        problem = self.generator.generate(seed=301, template='word_problem_temp')

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        self.assertFalse(malrule_solution.is_correct)
        self.assertTrue(correct_solution.is_correct)

        # Verify answers match metadata
        expected_correct = str(problem.metadata['correct_answer'])
        expected_malrule = str(problem.metadata['malrule_answer'])

        if correct_solution.answer == expected_correct and malrule_solution.answer == expected_malrule:
            print(f"\n  ✓ word_problem_temp: Correct={correct_solution.answer}, Malrule={malrule_solution.answer}")
        else:
            print(f"\n  ✗ word_problem_temp FAILED:")
            print(f"    Problem: {problem.text}")
            print(f"    Expected correct: {expected_correct}, Got: {correct_solution.answer}")
            print(f"    Expected malrule: {expected_malrule}, Got: {malrule_solution.answer}")
            print(f"\n    Correct steps:")
            for step in correct_solution.steps:
                print(f"      {step}")
            print(f"\n    Malrule steps:")
            for step in malrule_solution.steps:
                print(f"      {step}")

        self.assertEqual(correct_solution.answer, expected_correct)
        self.assertEqual(malrule_solution.answer, expected_malrule)

        # Edge case: malrule accidentally gets correct answer
        if malrule_solution.answer == correct_solution.answer:
            print(f"    ⚠ WARNING: Malrule accidentally produced correct answer!")
            print(f"    Malrule steps:")
            for step in malrule_solution.steps:
                print(f"      {step}")
            self.fail("Malrule produced same answer as correct algorithm - this is an edge case")

    def test_word_problem_temp_calculate_expected_answer(self):
        """Test calculate_expected_answer for word_problem_temp template."""
        problem = self.generator.generate(seed=302, template='word_problem_temp')

        expected_answer = self.malrule.calculate_expected_answer(problem)
        malrule_solution = self.malrule.solve(problem)

        # Both should match (without unit)
        self.assertEqual(expected_answer, malrule_solution.answer)

    # Template 4: word_problem_money
    def test_word_problem_money_template(self):
        """Test word_problem_money template generates valid problems."""
        problem = self.generator.generate(seed=400, template='word_problem_money')

        self.assertEqual(problem.metadata['template'], 'word_problem_money')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)

        # Should mention money/bank context
        self.assertTrue(
            any(word in problem.text.lower() for word in ['$', 'dollar', 'bank', 'account', 'balance', 'withdraw', 'debt'])
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

        # Verify answers match metadata
        expected_correct = str(problem.metadata['correct_answer'])
        expected_malrule = str(problem.metadata['malrule_answer'])

        if correct_solution.answer == expected_correct and malrule_solution.answer == expected_malrule:
            print(f"\n  ✓ word_problem_money: Correct={correct_solution.answer}, Malrule={malrule_solution.answer}")
        else:
            print(f"\n  ✗ word_problem_money FAILED:")
            print(f"    Problem: {problem.text}")
            print(f"    Expected correct: {expected_correct}, Got: {correct_solution.answer}")
            print(f"    Expected malrule: {expected_malrule}, Got: {malrule_solution.answer}")
            print(f"\n    Correct steps:")
            for step in correct_solution.steps:
                print(f"      {step}")
            print(f"\n    Malrule steps:")
            for step in malrule_solution.steps:
                print(f"      {step}")

        self.assertEqual(correct_solution.answer, expected_correct)
        self.assertEqual(malrule_solution.answer, expected_malrule)

        # Edge case: malrule accidentally gets correct answer
        if malrule_solution.answer == correct_solution.answer:
            print(f"    ⚠ WARNING: Malrule accidentally produced correct answer!")
            print(f"    Malrule steps:")
            for step in malrule_solution.steps:
                print(f"      {step}")
            self.fail("Malrule produced same answer as correct algorithm - this is an edge case")

    def test_word_problem_money_calculate_expected_answer(self):
        """Test calculate_expected_answer for word_problem_money template."""
        problem = self.generator.generate(seed=402, template='word_problem_money')

        expected_answer = self.malrule.calculate_expected_answer(problem)
        malrule_solution = self.malrule.solve(problem)

        # Both should match (numeric part)
        self.assertEqual(expected_answer, malrule_solution.answer)

    # Template 5: multi_step
    def test_multi_step_template(self):
        """Test multi_step template generates valid problems."""
        problem = self.generator.generate(seed=500, template='multi_step')

        self.assertEqual(problem.metadata['template'], 'multi_step')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)

        # Should have 3 operands
        self.assertEqual(len(problem.operands), 3)

    def test_multi_step_malrule_vs_correct(self):
        """Test multi_step: malrule misapplies rule in multi-step operations."""
        problem = self.generator.generate(seed=501, template='multi_step')

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        self.assertFalse(malrule_solution.is_correct)
        self.assertTrue(correct_solution.is_correct)

        # Verify answers match metadata
        expected_correct = str(problem.metadata['correct_answer'])
        expected_malrule = str(problem.metadata['malrule_answer'])

        if correct_solution.answer == expected_correct and malrule_solution.answer == expected_malrule:
            print(f"\n  ✓ multi_step: Correct={correct_solution.answer}, Malrule={malrule_solution.answer}")
        else:
            print(f"\n  ✗ multi_step FAILED:")
            print(f"    Problem: {problem.text}")
            print(f"    Expected correct: {expected_correct}, Got: {correct_solution.answer}")
            print(f"    Expected malrule: {expected_malrule}, Got: {malrule_solution.answer}")
            print(f"\n    Correct steps:")
            for step in correct_solution.steps:
                print(f"      {step}")
            print(f"\n    Malrule steps:")
            for step in malrule_solution.steps:
                print(f"      {step}")

        self.assertEqual(correct_solution.answer, expected_correct)
        self.assertEqual(malrule_solution.answer, expected_malrule)

        # Edge case: malrule accidentally gets correct answer
        if malrule_solution.answer == correct_solution.answer:
            print(f"    ⚠ WARNING: Malrule accidentally produced correct answer!")
            print(f"    Malrule steps:")
            for step in malrule_solution.steps:
                print(f"      {step}")
            self.fail("Malrule produced same answer as correct algorithm - this is an edge case")

    def test_multi_step_calculate_expected_answer(self):
        """Test calculate_expected_answer for multi_step template."""
        problem = self.generator.generate(seed=502, template='multi_step')

        expected_answer = self.malrule.calculate_expected_answer(problem)
        malrule_solution = self.malrule.solve(problem)

        self.assertEqual(expected_answer, malrule_solution.answer)



class TestTwoNegativesAlwaysPositiveAutomated(unittest.TestCase):
    """Automated test suite runner."""

    def test_automated_suite(self):
        """Run the automated test suite."""
        problem_gen = NegativeSubtractionProblemGenerator(
            level=5,
            difficulty=DifficultyLevel.MEDIUM
        )
        malrule = TwoNegativesAlwaysPositiveMalrule()
        correct = NegativeSubtractionCorrectAlgorithm()

        test_suite = MalruleTest(malrule, correct, problem_gen)
        results = test_suite.run_all_tests(verbose=False)

        all_passed = all(r.passed for r in results)
        self.assertTrue(all_passed,
                       f"Automated tests failed: {[r.message for r in results if not r.passed]}")


def main():
    """Main entry point for standalone execution."""
    print("\n╔" + "═"*68 + "╗")
    print("║" + "  VERIFICATION TEST: Two Negatives Always Positive  ".center(70) + "║")
    print("╚" + "═"*68 + "╝\n")

    # Run unittest
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestTwoNegativesAlwaysPositiveTemplates))
    suite.addTests(loader.loadTestsFromTestCase(TestTwoNegativesAlwaysPositiveAutomated))

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
