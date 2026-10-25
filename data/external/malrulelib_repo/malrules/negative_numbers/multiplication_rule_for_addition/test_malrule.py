#!/usr/bin/env python3
"""
Comprehensive test suite for Multiplication Rule For Addition malrule.

This file combines:
1. Template validation tests (all templates)
2. Automated test suite functionality

Run from project root: python3 -m malrules.negative_numbers.multiplication_rule_for_addition.test_malrule
Or from this directory: python3 test_malrule.py
"""

import sys
import os
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.negative_numbers.multiplication_rule_for_addition import (
    NegativeAdditionProblemGenerator,
    MultiplicationRuleForAdditionMalrule,
    NegativeAdditionCorrectAlgorithm
)


class TestMultiplicationRuleForAdditionTemplates(unittest.TestCase):
    """Test all 5 templates for Multiplication-Rule-For-Addition malrule."""

    def setUp(self):
        """Set up test fixtures."""
        self.generator = NegativeAdditionProblemGenerator(
            level=7,
            difficulty=DifficultyLevel.MEDIUM
        )
        self.malrule = MultiplicationRuleForAdditionMalrule()
        self.correct_algo = NegativeAdditionCorrectAlgorithm()

    # Template 1: two_negatives_addition
    def test_two_negatives_addition_template(self):
        """Test two_negatives_addition template generates valid problems."""
        problem = self.generator.generate(seed=100, template='two_negatives_addition')

        self.assertEqual(problem.metadata['template'], 'two_negatives_addition')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)
        self.assertIn('num1', problem.metadata)
        self.assertIn('num2', problem.metadata)

        # Should have two negative operands
        self.assertTrue(problem.operands[0] < 0)
        self.assertTrue(problem.operands[1] < 0)

        print(f"\n  ✓ Template 'two_negatives_addition' generates valid problems")

    def test_two_negatives_addition_malrule_vs_correct(self):
        """Test two_negatives_addition: malrule gives wrong answer, correct gives right answer."""
        problem = self.generator.generate(seed=101, template='two_negatives_addition')

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        try:
            self.assertFalse(malrule_solution.is_correct)
            self.assertTrue(correct_solution.is_correct)

            self.assertEqual(malrule_solution.answer, str(problem.metadata['malrule_answer']))
            self.assertEqual(correct_solution.answer, str(problem.metadata['correct_answer']))

            # Malrule makes it positive, correct keeps it negative
            self.assertTrue(int(malrule_solution.answer) > 0)
            self.assertTrue(int(correct_solution.answer) < 0)

            # Check for edge case: malrule and correct produce same answer
            if malrule_solution.answer == correct_solution.answer:
                print(f"\n  ⚠ EDGE CASE DETECTED for two_negatives_addition:")
                print(f"  Problem: {problem.text}")
                print(f"  Malrule and correct produced same answer: {malrule_solution.answer}")
                print(f"  Malrule steps:\n" + "\n".join(f"    {s}" for s in malrule_solution.steps))
                print(f"  Correct steps:\n" + "\n".join(f"    {s}" for s in correct_solution.steps))
                self.fail("Edge case: malrule produced same answer as correct algorithm")

            print(f"  ✓ Correct answer: {correct_solution.answer}, Malrule answer: {malrule_solution.answer}")

        except AssertionError as e:
            print(f"\n  ✗ TEST FAILED for two_negatives_addition:")
            print(f"  Problem: {problem.text}")
            print(f"  Expected correct answer: {problem.metadata['correct_answer']}")
            print(f"  Expected malrule answer: {problem.metadata['malrule_answer']}")
            print(f"  Actual correct answer: {correct_solution.answer}")
            print(f"  Actual malrule answer: {malrule_solution.answer}")
            print(f"  Correct steps:\n" + "\n".join(f"    {s}" for s in correct_solution.steps))
            print(f"  Malrule steps:\n" + "\n".join(f"    {s}" for s in malrule_solution.steps))
            raise

    def test_two_negatives_addition_calculate_expected_answer(self):
        """Test calculate_expected_answer for two_negatives_addition template."""
        problem = self.generator.generate(seed=102, template='two_negatives_addition')

        expected_answer = self.malrule.calculate_expected_answer(problem)
        malrule_solution = self.malrule.solve(problem)

        try:
            self.assertEqual(expected_answer, malrule_solution.answer)
            self.assertEqual(expected_answer, str(problem.metadata['malrule_answer']))
            print(f"  ✓ calculate_expected_answer works correctly: {expected_answer}")
        except AssertionError as e:
            print(f"\n  ✗ TEST FAILED for calculate_expected_answer:")
            print(f"  Expected: {expected_answer}")
            print(f"  Actual: {malrule_solution.answer}")
            print(f"  Metadata malrule_answer: {problem.metadata['malrule_answer']}")
            raise

    # Template 2: positive_minus_negative
    def test_positive_minus_negative_template(self):
        """Test positive_minus_negative template generates valid problems."""
        problem = self.generator.generate(seed=200, template='positive_minus_negative')

        self.assertEqual(problem.metadata['template'], 'positive_minus_negative')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)
        self.assertIn('num1', problem.metadata)
        self.assertIn('num2', problem.metadata)

        # Should have positive first operand and negative second
        self.assertTrue(problem.metadata['num1'] > 0)
        self.assertTrue(problem.metadata['num2'] < 0)

        print(f"\n  ✓ Template 'positive_minus_negative' generates valid problems")

    def test_positive_minus_negative_malrule_vs_correct(self):
        """Test positive_minus_negative: malrule misapplies rule."""
        problem = self.generator.generate(seed=201, template='positive_minus_negative')

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        try:
            self.assertFalse(malrule_solution.is_correct)
            self.assertTrue(correct_solution.is_correct)

            self.assertEqual(malrule_solution.answer, str(problem.metadata['malrule_answer']))
            self.assertEqual(correct_solution.answer, str(problem.metadata['correct_answer']))

            # Check for edge case: malrule and correct produce same answer
            if malrule_solution.answer == correct_solution.answer:
                print(f"\n  ⚠ EDGE CASE DETECTED for positive_minus_negative:")
                print(f"  Problem: {problem.text}")
                print(f"  Malrule and correct produced same answer: {malrule_solution.answer}")
                print(f"  Malrule steps:\n" + "\n".join(f"    {s}" for s in malrule_solution.steps))
                print(f"  Correct steps:\n" + "\n".join(f"    {s}" for s in correct_solution.steps))
                self.fail("Edge case: malrule produced same answer as correct algorithm")

            print(f"  ✓ Correct answer: {correct_solution.answer}, Malrule answer: {malrule_solution.answer}")

        except AssertionError as e:
            print(f"\n  ✗ TEST FAILED for positive_minus_negative:")
            print(f"  Problem: {problem.text}")
            print(f"  Expected correct answer: {problem.metadata['correct_answer']}")
            print(f"  Expected malrule answer: {problem.metadata['malrule_answer']}")
            print(f"  Actual correct answer: {correct_solution.answer}")
            print(f"  Actual malrule answer: {malrule_solution.answer}")
            print(f"  Correct steps:\n" + "\n".join(f"    {s}" for s in correct_solution.steps))
            print(f"  Malrule steps:\n" + "\n".join(f"    {s}" for s in malrule_solution.steps))
            raise

    def test_positive_minus_negative_calculate_expected_answer(self):
        """Test calculate_expected_answer for positive_minus_negative template."""
        problem = self.generator.generate(seed=202, template='positive_minus_negative')

        expected_answer = self.malrule.calculate_expected_answer(problem)
        malrule_solution = self.malrule.solve(problem)

        try:
            self.assertEqual(expected_answer, malrule_solution.answer)
            print(f"  ✓ calculate_expected_answer works correctly: {expected_answer}")
        except AssertionError as e:
            print(f"\n  ✗ TEST FAILED for calculate_expected_answer:")
            print(f"  Expected: {expected_answer}")
            print(f"  Actual: {malrule_solution.answer}")
            raise

    # Template 3: word_problem_temperature
    def test_word_problem_temperature_template(self):
        """Test word_problem_temperature template generates valid problems."""
        problem = self.generator.generate(seed=300, template='word_problem_temperature')

        self.assertEqual(problem.metadata['template'], 'word_problem_temperature')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)

        # Should mention temperature context
        self.assertTrue(
            any(word in problem.text.lower() for word in ['temperature', 'temp', '°c', '°f', 'drop', 'decrease', 'fall', 'freezer'])
        )

        # Answers should have degree symbol
        self.assertTrue('°' in problem.metadata['correct_answer'])
        self.assertTrue('°' in problem.metadata['malrule_answer'])

        print(f"\n  ✓ Template 'word_problem_temperature' generates valid problems")

    def test_word_problem_temperature_malrule_vs_correct(self):
        """Test word_problem_temperature: malrule misapplies rule in temperature context."""
        problem = self.generator.generate(seed=301, template='word_problem_temperature')

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        try:
            self.assertFalse(malrule_solution.is_correct)
            self.assertTrue(correct_solution.is_correct)

            # Both should have degree symbols
            self.assertTrue('°' in malrule_solution.answer)
            self.assertTrue('°' in correct_solution.answer)

            # Check for edge case: malrule and correct produce same answer
            if malrule_solution.answer == correct_solution.answer:
                print(f"\n  ⚠ EDGE CASE DETECTED for word_problem_temperature:")
                print(f"  Problem: {problem.text}")
                print(f"  Malrule and correct produced same answer: {malrule_solution.answer}")
                print(f"  Malrule steps:\n" + "\n".join(f"    {s}" for s in malrule_solution.steps))
                print(f"  Correct steps:\n" + "\n".join(f"    {s}" for s in correct_solution.steps))
                self.fail("Edge case: malrule produced same answer as correct algorithm")

            print(f"  ✓ Correct answer: {correct_solution.answer}, Malrule answer: {malrule_solution.answer}")

        except AssertionError as e:
            print(f"\n  ✗ TEST FAILED for word_problem_temperature:")
            print(f"  Problem: {problem.text}")
            print(f"  Expected correct answer: {problem.metadata['correct_answer']}")
            print(f"  Expected malrule answer: {problem.metadata['malrule_answer']}")
            print(f"  Actual correct answer: {correct_solution.answer}")
            print(f"  Actual malrule answer: {malrule_solution.answer}")
            print(f"  Correct steps:\n" + "\n".join(f"    {s}" for s in correct_solution.steps))
            print(f"  Malrule steps:\n" + "\n".join(f"    {s}" for s in malrule_solution.steps))
            raise

    def test_word_problem_temperature_calculate_expected_answer(self):
        """Test calculate_expected_answer for word_problem_temperature template."""
        problem = self.generator.generate(seed=302, template='word_problem_temperature')

        expected_answer = self.malrule.calculate_expected_answer(problem)
        malrule_solution = self.malrule.solve(problem)

        try:
            # Both should match
            self.assertEqual(expected_answer, malrule_solution.answer)
            print(f"  ✓ calculate_expected_answer works correctly: {expected_answer}")
        except AssertionError as e:
            print(f"\n  ✗ TEST FAILED for calculate_expected_answer:")
            print(f"  Expected: {expected_answer}")
            print(f"  Actual: {malrule_solution.answer}")
            raise

    # Template 4: word_problem_elevation
    def test_word_problem_elevation_template(self):
        """Test word_problem_elevation template generates valid problems."""
        problem = self.generator.generate(seed=400, template='word_problem_elevation')

        self.assertEqual(problem.metadata['template'], 'word_problem_elevation')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)

        # Should mention elevation/depth context
        self.assertTrue(
            any(word in problem.text.lower() for word in ['submarine', 'diver', 'elevation', 'depth', 'sea level', 'descend'])
        )

        # Answers should have meter unit
        self.assertTrue(problem.metadata['correct_answer'].endswith('m'))
        self.assertTrue(problem.metadata['malrule_answer'].endswith('m'))

        print(f"\n  ✓ Template 'word_problem_elevation' generates valid problems")

    def test_word_problem_elevation_malrule_vs_correct(self):
        """Test word_problem_elevation: malrule misapplies rule in elevation context."""
        problem = self.generator.generate(seed=401, template='word_problem_elevation')

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        try:
            self.assertFalse(malrule_solution.is_correct)
            self.assertTrue(correct_solution.is_correct)

            # Both should have meter units
            self.assertTrue('m' in malrule_solution.answer)
            self.assertTrue('m' in correct_solution.answer)

            # Check for edge case: malrule and correct produce same answer
            if malrule_solution.answer == correct_solution.answer:
                print(f"\n  ⚠ EDGE CASE DETECTED for word_problem_elevation:")
                print(f"  Problem: {problem.text}")
                print(f"  Malrule and correct produced same answer: {malrule_solution.answer}")
                print(f"  Malrule steps:\n" + "\n".join(f"    {s}" for s in malrule_solution.steps))
                print(f"  Correct steps:\n" + "\n".join(f"    {s}" for s in correct_solution.steps))
                self.fail("Edge case: malrule produced same answer as correct algorithm")

            print(f"  ✓ Correct answer: {correct_solution.answer}, Malrule answer: {malrule_solution.answer}")

        except AssertionError as e:
            print(f"\n  ✗ TEST FAILED for word_problem_elevation:")
            print(f"  Problem: {problem.text}")
            print(f"  Expected correct answer: {problem.metadata['correct_answer']}")
            print(f"  Expected malrule answer: {problem.metadata['malrule_answer']}")
            print(f"  Actual correct answer: {correct_solution.answer}")
            print(f"  Actual malrule answer: {malrule_solution.answer}")
            print(f"  Correct steps:\n" + "\n".join(f"    {s}" for s in correct_solution.steps))
            print(f"  Malrule steps:\n" + "\n".join(f"    {s}" for s in malrule_solution.steps))
            raise

    def test_word_problem_elevation_calculate_expected_answer(self):
        """Test calculate_expected_answer for word_problem_elevation template."""
        problem = self.generator.generate(seed=402, template='word_problem_elevation')

        expected_answer = self.malrule.calculate_expected_answer(problem)
        malrule_solution = self.malrule.solve(problem)

        try:
            # Both should match
            self.assertEqual(expected_answer, malrule_solution.answer)
            print(f"  ✓ calculate_expected_answer works correctly: {expected_answer}")
        except AssertionError as e:
            print(f"\n  ✗ TEST FAILED for calculate_expected_answer:")
            print(f"  Expected: {expected_answer}")
            print(f"  Actual: {malrule_solution.answer}")
            raise

    # Template 5: sequential_operations
    def test_sequential_operations_template(self):
        """Test sequential_operations template generates valid problems."""
        problem = self.generator.generate(seed=500, template='sequential_operations')

        self.assertEqual(problem.metadata['template'], 'sequential_operations')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)

        # Should have 3 operands
        self.assertEqual(len(problem.operands), 3)

        # First two should be negative
        self.assertTrue(problem.operands[0] < 0)
        self.assertTrue(problem.operands[1] < 0)

        print(f"\n  ✓ Template 'sequential_operations' generates valid problems")

    def test_sequential_operations_malrule_vs_correct(self):
        """Test sequential_operations: malrule misapplies rule in multi-step operations."""
        problem = self.generator.generate(seed=501, template='sequential_operations')

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        try:
            self.assertFalse(malrule_solution.is_correct)
            self.assertTrue(correct_solution.is_correct)

            self.assertEqual(malrule_solution.answer, str(problem.metadata['malrule_answer']))
            self.assertEqual(correct_solution.answer, str(problem.metadata['correct_answer']))

            # Check for edge case: malrule and correct produce same answer
            if malrule_solution.answer == correct_solution.answer:
                print(f"\n  ⚠ EDGE CASE DETECTED for sequential_operations:")
                print(f"  Problem: {problem.text}")
                print(f"  Malrule and correct produced same answer: {malrule_solution.answer}")
                print(f"  Malrule steps:\n" + "\n".join(f"    {s}" for s in malrule_solution.steps))
                print(f"  Correct steps:\n" + "\n".join(f"    {s}" for s in correct_solution.steps))
                self.fail("Edge case: malrule produced same answer as correct algorithm")

            print(f"  ✓ Correct answer: {correct_solution.answer}, Malrule answer: {malrule_solution.answer}")

        except AssertionError as e:
            print(f"\n  ✗ TEST FAILED for sequential_operations:")
            print(f"  Problem: {problem.text}")
            print(f"  Expected correct answer: {problem.metadata['correct_answer']}")
            print(f"  Expected malrule answer: {problem.metadata['malrule_answer']}")
            print(f"  Actual correct answer: {correct_solution.answer}")
            print(f"  Actual malrule answer: {malrule_solution.answer}")
            print(f"  Correct steps:\n" + "\n".join(f"    {s}" for s in correct_solution.steps))
            print(f"  Malrule steps:\n" + "\n".join(f"    {s}" for s in malrule_solution.steps))
            raise

    def test_sequential_operations_calculate_expected_answer(self):
        """Test calculate_expected_answer for sequential_operations template."""
        problem = self.generator.generate(seed=502, template='sequential_operations')

        expected_answer = self.malrule.calculate_expected_answer(problem)
        malrule_solution = self.malrule.solve(problem)

        try:
            self.assertEqual(expected_answer, malrule_solution.answer)
            print(f"  ✓ calculate_expected_answer works correctly: {expected_answer}")
        except AssertionError as e:
            print(f"\n  ✗ TEST FAILED for calculate_expected_answer:")
            print(f"  Expected: {expected_answer}")
            print(f"  Actual: {malrule_solution.answer}")
            raise



class TestMultiplicationRuleForAdditionAutomated(unittest.TestCase):
    """Automated test suite runner."""

    def test_automated_suite(self):
        """Run the automated test suite."""
        problem_gen = NegativeAdditionProblemGenerator(
            level=5,
            difficulty=DifficultyLevel.MEDIUM
        )
        malrule = MultiplicationRuleForAdditionMalrule()
        correct = NegativeAdditionCorrectAlgorithm()

        test_suite = MalruleTest(malrule, correct, problem_gen)
        results = test_suite.run_all_tests(verbose=False)

        all_passed = all(r.passed for r in results)
        self.assertTrue(all_passed,
                       f"Automated tests failed: {[r.message for r in results if not r.passed]}")


def main():
    """Main entry point for standalone execution."""
    print("\n╔" + "═"*68 + "╗")
    print("║" + "  VERIFICATION TEST: Multiplication Rule For Addition  ".center(70) + "║")
    print("╚" + "═"*68 + "╝\n")

    # Run unittest
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestMultiplicationRuleForAdditionTemplates))
    suite.addTests(loader.loadTestsFromTestCase(TestMultiplicationRuleForAdditionAutomated))

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
