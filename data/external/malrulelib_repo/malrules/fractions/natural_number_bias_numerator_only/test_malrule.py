#!/usr/bin/env python3
"""
Comprehensive test suite for Natural Number Bias Numerator Only malrule.

This file combines:
1. Template validation tests (all templates)
2. Automated test suite functionality

Run from project root: python3 -m malrules.fractions.natural_number_bias_numerator_only.test_malrule
Or from this directory: python3 test_malrule.py
"""

import sys
import os
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.fractions.natural_number_bias_numerator_only import (
    NaturalNumberBiasNumeratorOnlyProblemGenerator,
    NaturalNumberBiasNumeratorOnlyMalrule,
    FractionComparisonCorrectAlgorithm
)


class TestNaturalNumberBiasNumeratorOnly(unittest.TestCase):
    """Test cases for Natural-Number-Bias-Numerator-Only malrule."""

    def setUp(self):
        """Set up test fixtures."""
        self.generator = NaturalNumberBiasNumeratorOnlyProblemGenerator(
            level=5,
            difficulty=DifficultyLevel.MEDIUM
        )
        self.malrule = NaturalNumberBiasNumeratorOnlyMalrule()
        self.correct_algo = FractionComparisonCorrectAlgorithm()

    def test_get_available_templates(self):
        """Test that all 5 templates are available."""
        templates = self.generator.get_available_templates()
        self.assertEqual(len(templates), 7)
        expected = [
            'basic_comparison',
            'visual_models',
            'real_world_context',
            'multiple_choice',
            'word_problem_multiple_choice',
            'ordering',
            'word_problem_ordering'
        ]
        for template in expected:
            self.assertIn(template, templates)

    def test_basic_comparison_template(self):
        """Test basic_comparison template."""
        problem = self.generator.generate(seed=42, template='basic_comparison')

        # Check problem structure
        self.assertEqual(problem.operation, 'fraction_comparison')
        self.assertIn('template', problem.metadata)
        self.assertEqual(problem.metadata['template'], 'basic_comparison')

        # Check metadata has required fields
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)
        self.assertIn('num1', problem.metadata)
        self.assertIn('den1', problem.metadata)
        self.assertIn('num2', problem.metadata)
        self.assertIn('den2', problem.metadata)

        # Verify answers are strings
        self.assertIsInstance(problem.metadata['correct_answer'], str)
        self.assertIsInstance(problem.metadata['malrule_answer'], str)

    def test_visual_models_template(self):
        """Test visual_models template."""
        problem = self.generator.generate(seed=42, template='visual_models')

        self.assertEqual(problem.metadata['template'], 'visual_models')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)

        # Should mention visual model in text
        self.assertTrue(
            any(word in problem.text.lower() for word in ['circle', 'bar', 'rectangle', 'shaded'])
        )

    def test_real_world_context_template(self):
        """Test real_world_context template."""
        problem = self.generator.generate(seed=42, template='real_world_context')

        self.assertEqual(problem.metadata['template'], 'real_world_context')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)

        # Should have real-world context
        self.assertTrue(
            any(word in problem.text.lower() for word in ['pizza', 'bag', 'tank', 'walk', 'mile'])
        )

    def test_multiple_choice_template(self):
        """Test multiple_choice template."""
        problem = self.generator.generate(seed=42, template='multiple_choice')

        self.assertEqual(problem.metadata['template'], 'multiple_choice')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)

        # Should have 3 fractions
        self.assertIn('fraction3', problem.metadata)
        self.assertIn('num3', problem.metadata)
        self.assertIn('den3', problem.metadata)

    def test_ordering_template(self):
        """Test ordering template."""
        problem = self.generator.generate(seed=42, template='ordering')

        self.assertEqual(problem.metadata['template'], 'ordering')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)

        # Should have 3 fractions
        self.assertIn('fraction3', problem.metadata)

        # Answer should be a comma-separated list
        self.assertIn(',', problem.metadata['correct_answer'])
        self.assertIn(',', problem.metadata['malrule_answer'])

    def test_calculate_expected_answer(self):
        """Test calculate_expected_answer() for all templates."""
        for template in self.generator.get_available_templates():
            with self.subTest(template=template):
                problem = self.generator.generate(seed=42, template=template)

                # Calculate expected answer
                expected = self.malrule.calculate_expected_answer(problem)

                # Should match metadata malrule_answer
                metadata_answer = problem.metadata['malrule_answer']
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
        # Test on 2-fraction templates only (multiple_choice/ordering have complex answers)
        for template in ['basic_comparison', 'visual_models', 'real_world_context']:
            with self.subTest(template=template):
                problem = self.generator.generate(seed=42, template=template)

                malrule_solution = self.malrule.solve(problem)
                correct_solution = self.correct_algo.solve(problem)

                # Answers should be different (this is the whole point of the malrule!)
                self.assertNotEqual(malrule_solution.answer, correct_solution.answer,
                                  f"Malrule and correct should differ for {template}")

    def test_specific_example_3_4_vs_5_8(self):
        """Test classic example: 3/4 vs 5/8 where numerator comparison is wrong."""
        from utils import Problem

        # 3/4 = 0.75, 5/8 = 0.625, so 3/4 > 5/8
        # But student comparing numerators thinks 3 < 5, so 3/4 < 5/8 (WRONG)
        problem = Problem(
            text="Which is larger: 3/4 or 5/8?",
            operands=[3, 4, 5, 8],
            operation='fraction_comparison',
            level=5,
            difficulty=DifficultyLevel.MEDIUM,
            metadata={
                'num1': 3,
                'den1': 4,
                'num2': 5,
                'den2': 8,
                'correct_answer': '3/4',
                'malrule_answer': '5/8',
                'template': 'basic_comparison'
            }
        )

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        # Correct: 3/4 is larger
        self.assertEqual(correct_solution.answer, '3/4')

        # Malrule: 5/8 is larger (because 5 > 3)
        self.assertEqual(malrule_solution.answer, '5/8')

    def test_backwards_compatibility(self):
        """Test that old problems without metadata still work."""
        from utils import Problem

        # Create old-style problem without template metadata
        old_problem = Problem(
            text="Which is larger: 2/5 or 3/7?",
            operands=[2, 5, 3, 7],
            operation='fraction_comparison',
            level=5,
            difficulty=DifficultyLevel.MEDIUM,
            metadata={
                'num1': 2,
                'den1': 5,
                'num2': 3,
                'den2': 7
            }
        )

        # Should still work
        malrule_solution = self.malrule.solve(old_problem)
        correct_solution = self.correct_algo.solve(old_problem)

        self.assertIsInstance(malrule_solution.answer, str)
        self.assertIsInstance(correct_solution.answer, str)

    def test_numerator_bias_behavior(self):
        """Test that malrule always chooses based on numerator only."""
        # Create a problem where smaller numerator is larger fraction
        problem = self.generator.generate(seed=100, template='basic_comparison')

        num1 = problem.metadata['num1']
        num2 = problem.metadata['num2']

        # Get solutions
        malrule_solution = self.malrule.solve(problem)

        # Malrule should choose based on numerator only
        if num1 > num2:
            self.assertIn(f"{num1}/", malrule_solution.answer)
        elif num1 < num2:
            self.assertIn(f"{num2}/", malrule_solution.answer)
        else:
            self.assertEqual(malrule_solution.answer, "equal")



class TestNaturalNumberBiasNumeratorOnlyAutomated(unittest.TestCase):
    """Automated test suite runner."""

    def test_automated_suite(self):
        """Run the automated test suite."""
        problem_gen = NaturalNumberBiasNumeratorOnlyProblemGenerator(
            level=5,
            difficulty=DifficultyLevel.MEDIUM
        )
        malrule = NaturalNumberBiasNumeratorOnlyMalrule()
        correct = FractionComparisonCorrectAlgorithm()

        test_suite = MalruleTest(malrule, correct, problem_gen)
        results = test_suite.run_all_tests(verbose=False)

        all_passed = all(r.passed for r in results)
        self.assertTrue(all_passed,
                       f"Automated tests failed: {[r.message for r in results if not r.passed]}")


def main():
    """Main entry point for standalone execution."""
    print("\n╔" + "═"*68 + "╗")
    print("║" + "  VERIFICATION TEST: Natural Number Bias Numerator Only  ".center(70) + "║")
    print("╚" + "═"*68 + "╝\n")

    # Run unittest
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestNaturalNumberBiasNumeratorOnly))
    suite.addTests(loader.loadTestsFromTestCase(TestNaturalNumberBiasNumeratorOnlyAutomated))

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
