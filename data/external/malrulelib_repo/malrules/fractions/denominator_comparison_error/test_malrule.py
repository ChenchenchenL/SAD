#!/usr/bin/env python3
"""
Comprehensive test suite for Denominator Comparison Error malrule.

This file combines:
1. Template validation tests (all templates)
2. Automated test suite functionality

Run from project root: python3 -m malrules.fractions.denominator_comparison_error.test_malrule
Or from this directory: python3 test_malrule.py
"""

import sys
import os
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.fractions.denominator_comparison_error import (
    FractionComparisonProblemGenerator,
    DenominatorComparisonErrorMalrule,
    FractionComparisonCorrectAlgorithm
)


class TestDenominatorComparisonErrorTemplates(unittest.TestCase):
    """Test all 5 templates for Denominator-Comparison-Error malrule."""

    def setUp(self):
        """Set up test fixtures."""
        self.generator = FractionComparisonProblemGenerator(
            level=5,
            difficulty=DifficultyLevel.MEDIUM
        )
        self.malrule = DenominatorComparisonErrorMalrule()
        self.correct_algo = FractionComparisonCorrectAlgorithm()

    # Template 1: basic_two_fractions
    def test_basic_two_fractions_template(self):
        """Test basic_two_fractions template generates valid problems."""
        problem = self.generator.generate(seed=100, template='basic_two_fractions')

        self.assertEqual(problem.metadata['template'], 'basic_two_fractions')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)
        self.assertIn('num1', problem.metadata)
        self.assertIn('num2', problem.metadata)
        self.assertIn('den1', problem.metadata)
        self.assertIn('den2', problem.metadata)

        # Verify answers are strings
        self.assertIsInstance(problem.metadata['correct_answer'], str)
        self.assertIsInstance(problem.metadata['malrule_answer'], str)

    def test_basic_two_fractions_malrule_vs_correct(self):
        """Test basic_two_fractions: malrule gives wrong answer, correct gives right answer."""
        problem = self.generator.generate(seed=101, template='basic_two_fractions')

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        self.assertFalse(malrule_solution.is_correct)
        self.assertTrue(correct_solution.is_correct)

        self.assertEqual(malrule_solution.answer, problem.metadata['malrule_answer'])
        self.assertEqual(correct_solution.answer, problem.metadata['correct_answer'])

        # Verify answers are strings
        self.assertIsInstance(malrule_solution.answer, str)
        self.assertIsInstance(correct_solution.answer, str)

    def test_basic_two_fractions_calculate_expected_answer(self):
        """Test calculate_expected_answer for basic_two_fractions template."""
        problem = self.generator.generate(seed=102, template='basic_two_fractions')

        expected_answer = self.malrule.calculate_expected_answer(problem)
        malrule_solution = self.malrule.solve(problem)

        self.assertEqual(expected_answer, malrule_solution.answer)
        self.assertEqual(expected_answer, problem.metadata['malrule_answer'])
        self.assertIsInstance(expected_answer, str)

    # Template 2: three_fractions_ordering
    def test_three_fractions_ordering_template(self):
        """Test three_fractions_ordering template generates valid problems."""
        problem = self.generator.generate(seed=200, template='three_fractions_ordering')

        self.assertEqual(problem.metadata['template'], 'three_fractions_ordering')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)
        self.assertEqual(problem.metadata['num_fractions'], 3)

        # Should have three fractions
        self.assertIn('num1', problem.metadata)
        self.assertIn('num2', problem.metadata)
        self.assertIn('num3', problem.metadata)

        # Verify answers are strings (comma-separated lists)
        self.assertIsInstance(problem.metadata['correct_answer'], str)
        self.assertIsInstance(problem.metadata['malrule_answer'], str)
        self.assertIn(',', problem.metadata['correct_answer'])
        self.assertIn(',', problem.metadata['malrule_answer'])

    def test_three_fractions_ordering_malrule_vs_correct(self):
        """Test three_fractions_ordering: malrule orders by denominator incorrectly."""
        problem = self.generator.generate(seed=201, template='three_fractions_ordering')

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        self.assertFalse(malrule_solution.is_correct)
        self.assertTrue(correct_solution.is_correct)

        self.assertEqual(malrule_solution.answer, problem.metadata['malrule_answer'])
        self.assertEqual(correct_solution.answer, problem.metadata['correct_answer'])

        # Verify answers are strings
        self.assertIsInstance(malrule_solution.answer, str)
        self.assertIsInstance(correct_solution.answer, str)

    def test_three_fractions_ordering_calculate_expected_answer(self):
        """Test calculate_expected_answer for three_fractions_ordering template."""
        problem = self.generator.generate(seed=202, template='three_fractions_ordering')

        expected_answer = self.malrule.calculate_expected_answer(problem)
        malrule_solution = self.malrule.solve(problem)

        self.assertEqual(expected_answer, malrule_solution.answer)
        self.assertEqual(expected_answer, problem.metadata['malrule_answer'])
        self.assertIsInstance(expected_answer, str)

    # Template 3: mixed_comparisons
    def test_mixed_comparisons_template(self):
        """Test mixed_comparisons template generates valid problems."""
        problem = self.generator.generate(seed=300, template='mixed_comparisons')

        self.assertEqual(problem.metadata['template'], 'mixed_comparisons')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)

        # Should have proper and improper fractions
        self.assertEqual(problem.metadata['fraction1_type'], 'proper')
        self.assertEqual(problem.metadata['fraction2_type'], 'improper')

        # Verify num1 < den1 (proper) and num2 >= den2 (improper)
        self.assertLess(problem.metadata['num1'], problem.metadata['den1'])
        self.assertGreaterEqual(problem.metadata['num2'], problem.metadata['den2'])

        # Verify answers are strings
        self.assertIsInstance(problem.metadata['correct_answer'], str)
        self.assertIsInstance(problem.metadata['malrule_answer'], str)

    def test_mixed_comparisons_malrule_vs_correct(self):
        """Test mixed_comparisons: malrule miscompares proper vs improper fractions."""
        problem = self.generator.generate(seed=301, template='mixed_comparisons')

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        self.assertFalse(malrule_solution.is_correct)
        self.assertTrue(correct_solution.is_correct)

        # Correct answer should be the improper fraction (fraction2)
        self.assertEqual(correct_solution.answer, problem.metadata['fraction2'])

        # Verify answers are strings
        self.assertIsInstance(malrule_solution.answer, str)
        self.assertIsInstance(correct_solution.answer, str)

    def test_mixed_comparisons_calculate_expected_answer(self):
        """Test calculate_expected_answer for mixed_comparisons template."""
        problem = self.generator.generate(seed=302, template='mixed_comparisons')

        expected_answer = self.malrule.calculate_expected_answer(problem)
        malrule_solution = self.malrule.solve(problem)

        self.assertEqual(expected_answer, malrule_solution.answer)
        self.assertEqual(expected_answer, problem.metadata['malrule_answer'])
        self.assertIsInstance(expected_answer, str)

    # Template 4: real_world_context
    def test_real_world_context_template(self):
        """Test real_world_context template generates valid problems."""
        problem = self.generator.generate(seed=400, template='real_world_context')

        self.assertEqual(problem.metadata['template'], 'real_world_context')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)
        self.assertIn('context', problem.metadata)

        # Should be unit fractions (numerators = 1)
        self.assertEqual(problem.metadata['num1'], 1)
        self.assertEqual(problem.metadata['num2'], 1)

        # Should have word problem context
        context_words = ['pizza', 'distance', 'time', 'measurement']
        self.assertIn(problem.metadata['context'], context_words)

        # Verify answers are strings
        self.assertIsInstance(problem.metadata['correct_answer'], str)
        self.assertIsInstance(problem.metadata['malrule_answer'], str)

    def test_real_world_context_malrule_vs_correct(self):
        """Test real_world_context: malrule misapplies rule in word problem."""
        problem = self.generator.generate(seed=401, template='real_world_context')

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        self.assertFalse(malrule_solution.is_correct)
        self.assertTrue(correct_solution.is_correct)

        self.assertEqual(malrule_solution.answer, problem.metadata['malrule_answer'])
        self.assertEqual(correct_solution.answer, problem.metadata['correct_answer'])

        # For unit fractions, malrule picks larger denominator, correct picks smaller
        self.assertEqual(malrule_solution.answer, problem.metadata['fraction1'])
        self.assertEqual(correct_solution.answer, problem.metadata['fraction2'])

        # Verify answers are strings
        self.assertIsInstance(malrule_solution.answer, str)
        self.assertIsInstance(correct_solution.answer, str)

    def test_real_world_context_calculate_expected_answer(self):
        """Test calculate_expected_answer for real_world_context template."""
        problem = self.generator.generate(seed=402, template='real_world_context')

        expected_answer = self.malrule.calculate_expected_answer(problem)
        malrule_solution = self.malrule.solve(problem)

        self.assertEqual(expected_answer, malrule_solution.answer)
        self.assertEqual(expected_answer, problem.metadata['malrule_answer'])
        self.assertIsInstance(expected_answer, str)

    # Template 5: benchmark_comparison
    def test_benchmark_comparison_template(self):
        """Test benchmark_comparison template generates valid problems."""
        problem = self.generator.generate(seed=500, template='benchmark_comparison')

        self.assertEqual(problem.metadata['template'], 'benchmark_comparison')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)
        self.assertIn('benchmark', problem.metadata)

        # Should compare to either 1/2 or 1
        self.assertIn(problem.metadata['benchmark'], ['half', 'one'])

        # Verify answers are strings
        self.assertIsInstance(problem.metadata['correct_answer'], str)
        self.assertIsInstance(problem.metadata['malrule_answer'], str)

    def test_benchmark_comparison_malrule_vs_correct(self):
        """Test benchmark_comparison: malrule miscompares to benchmark values."""
        problem = self.generator.generate(seed=501, template='benchmark_comparison')

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        self.assertFalse(malrule_solution.is_correct)
        self.assertTrue(correct_solution.is_correct)

        self.assertEqual(malrule_solution.answer, problem.metadata['malrule_answer'])
        self.assertEqual(correct_solution.answer, problem.metadata['correct_answer'])

        # Malrule should pick fraction1 (larger denominator)
        self.assertEqual(malrule_solution.answer, problem.metadata['fraction1'])

        # Correct should pick the benchmark (1/2 or 1)
        if problem.metadata['benchmark'] == 'half':
            self.assertEqual(correct_solution.answer, '1/2')
        else:
            self.assertEqual(correct_solution.answer, '1')

        # Verify answers are strings
        self.assertIsInstance(malrule_solution.answer, str)
        self.assertIsInstance(correct_solution.answer, str)

    def test_benchmark_comparison_calculate_expected_answer(self):
        """Test calculate_expected_answer for benchmark_comparison template."""
        problem = self.generator.generate(seed=502, template='benchmark_comparison')

        expected_answer = self.malrule.calculate_expected_answer(problem)
        malrule_solution = self.malrule.solve(problem)

        self.assertEqual(expected_answer, malrule_solution.answer)
        self.assertEqual(expected_answer, problem.metadata['malrule_answer'])
        self.assertIsInstance(expected_answer, str)

    # Additional tests for robustness
    def test_get_available_templates(self):
        """Test that get_available_templates returns correct list."""
        templates = self.generator.get_available_templates()

        self.assertEqual(len(templates), 7)
        self.assertIn('basic_two_fractions', templates)
        self.assertIn('three_fractions_ordering', templates)
        self.assertIn('mixed_comparisons', templates)
        self.assertIn('real_world_context', templates)
        self.assertIn('benchmark_comparison', templates)

    def test_generate_without_template(self):
        """Test that generate works without explicit template (random selection)."""
        problem = self.generator.generate(seed=999)

        self.assertIn('template', problem.metadata)
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)
        self.assertIn(problem.metadata['template'], self.generator.get_available_templates())

    def test_invalid_template_raises_error(self):
        """Test that invalid template raises ValueError."""
        with self.assertRaises(ValueError):
            self.generator.generate(seed=100, template='invalid_template')

    def test_malrule_and_correct_differ(self):
        """Test that malrule and correct answers differ for all templates."""
        for seed, template in enumerate(['basic_two_fractions', 'three_fractions_ordering',
                                         'mixed_comparisons', 'real_world_context',
                                         'benchmark_comparison'], start=700):
            problem = self.generator.generate(seed=seed, template=template)

            # Malrule and correct answers should be different
            self.assertNotEqual(
                problem.metadata['malrule_answer'],
                problem.metadata['correct_answer'],
                f"Template {template}: malrule and correct answers should differ"
            )



class TestDenominatorComparisonErrorAutomated(unittest.TestCase):
    """Automated test suite runner."""

    def test_automated_suite(self):
        """Run the automated test suite."""
        problem_gen = FractionComparisonProblemGenerator(
            level=5,
            difficulty=DifficultyLevel.MEDIUM
        )
        malrule = DenominatorComparisonErrorMalrule()
        correct = FractionComparisonCorrectAlgorithm()

        test_suite = MalruleTest(malrule, correct, problem_gen)
        results = test_suite.run_all_tests(verbose=False)

        all_passed = all(r.passed for r in results)
        self.assertTrue(all_passed,
                       f"Automated tests failed: {[r.message for r in results if not r.passed]}")


def main():
    """Main entry point for standalone execution."""
    print("\n╔" + "═"*68 + "╗")
    print("║" + "  VERIFICATION TEST: Denominator Comparison Error  ".center(70) + "║")
    print("╚" + "═"*68 + "╝\n")

    # Run unittest
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestDenominatorComparisonErrorTemplates))
    suite.addTests(loader.loadTestsFromTestCase(TestDenominatorComparisonErrorAutomated))

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
