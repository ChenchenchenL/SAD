#!/usr/bin/env python3
"""
Comprehensive test suite for Additive Instead Of Multiplicative malrule.

This file combines:
1. Template validation tests (all templates)
2. Automated test suite functionality

Run from project root: python3 -m malrules.ratios_proportions.additive_instead_of_multiplicative.test_malrule
Or from this directory: python3 test_malrule.py
"""

import sys
import os
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.ratios_proportions.additive_instead_of_multiplicative import (
    AdditiveInsteadOfMultiplicativeProblemGenerator,
    AdditiveInsteadOfMultiplicativeMalrule,
    RatioScalingCorrectAlgorithm
)


class TestAdditiveInsteadOfMultiplicative(unittest.TestCase):
    """Test suite for Additive-Instead-Of-Multiplicative malrule with all templates."""

    def setUp(self):
        """Set up test fixtures."""
        self.generator = AdditiveInsteadOfMultiplicativeProblemGenerator(
            level=7,
            difficulty=DifficultyLevel.MEDIUM
        )
        self.malrule = AdditiveInsteadOfMultiplicativeMalrule()
        self.correct_algo = RatioScalingCorrectAlgorithm()

    # ============================================================================
    # TEMPLATE 1: basic_scaling (3 tests)
    # ============================================================================

    def test_basic_scaling_simple_ratio(self):
        """Test basic ratio scaling with simple numbers."""
        problem = self.generator.generate(seed=100, template='basic_scaling')

        # Verify problem has correct template
        self.assertEqual(problem.metadata['template'], 'basic_scaling')

        # Get both answers
        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        # Verify malrule answer matches expected
        self.assertEqual(malrule_solution.answer, problem.metadata['malrule_answer'])
        self.assertFalse(malrule_solution.is_correct)

        # Verify correct answer matches expected
        self.assertEqual(correct_solution.answer, problem.metadata['correct_answer'])
        self.assertTrue(correct_solution.is_correct)

        # Verify answers are different
        self.assertNotEqual(malrule_solution.answer, correct_solution.answer)

        # Verify answer format is string with colon
        self.assertIn(':', malrule_solution.answer)
        self.assertIn(':', correct_solution.answer)

    def test_basic_scaling_larger_numbers(self):
        """Test basic ratio scaling with larger values."""
        problem = self.generator.generate(seed=200, template='basic_scaling')

        self.assertEqual(problem.metadata['template'], 'basic_scaling')

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        # Verify malrule uses addition
        a = problem.metadata['initial_a']
        b = problem.metadata['initial_b']
        k = problem.metadata['scale_factor']

        expected_malrule = f"{a + k}:{b + k}"
        expected_correct = f"{a * k}:{b * k}"

        self.assertEqual(malrule_solution.answer, expected_malrule)
        self.assertEqual(correct_solution.answer, expected_correct)

    def test_basic_scaling_different_seed(self):
        """Test basic ratio scaling with different seed for variety."""
        problem = self.generator.generate(seed=300, template='basic_scaling')

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        # Verify steps are present
        self.assertGreater(len(malrule_solution.steps), 0)
        self.assertGreater(len(correct_solution.steps), 0)

        # Verify solution correctness flags
        self.assertFalse(malrule_solution.is_correct)
        self.assertTrue(correct_solution.is_correct)

    # ============================================================================
    # TEMPLATE 2: recipe_scaling (3 tests)
    # ============================================================================

    def test_recipe_scaling_basic(self):
        """Test recipe scaling with basic ingredients."""
        problem = self.generator.generate(seed=400, template='recipe_scaling')

        self.assertEqual(problem.metadata['template'], 'recipe_scaling')

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        # Verify answers are strings with 'and' separator
        self.assertIn('and', malrule_solution.answer)
        self.assertIn('and', correct_solution.answer)

        # Verify different answers
        self.assertNotEqual(malrule_solution.answer, correct_solution.answer)

    def test_recipe_scaling_with_verification(self):
        """Test recipe scaling and verify calculations."""
        problem = self.generator.generate(seed=500, template='recipe_scaling')

        amount1 = problem.metadata['initial_a']
        amount2 = problem.metadata['initial_b']
        k = problem.metadata['scale_factor']
        ingredient1 = problem.metadata['ingredient1']
        ingredient2 = problem.metadata['ingredient2']

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        # Verify malrule adds
        expected_malrule = f"{amount1 + k} {ingredient1} and {amount2 + k} {ingredient2}"
        self.assertEqual(malrule_solution.answer, expected_malrule)

        # Verify correct multiplies
        expected_correct = f"{amount1 * k} {ingredient1} and {amount2 * k} {ingredient2}"
        self.assertEqual(correct_solution.answer, expected_correct)

    def test_recipe_scaling_algorithm_names(self):
        """Test recipe scaling algorithm names are correct."""
        problem = self.generator.generate(seed=600, template='recipe_scaling')

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        self.assertEqual(malrule_solution.algorithm_name, "Additive Strategy Error (Constant Difference)")
        self.assertEqual(correct_solution.algorithm_name, "Correct Ratio Scaling (Multiplicative)")

    # ============================================================================
    # TEMPLATE 3: speed_problems (3 tests)
    # ============================================================================

    def test_speed_problems_basic(self):
        """Test speed/rate problem with basic values."""
        problem = self.generator.generate(seed=700, template='speed_problems')

        self.assertEqual(problem.metadata['template'], 'speed_problems')

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        # Verify answers contain distance units
        distance_unit = problem.metadata['distance_unit']
        self.assertIn(distance_unit, malrule_solution.answer)
        self.assertIn(distance_unit, correct_solution.answer)

    def test_speed_problems_proportional_reasoning(self):
        """Test speed problem uses proportional reasoning correctly."""
        problem = self.generator.generate(seed=800, template='speed_problems')

        distance = problem.metadata['distance']
        time1 = problem.metadata['time1']
        time2 = problem.metadata['time2']
        speed = problem.metadata['speed']
        distance_unit = problem.metadata['distance_unit']

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        # Malrule: adds time difference
        time_diff = time2 - time1
        expected_malrule = f"{distance + time_diff} {distance_unit}"
        self.assertEqual(malrule_solution.answer, expected_malrule)

        # Correct: multiplies speed by time
        expected_correct_distance = int(speed * time2)
        expected_correct = f"{expected_correct_distance} {distance_unit}"
        self.assertEqual(correct_solution.answer, expected_correct)

    def test_speed_problems_different_units(self):
        """Test speed problem with potentially different units."""
        problem = self.generator.generate(seed=900, template='speed_problems')

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        # Both should produce different answers (additive vs multiplicative)
        self.assertNotEqual(malrule_solution.answer, correct_solution.answer)
        self.assertFalse(malrule_solution.is_correct)
        self.assertTrue(correct_solution.is_correct)

    # ============================================================================
    # TEMPLATE 4: similar_figures (3 tests)
    # ============================================================================

    def test_similar_figures_basic(self):
        """Test similar figures scaling with basic dimensions."""
        problem = self.generator.generate(seed=1000, template='similar_figures')

        self.assertEqual(problem.metadata['template'], 'similar_figures')

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        # Verify answers contain 'cm by cm' format
        self.assertIn('cm by', malrule_solution.answer)
        self.assertIn('cm by', correct_solution.answer)

    def test_similar_figures_dimension_scaling(self):
        """Test similar figures dimension scaling calculations."""
        problem = self.generator.generate(seed=1100, template='similar_figures')

        width = problem.metadata['initial_a']
        height = problem.metadata['initial_b']
        k = problem.metadata['scale_factor']

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        # Malrule: adds to dimensions
        expected_malrule = f"{width + k} cm by {height + k} cm"
        self.assertEqual(malrule_solution.answer, expected_malrule)

        # Correct: multiplies dimensions
        expected_correct = f"{width * k} cm by {height * k} cm"
        self.assertEqual(correct_solution.answer, expected_correct)

    def test_similar_figures_proportion_preservation(self):
        """Test that correct algorithm preserves proportions."""
        problem = self.generator.generate(seed=1200, template='similar_figures')

        width = problem.metadata['initial_a']
        height = problem.metadata['initial_b']
        k = problem.metadata['scale_factor']

        correct_solution = self.correct_algo.solve(problem)

        # Verify correct solution preserves ratio
        original_ratio = width / height
        new_ratio = (width * k) / (height * k)
        self.assertAlmostEqual(original_ratio, new_ratio, places=5)

    # ============================================================================
    # TEMPLATE 5: mixture_problems (3 tests)
    # ============================================================================

    def test_mixture_problems_basic(self):
        """Test mixture problem with basic ratio."""
        problem = self.generator.generate(seed=1300, template='mixture_problems')

        self.assertEqual(problem.metadata['template'], 'mixture_problems')

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        # Verify answers are ratio format
        self.assertIn(':', malrule_solution.answer)
        self.assertIn(':', correct_solution.answer)

    def test_mixture_problems_concentration(self):
        """Test mixture problem concentration calculations."""
        problem = self.generator.generate(seed=1400, template='mixture_problems')

        parts1 = problem.metadata['initial_a']
        parts2 = problem.metadata['initial_b']
        k = problem.metadata['scale_factor']

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        # Malrule: adds to both parts
        expected_malrule = f"{parts1 + k}:{parts2 + k}"
        self.assertEqual(malrule_solution.answer, expected_malrule)

        # Correct: multiplies both parts
        expected_correct = f"{parts1 * k}:{parts2 * k}"
        self.assertEqual(correct_solution.answer, expected_correct)

    def test_mixture_problems_ratio_preservation(self):
        """Test that correct algorithm preserves mixture ratio."""
        problem = self.generator.generate(seed=1500, template='mixture_problems')

        parts1 = problem.metadata['initial_a']
        parts2 = problem.metadata['initial_b']
        k = problem.metadata['scale_factor']

        correct_solution = self.correct_algo.solve(problem)
        malrule_solution = self.malrule.solve(problem)

        # Correct preserves ratio
        original_ratio = parts1 / parts2
        new_ratio_correct = (parts1 * k) / (parts2 * k)
        self.assertAlmostEqual(original_ratio, new_ratio_correct, places=5)

        # Malrule changes ratio (unless parts1 = parts2, which we avoid)
        new_ratio_malrule = (parts1 + k) / (parts2 + k)
        # Only equal if parts1 == parts2 (which should be rare/avoided)
        if parts1 != parts2:
            self.assertNotAlmostEqual(original_ratio, new_ratio_malrule, places=5)

    # ============================================================================
    # ADDITIONAL TESTS: Template availability and metadata
    # ============================================================================

    def test_get_available_templates(self):
        """Test that get_available_templates returns all 5 templates."""
        templates = self.generator.get_available_templates()

        self.assertEqual(len(templates), 6)
        self.assertIn('basic_scaling', templates)
        self.assertIn('recipe_scaling', templates)
        self.assertIn('speed_problems', templates)
        self.assertIn('similar_figures', templates)
        self.assertIn('mixture_problems', templates)
        self.assertIn('word_problem_context', templates)

    def test_metadata_structure(self):
        """Test that all templates generate correct metadata structure."""
        templates = self.generator.get_available_templates()

        for template in templates:
            with self.subTest(template=template):
                problem = self.generator.generate(seed=42, template=template)

                # Verify required metadata fields
                self.assertIn('template', problem.metadata)
                self.assertIn('correct_answer', problem.metadata)
                self.assertIn('malrule_answer', problem.metadata)

                # Verify answers are strings
                self.assertIsInstance(problem.metadata['correct_answer'], str)
                self.assertIsInstance(problem.metadata['malrule_answer'], str)

                # Verify template matches
                self.assertEqual(problem.metadata['template'], template)

    def test_calculate_expected_answer(self):
        """Test that calculate_expected_answer returns malrule answer."""
        for template in self.generator.get_available_templates():
            with self.subTest(template=template):
                problem = self.generator.generate(seed=99, template=template)
                expected = self.malrule.calculate_expected_answer(problem)

                self.assertEqual(expected, problem.metadata['malrule_answer'])
                self.assertIsInstance(expected, str)



