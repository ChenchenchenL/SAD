#!/usr/bin/env python3
"""
Comprehensive test suite for Negative Times Negative Negative malrule.

This file combines:
1. Template validation tests (all templates)
2. Automated test suite functionality

Run from project root: python3 -m malrules.negative_numbers.negative_times_negative_negative.test_malrule
Or from this directory: python3 test_malrule.py
"""

import sys
import os
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.negative_numbers.negative_times_negative_negative import (
    NegativeTimesNegativeNegativeProblemGenerator,
    NegativeTimesNegativeNegativeMalrule,
    NegativeMultiplicationCorrectAlgorithm
)


class TestNegativeTimesNegativeNegativeTemplates(unittest.TestCase):
    """Test all 8 templates for Negative-Times-Negative-Negative malrule."""

    def setUp(self):
        """Set up test fixtures."""
        self.generator = NegativeTimesNegativeNegativeProblemGenerator(
            level=7,
            difficulty=DifficultyLevel.MEDIUM
        )
        self.malrule = NegativeTimesNegativeNegativeMalrule()
        self.correct_algo = NegativeMultiplicationCorrectAlgorithm()

    # Template 1: basic_multiplication
    def test_basic_multiplication_template(self):
        """Test basic_multiplication template generates valid problems."""
        problem = self.generator.generate(seed=100, template='basic_multiplication')

        self.assertEqual(problem.metadata['template'], 'basic_multiplication')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)
        self.assertIn('a', problem.metadata)
        self.assertIn('b', problem.metadata)

        # Both operands should be negative
        self.assertTrue(problem.metadata['a'] < 0)
        self.assertTrue(problem.metadata['b'] < 0)

    def test_basic_multiplication_malrule_vs_correct(self):
        """Test basic_multiplication: malrule gives wrong answer, correct gives right answer."""
        problem = self.generator.generate(seed=101, template='basic_multiplication')

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        self.assertFalse(malrule_solution.is_correct)
        self.assertTrue(correct_solution.is_correct)

        self.assertEqual(malrule_solution.answer, problem.metadata['malrule_answer'])
        self.assertEqual(correct_solution.answer, problem.metadata['correct_answer'])

    def test_basic_multiplication_calculate_expected_answer(self):
        """Test calculate_expected_answer for basic_multiplication template."""
        problem = self.generator.generate(seed=102, template='basic_multiplication')

        expected_answer = self.malrule.calculate_expected_answer(problem)
        malrule_solution = self.malrule.solve(problem)

        self.assertEqual(expected_answer, malrule_solution.answer)
        self.assertEqual(expected_answer, problem.metadata['malrule_answer'])

    # Template 2: word_problem_temperature
    def test_word_problem_temperature_template(self):
        """Test word_problem_temperature template generates valid problems."""
        problem = self.generator.generate(seed=200, template='word_problem_temperature')

        self.assertEqual(problem.metadata['template'], 'word_problem_temperature')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)

        # Should mention temperature or related words
        text_lower = problem.text.lower()
        self.assertTrue(
            any(word in text_lower for word in ['temperature', 'drop', 'degree', 'revers', 'decrease'])
        )

        # Answers should have degree symbol
        self.assertTrue('°' in problem.metadata['correct_answer'])
        self.assertTrue('°' in problem.metadata['malrule_answer'])

    def test_word_problem_temperature_malrule_vs_correct(self):
        """Test word_problem_temperature: malrule incorrectly makes result negative."""
        problem = self.generator.generate(seed=201, template='word_problem_temperature')

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        self.assertFalse(malrule_solution.is_correct)
        self.assertTrue(correct_solution.is_correct)

        # Malrule makes it negative, correct makes it positive
        self.assertEqual(malrule_solution.answer, problem.metadata['malrule_answer'])
        self.assertEqual(correct_solution.answer, problem.metadata['correct_answer'])

    def test_word_problem_temperature_calculate_expected_answer(self):
        """Test calculate_expected_answer for word_problem_temperature template."""
        problem = self.generator.generate(seed=202, template='word_problem_temperature')

        expected_answer = problem.metadata['malrule_answer']
        malrule_solution = self.malrule.solve(problem)

        # Both should match
        self.assertEqual(expected_answer, malrule_solution.answer)

    # Template 3: word_problem_debt
    def test_word_problem_debt_template(self):
        """Test word_problem_debt template generates valid problems."""
        problem = self.generator.generate(seed=300, template='word_problem_debt')

        self.assertEqual(problem.metadata['template'], 'word_problem_debt')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)

        # Should mention money/debt context
        text_lower = problem.text.lower()
        self.assertTrue(
            any(word in text_lower for word in ['$', 'debt', 'owe', 'remov', 'forgiv', 'eliminat', 'balance'])
        )

        # Answers should have $ symbol
        self.assertTrue(problem.metadata['correct_answer'].startswith('+$'))
        self.assertTrue(problem.metadata['malrule_answer'].startswith('$'))

    def test_word_problem_debt_malrule_vs_correct(self):
        """Test word_problem_debt: malrule misapplies rule in debt context."""
        problem = self.generator.generate(seed=301, template='word_problem_debt')

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        self.assertFalse(malrule_solution.is_correct)
        self.assertTrue(correct_solution.is_correct)

        self.assertEqual(malrule_solution.answer, problem.metadata['malrule_answer'])
        self.assertEqual(correct_solution.answer, problem.metadata['correct_answer'])

    def test_word_problem_debt_calculate_expected_answer(self):
        """Test calculate_expected_answer for word_problem_debt template."""
        problem = self.generator.generate(seed=302, template='word_problem_debt')

        expected_answer = problem.metadata['malrule_answer']
        malrule_solution = self.malrule.solve(problem)

        # Both should match
        self.assertEqual(expected_answer, malrule_solution.answer)

    # Template 4: equation_solving
    def test_equation_solving_template(self):
        """Test equation_solving template generates valid problems."""
        problem = self.generator.generate(seed=400, template='equation_solving')

        self.assertEqual(problem.metadata['template'], 'equation_solving')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)

        # Should have equation format
        self.assertTrue('x' in problem.text.lower())
        self.assertTrue('=' in problem.text)

        # x should be negative (correct answer)
        self.assertTrue(int(problem.metadata['correct_answer']) < 0)
        # malrule answer should be positive
        self.assertTrue(int(problem.metadata['malrule_answer']) > 0)

    def test_equation_solving_malrule_vs_correct(self):
        """Test equation_solving: malrule gives wrong sign for x."""
        problem = self.generator.generate(seed=401, template='equation_solving')

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        self.assertFalse(malrule_solution.is_correct)
        self.assertTrue(correct_solution.is_correct)

        self.assertEqual(malrule_solution.answer, problem.metadata['malrule_answer'])
        self.assertEqual(correct_solution.answer, problem.metadata['correct_answer'])

    def test_equation_solving_calculate_expected_answer(self):
        """Test calculate_expected_answer for equation_solving template."""
        problem = self.generator.generate(seed=402, template='equation_solving')

        expected_answer = problem.metadata['malrule_answer']
        malrule_solution = self.malrule.solve(problem)

        # Both should match
        self.assertEqual(expected_answer, malrule_solution.answer)

    # Template 5: pattern_completion
    def test_pattern_completion_template(self):
        """Test pattern_completion template generates valid problems."""
        problem = self.generator.generate(seed=500, template='pattern_completion')

        self.assertEqual(problem.metadata['template'], 'pattern_completion')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)
        self.assertIn('pattern', problem.metadata)

        # Should have pattern in text
        self.assertTrue('pattern' in problem.text.lower() or '×' in problem.text)

        # Correct answer should be positive
        self.assertTrue(int(problem.metadata['correct_answer']) > 0)
        # Malrule answer should be negative
        self.assertTrue(int(problem.metadata['malrule_answer']) < 0)

    def test_pattern_completion_malrule_vs_correct(self):
        """Test pattern_completion: malrule misunderstands the pattern."""
        problem = self.generator.generate(seed=501, template='pattern_completion')

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        self.assertFalse(malrule_solution.is_correct)
        self.assertTrue(correct_solution.is_correct)

        self.assertEqual(malrule_solution.answer, problem.metadata['malrule_answer'])
        self.assertEqual(correct_solution.answer, problem.metadata['correct_answer'])

    def test_pattern_completion_calculate_expected_answer(self):
        """Test calculate_expected_answer for pattern_completion template."""
        problem = self.generator.generate(seed=502, template='pattern_completion')

        expected_answer = self.malrule.calculate_expected_answer(problem)
        malrule_solution = self.malrule.solve(problem)

        # Both should match
        self.assertEqual(expected_answer, malrule_solution.answer)

    # Template 6: word_problem_multi_step
    def test_word_problem_multi_step_template(self):
        """Test word_problem_multi_step template generates valid problems."""
        problem = self.generator.generate(seed=600, template='word_problem_multi_step')

        self.assertEqual(problem.metadata['template'], 'word_problem_multi_step')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)
        self.assertIn('problem_type', problem.metadata)
        self.assertEqual(problem.metadata['problem_type'], 'multi_step_multiplication')

        # Should have three operands
        self.assertIn('a', problem.metadata)
        self.assertIn('b', problem.metadata)
        self.assertIn('c', problem.metadata)

    def test_word_problem_multi_step_malrule_vs_correct(self):
        """Test word_problem_multi_step: malrule gives wrong answer."""
        problem = self.generator.generate(seed=601, template='word_problem_multi_step')

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        self.assertFalse(malrule_solution.is_correct)
        self.assertTrue(correct_solution.is_correct)

    # Template 7: word_problem_mixed_operations
    def test_word_problem_mixed_operations_template(self):
        """Test word_problem_mixed_operations template generates valid problems."""
        problem = self.generator.generate(seed=700, template='word_problem_mixed_operations')

        self.assertEqual(problem.metadata['template'], 'word_problem_mixed_operations')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)
        self.assertIn('problem_type', problem.metadata)
        self.assertEqual(problem.metadata['problem_type'], 'mixed_operations')

        # Should have three operands
        self.assertIn('a', problem.metadata)
        self.assertIn('b', problem.metadata)
        self.assertIn('c', problem.metadata)

    def test_word_problem_mixed_operations_malrule_vs_correct(self):
        """Test word_problem_mixed_operations: malrule gives wrong answer."""
        problem = self.generator.generate(seed=701, template='word_problem_mixed_operations')

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        self.assertFalse(malrule_solution.is_correct)
        self.assertTrue(correct_solution.is_correct)

    # Template 8: word_problem_distributive
    def test_word_problem_distributive_template(self):
        """Test word_problem_distributive template generates valid problems."""
        problem = self.generator.generate(seed=800, template='word_problem_distributive')

        self.assertEqual(problem.metadata['template'], 'word_problem_distributive')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)
        self.assertIn('problem_type', problem.metadata)
        self.assertEqual(problem.metadata['problem_type'], 'distributive_property')

        # Should have distributive structure
        self.assertIn('a', problem.metadata)
        self.assertIn('b', problem.metadata)
        self.assertIn('c', problem.metadata)
        self.assertIn('pattern', problem.metadata)

    def test_word_problem_distributive_malrule_vs_correct(self):
        """Test word_problem_distributive: malrule gives wrong answer."""
        problem = self.generator.generate(seed=801, template='word_problem_distributive')

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        self.assertFalse(malrule_solution.is_correct)
        self.assertTrue(correct_solution.is_correct)

    # Additional tests for robustness
    def test_get_available_templates(self):
        """Test that get_available_templates returns exactly 8 templates."""
        templates = self.generator.get_available_templates()

        self.assertEqual(len(templates), 8)
        self.assertIn('basic_multiplication', templates)
        self.assertIn('word_problem_temperature', templates)
        self.assertIn('word_problem_debt', templates)
        self.assertIn('equation_solving', templates)
        self.assertIn('pattern_completion', templates)
        self.assertIn('word_problem_multi_step', templates)
        self.assertIn('word_problem_mixed_operations', templates)
        self.assertIn('word_problem_distributive', templates)

    def test_random_template_selection(self):
        """Test that random template selection works."""
        problem = self.generator.generate(seed=999)

        # Should have a template
        self.assertIn('template', problem.metadata)
        self.assertIn(problem.metadata['template'], self.generator.get_available_templates())

    def test_all_templates_store_string_answers(self):
        """Test that all templates store correct_answer and malrule_answer as strings."""
        for i, template in enumerate(self.generator.get_available_templates()):
            with self.subTest(template=template):
                problem = self.generator.generate(seed=600+i, template=template)

                # Check that answers are stored
                self.assertIn('correct_answer', problem.metadata)
                self.assertIn('malrule_answer', problem.metadata)

                # Check that they are strings
                self.assertIsInstance(problem.metadata['correct_answer'], str)
                self.assertIsInstance(problem.metadata['malrule_answer'], str)



class TestNegativeTimesNegativeNegativeAutomated(unittest.TestCase):
    """Automated test suite runner."""

    def test_automated_suite(self):
        """Run the automated test suite."""
        problem_gen = NegativeTimesNegativeNegativeProblemGenerator(
            level=5,
            difficulty=DifficultyLevel.MEDIUM
        )
        malrule = NegativeTimesNegativeNegativeMalrule()
        correct = NegativeMultiplicationCorrectAlgorithm()

        test_suite = MalruleTest(malrule, correct, problem_gen)
        results = test_suite.run_all_tests(verbose=True)

        all_passed = all(r.passed for r in results)
        self.assertTrue(all_passed,
                       f"Automated tests failed: {[r.message for r in results if not r.passed]}")


def main():
    """Main entry point for standalone execution."""
    print("\n╔" + "═"*68 + "╗")
    print("║" + "  VERIFICATION TEST: Negative Times Negative Negative  ".center(70) + "║")
    print("╚" + "═"*68 + "╝\n")

    # Run unittest
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestNegativeTimesNegativeNegativeTemplates))
    suite.addTests(loader.loadTestsFromTestCase(TestNegativeTimesNegativeNegativeAutomated))

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