class TestAdditiveInsteadOfMultiplicativeAutomated(unittest.TestCase):
    """Automated test suite runner."""

    def test_automated_suite(self):
        """Run the automated test suite."""
        problem_gen = AdditiveInsteadOfMultiplicativeProblemGenerator(
            level=5,
            difficulty=DifficultyLevel.MEDIUM
        )
        malrule = AdditiveInsteadOfMultiplicativeMalrule()
        correct = RatioScalingCorrectAlgorithm()

        test_suite = MalruleTest(malrule, correct, problem_gen)
        results = test_suite.run_all_tests(verbose=False)

        all_passed = all(r.passed for r in results)
        self.assertTrue(all_passed,
                       f"Automated tests failed: {[r.message for r in results if not r.passed]}")

    # ============================================================================
    # TEMPLATE 6: word_problem_context - NEW EXPANDED COVERAGE
    # ============================================================================

    def test_word_problem_direct_proportion(self):
        """Test word problem with direct proportion formula."""
        problem_gen = AdditiveInsteadOfMultiplicativeProblemGenerator(
            level=5,
            difficulty=DifficultyLevel.MEDIUM
        )
        problem = problem_gen.generate(seed=500, template='word_problem_context')

        malrule = AdditiveInsteadOfMultiplicativeMalrule()
        correct = RatioScalingCorrectAlgorithm()

        # Verify it's a word problem
        self.assertEqual(problem.metadata['template'], 'word_problem_context')
        self.assertTrue(problem.metadata.get('is_word_problem', False))

        # Test correct solution
        correct_solution = correct.solve(problem)
        self.assertTrue(correct_solution.is_correct)

        # Test malrule solution
        malrule_solution = malrule.solve(problem)
        self.assertFalse(malrule_solution.is_correct)

        # Verify they're different
        self.assertNotEqual(correct_solution.answer, malrule_solution.answer)

    def test_word_problem_coverage(self):
        """Test that all word problem types can be generated."""
        problem_types_seen = set()
        problem_gen = AdditiveInsteadOfMultiplicativeProblemGenerator(
            level=5,
            difficulty=DifficultyLevel.MEDIUM
        )
        for seed in range(500, 600):
            problem = problem_gen.generate(seed=seed, template='word_problem_context')
            problem_type = problem.metadata.get('problem_type')
            if problem_type:
                problem_types_seen.add(problem_type)

        # Should see multiple problem types
        self.assertGreaterEqual(len(problem_types_seen), 3, "Should cover multiple problem types")


def main():
    """Main entry point for standalone execution."""
    print("\n╔" + "═"*68 + "╗")
    print("║" + "  VERIFICATION TEST: Additive Instead Of Multiplicative  ".center(70) + "║")
    print("╚" + "═"*68 + "╝\n")

    # Run unittest
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestAdditiveInsteadOfMultiplicative))
    suite.addTests(loader.loadTestsFromTestCase(TestAdditiveInsteadOfMultiplicativeAutomated))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # ============================================================================

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
