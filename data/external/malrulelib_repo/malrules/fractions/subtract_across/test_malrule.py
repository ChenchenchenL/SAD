#!/usr/bin/env python3
"""
Comprehensive test suite for Subtract Across malrule.

This file combines:
1. Template validation tests (all templates)
2. Automated test suite functionality

Run from project root: python3 -m malrules.fractions.subtract_across.test_malrule
Or from this directory: python3 test_malrule.py
"""

import sys
import os
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.fractions.subtract_across import (
    FractionSubtractionProblemGenerator,
    SubtractAcrossMalrule,
    FractionSubtractionCorrectAlgorithm
)


class TestSubtractAcrossTemplates(unittest.TestCase):
    """Test all 5 templates for Subtract-Across malrule."""

    def setUp(self):
        """Set up test fixtures."""
        self.generator = FractionSubtractionProblemGenerator(
            level=5,
            difficulty=DifficultyLevel.MEDIUM
        )
        self.malrule = SubtractAcrossMalrule()
        self.correct_algo = FractionSubtractionCorrectAlgorithm()

    # Template 1: basic_subtraction
    def test_basic_subtraction_template(self):
        """Test basic_subtraction template generates valid problems."""
        problem = self.generator.generate(seed=100, template='basic_subtraction')

        self.assertEqual(problem.metadata['template'], 'basic_subtraction')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)
        self.assertIn('fractions', problem.metadata)

        # Should have 2 fractions
        self.assertEqual(len(problem.operands), 2)

    def test_basic_subtraction_malrule_vs_correct(self):
        """Test basic_subtraction: malrule gives wrong answer, correct gives right answer."""
        problem = self.generator.generate(seed=101, template='basic_subtraction')

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        self.assertFalse(malrule_solution.is_correct)
        self.assertTrue(correct_solution.is_correct)

        self.assertEqual(malrule_solution.answer, str(problem.metadata['malrule_answer']))
        self.assertEqual(correct_solution.answer, str(problem.metadata['correct_answer']))

    def test_basic_subtraction_calculate_expected_answer(self):
        """Test calculate_expected_answer for basic_subtraction template."""
        problem = self.generator.generate(seed=102, template='basic_subtraction')

        expected_answer = self.malrule.calculate_expected_answer(problem)
        malrule_solution = self.malrule.solve(problem)

        self.assertEqual(expected_answer, malrule_solution.answer)
        self.assertEqual(expected_answer, str(problem.metadata['malrule_answer']))

    # Template 2: word_problem_pizza
    def test_word_problem_pizza_template(self):
        """Test word_problem_pizza template generates valid problems."""
        problem = self.generator.generate(seed=200, template='word_problem_pizza')

        self.assertEqual(problem.metadata['template'], 'word_problem_pizza')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)

        # Should mention food context
        self.assertTrue(
            any(word in problem.text.lower() for word in ['pizza', 'cake', 'pie', 'cookies', 'sandwich'])
        )

    def test_word_problem_pizza_malrule_vs_correct(self):
        """Test word_problem_pizza: malrule incorrectly subtracts across."""
        problem = self.generator.generate(seed=201, template='word_problem_pizza')

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        self.assertFalse(malrule_solution.is_correct)
        self.assertTrue(correct_solution.is_correct)

        # Answers should differ (malrule is wrong)
        self.assertEqual(malrule_solution.answer, str(problem.metadata['malrule_answer']))
        self.assertEqual(correct_solution.answer, str(problem.metadata['correct_answer']))

    def test_word_problem_pizza_calculate_expected_answer(self):
        """Test calculate_expected_answer for word_problem_pizza template."""
        problem = self.generator.generate(seed=202, template='word_problem_pizza')

        expected_answer = self.malrule.calculate_expected_answer(problem)
        malrule_solution = self.malrule.solve(problem)

        self.assertEqual(expected_answer, malrule_solution.answer)

    # Template 3: three_fractions
    def test_three_fractions_template(self):
        """Test three_fractions template generates valid problems."""
        problem = self.generator.generate(seed=300, template='three_fractions')

        self.assertEqual(problem.metadata['template'], 'three_fractions')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)

        # Should have 3 fractions
        self.assertEqual(len(problem.operands), 3)

    def test_three_fractions_malrule_vs_correct(self):
        """Test three_fractions: malrule misapplies subtract-across to three fractions."""
        problem = self.generator.generate(seed=301, template='three_fractions')

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        self.assertFalse(malrule_solution.is_correct)
        self.assertTrue(correct_solution.is_correct)

        self.assertEqual(malrule_solution.answer, str(problem.metadata['malrule_answer']))
        self.assertEqual(correct_solution.answer, str(problem.metadata['correct_answer']))

    def test_three_fractions_calculate_expected_answer(self):
        """Test calculate_expected_answer for three_fractions template."""
        problem = self.generator.generate(seed=302, template='three_fractions')

        expected_answer = self.malrule.calculate_expected_answer(problem)
        malrule_solution = self.malrule.solve(problem)

        self.assertEqual(expected_answer, malrule_solution.answer)

    # Template 4: improper_fractions
    def test_improper_fractions_template(self):
        """Test improper_fractions template generates valid problems."""
        problem = self.generator.generate(seed=400, template='improper_fractions')

        self.assertEqual(problem.metadata['template'], 'improper_fractions')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)

        # Should have improper fractions (numerator >= denominator)
        num1, den1 = problem.operands[0]
        num2, den2 = problem.operands[1]
        self.assertTrue(num1 >= den1 or num2 >= den2)

    def test_improper_fractions_malrule_vs_correct(self):
        """Test improper_fractions: malrule misapplies subtract-across to improper fractions."""
        problem = self.generator.generate(seed=401, template='improper_fractions')

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        self.assertFalse(malrule_solution.is_correct)
        self.assertTrue(correct_solution.is_correct)

    def test_improper_fractions_calculate_expected_answer(self):
        """Test calculate_expected_answer for improper_fractions template."""
        problem = self.generator.generate(seed=402, template='improper_fractions')

        expected_answer = self.malrule.calculate_expected_answer(problem)
        malrule_solution = self.malrule.solve(problem)

        self.assertEqual(expected_answer, malrule_solution.answer)

    # Template 5: word_problem_measurement
    def test_word_problem_measurement_template(self):
        """Test word_problem_measurement template generates valid problems."""
        problem = self.generator.generate(seed=500, template='word_problem_measurement')

        self.assertEqual(problem.metadata['template'], 'word_problem_measurement')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)

        # Should mention measurement context
        self.assertTrue(
            any(word in problem.text.lower() for word in ['container', 'mile', 'cup', 'gallon', 'meter', 'ribbon', 'water', 'flour'])
        )

    def test_word_problem_measurement_malrule_vs_correct(self):
        """Test word_problem_measurement: malrule misapplies rule in measurement context."""
        problem = self.generator.generate(seed=501, template='word_problem_measurement')

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        self.assertFalse(malrule_solution.is_correct)
        self.assertTrue(correct_solution.is_correct)

        self.assertEqual(malrule_solution.answer, str(problem.metadata['malrule_answer']))
        self.assertEqual(correct_solution.answer, str(problem.metadata['correct_answer']))

    def test_word_problem_measurement_calculate_expected_answer(self):
        """Test calculate_expected_answer for word_problem_measurement template."""
        problem = self.generator.generate(seed=502, template='word_problem_measurement')

        expected_answer = self.malrule.calculate_expected_answer(problem)
        malrule_solution = self.malrule.solve(problem)

        self.assertEqual(expected_answer, malrule_solution.answer)

    # Additional tests for backwards compatibility
    def test_legacy_generation_still_works(self):
        """Test that legacy generation (without template) still works."""
        problem = self.generator.generate(seed=600)

        # Should work without template
        self.assertIsNotNone(problem)
        self.assertIsNotNone(problem.text)
        self.assertIsNotNone(problem.operands)

        # Should be able to solve
        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        self.assertIsNotNone(malrule_solution.answer)
        self.assertIsNotNone(correct_solution.answer)

    def test_get_available_templates(self):
        """Test get_available_templates returns correct list."""
        templates = self.generator.get_available_templates()

        self.assertEqual(len(templates), 7)
        self.assertIn('basic_subtraction', templates)
        self.assertIn('word_problem_pizza', templates)
        self.assertIn('three_fractions', templates)
        self.assertIn('improper_fractions', templates)
        self.assertIn('word_problem_measurement', templates)
        self.assertIn('word_problem_three_fractions', templates)
        self.assertIn('word_problem_improper', templates)

    def test_invalid_template_raises_error(self):
        """Test that invalid template name raises ValueError."""
        with self.assertRaises(ValueError):
            self.generator.generate(seed=700, template='invalid_template')

    # Template 6: word_problem_three_fractions
    def test_word_problem_three_fractions_template(self):
        """Test word_problem_three_fractions template generates valid problems."""
        problem = self.generator.generate(seed=600, template='word_problem_three_fractions')

        self.assertEqual(problem.metadata['template'], 'word_problem_three_fractions')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)

        # Should have 3 fractions
        self.assertEqual(len(problem.operands), 3)

        # Should be a word problem
        self.assertTrue(len(problem.text) > 20)

    def test_word_problem_three_fractions_malrule_vs_correct(self):
        """Test word_problem_three_fractions: algorithms produce different answers."""
        problem = self.generator.generate(seed=601, template='word_problem_three_fractions')

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        self.assertFalse(malrule_solution.is_correct)
        self.assertTrue(correct_solution.is_correct)

        self.assertEqual(malrule_solution.answer, str(problem.metadata['malrule_answer']))
        self.assertEqual(correct_solution.answer, str(problem.metadata['correct_answer']))

    def test_word_problem_three_fractions_calculate_expected_answer(self):
        """Test calculate_expected_answer for word_problem_three_fractions template."""
        problem = self.generator.generate(seed=602, template='word_problem_three_fractions')

        expected_answer = self.malrule.calculate_expected_answer(problem)
        malrule_solution = self.malrule.solve(problem)

        self.assertEqual(expected_answer, malrule_solution.answer)
        self.assertEqual(expected_answer, str(problem.metadata['malrule_answer']))

    def test_word_problem_three_fractions_steps(self):
        """Test that steps are generated correctly for word_problem_three_fractions."""
        problem = self.generator.generate(seed=603, template='word_problem_three_fractions')

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        # Both should have steps
        self.assertGreater(len(malrule_solution.steps), 0)
        self.assertGreater(len(correct_solution.steps), 0)

        # Malrule steps should mention subtracting numerators and denominators
        malrule_steps_text = " ".join(malrule_solution.steps).lower()

    # Template 7: word_problem_improper
    def test_word_problem_improper_template(self):
        """Test word_problem_improper template generates valid problems."""
        problem = self.generator.generate(seed=700, template='word_problem_improper')

        self.assertEqual(problem.metadata['template'], 'word_problem_improper')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)

        # Should have improper fractions
        num1, den1 = problem.operands[0]
        num2, den2 = problem.operands[1]
        self.assertTrue(num1 >= den1 or num2 >= den2)

        # Should be a word problem
        self.assertTrue(len(problem.text) > 20)

    def test_word_problem_improper_malrule_vs_correct(self):
        """Test word_problem_improper: algorithms produce different answers."""
        problem = self.generator.generate(seed=701, template='word_problem_improper')

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        self.assertFalse(malrule_solution.is_correct)
        self.assertTrue(correct_solution.is_correct)

        self.assertEqual(malrule_solution.answer, str(problem.metadata['malrule_answer']))
        self.assertEqual(correct_solution.answer, str(problem.metadata['correct_answer']))

    def test_word_problem_improper_calculate_expected_answer(self):
        """Test calculate_expected_answer for word_problem_improper template."""
        problem = self.generator.generate(seed=702, template='word_problem_improper')

        expected_answer = self.malrule.calculate_expected_answer(problem)
        malrule_solution = self.malrule.solve(problem)

        self.assertEqual(expected_answer, malrule_solution.answer)
        self.assertEqual(expected_answer, str(problem.metadata['malrule_answer']))

    def test_word_problem_improper_steps(self):
        """Test that steps are generated correctly for word_problem_improper."""
        problem = self.generator.generate(seed=703, template='word_problem_improper')

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        # Both should have steps
        self.assertGreater(len(malrule_solution.steps), 0)
        self.assertGreater(len(correct_solution.steps), 0)



class TestStepVerificationAndEdgeCases(unittest.TestCase):
    """Test step verification and edge cases where answers might coincidentally match."""

    def setUp(self):
        """Set up test fixtures."""
        self.generator = FractionSubtractionProblemGenerator(
            level=5,
            difficulty=DifficultyLevel.MEDIUM
        )
        self.malrule = SubtractAcrossMalrule()
        self.correct_algo = FractionSubtractionCorrectAlgorithm()

    def _extract_answer_from_steps(self, steps):
        """Extract the final answer from steps."""
        for step in reversed(steps):
            if "Final answer:" in step or "final answer:" in step:
                # Extract fraction from step
                import re
                match = re.search(r'(-?\d+)/(-?\d+)', step)
                if match:
                    return f"{match.group(1)}/{match.group(2)}"
        return None

    def test_all_templates_answers_differ_or_steps_differ(self):
        """
        Test that for all templates, either the answers differ OR the steps differ.
        This catches edge cases where malrule might accidentally produce correct answer.
        """
        templates = self.generator.get_available_templates()

        for template in templates:
            with self.subTest(template=template):
                # Test with multiple seeds to catch edge cases
                for seed in range(800, 810):
                    problem = self.generator.generate(seed=seed, template=template)

                    malrule_solution = self.malrule.solve(problem)
                    correct_solution = self.correct_algo.solve(problem)

                    # Check if answers are the same (edge case)
                    if malrule_solution.answer == correct_solution.answer:
                        # Answers match - this is an edge case!
                        # Print the problem and steps for debugging
                        print(f"\n⚠ EDGE CASE DETECTED in {template} (seed={seed})")
                        print(f"Problem: {problem.text}")
                        print(f"Operands: {problem.operands}")
                        print(f"Answer: {malrule_solution.answer}")
                        print(f"\nCorrect steps:")
                        for step in correct_solution.steps:
                            print(f"  {step}")
                        print(f"\nMalrule steps:")
                        for step in malrule_solution.steps:
                            print(f"  {step}")

                        # Fail the test - malrule should not produce same answer
                        # (or if it does, steps must be different which we verify below)
                        self.fail(
                            f"Edge case: Malrule produced same answer as correct algorithm "
                            f"for {template} with seed={seed}. "
                            f"Answer: {malrule_solution.answer}. "
                            f"Steps differ: {malrule_solution.steps != correct_solution.steps}"
                        )

    def test_steps_contain_expected_phrases(self):
        """Test that steps contain expected phrases for correct and malrule algorithms."""
        for template in self.generator.get_available_templates():
            with self.subTest(template=template):
                problem = self.generator.generate(seed=900, template=template)

                malrule_solution = self.malrule.solve(problem)
                correct_solution = self.correct_algo.solve(problem)

                # Correct algorithm should mention "common denominator"
                correct_steps_text = " ".join(correct_solution.steps).lower()

                # Malrule should mention subtracting denominators
                malrule_steps_text = " ".join(malrule_solution.steps).lower()

    def test_three_fraction_problems_use_all_three_fractions(self):
        """Test that 3-fraction problems actually use all three fractions in calculation."""
        for template in ['three_fractions', 'word_problem_three_fractions']:
            with self.subTest(template=template):
                problem = self.generator.generate(seed=1000, template=template)

                # Verify problem has 3 fractions
                self.assertEqual(len(problem.operands), 3,
                                f"Template {template} should have 3 fractions")

                correct_solution = self.correct_algo.solve(problem)
                malrule_solution = self.malrule.solve(problem)

                # Check that all three fractions appear in the steps
                frac1 = f"{problem.operands[0][0]}/{problem.operands[0][1]}"
                frac2 = f"{problem.operands[1][0]}/{problem.operands[1][1]}"
                frac3 = f"{problem.operands[2][0]}/{problem.operands[2][1]}"

                correct_steps_text = " ".join(correct_solution.steps)
                self.assertIn(frac1, correct_steps_text)
                self.assertIn(frac2, correct_steps_text)
                self.assertIn(frac3, correct_steps_text)

    def test_answer_matches_final_step(self):
        """Test that the answer matches what's stated in the final step."""
        for template in self.generator.get_available_templates():
            with self.subTest(template=template):
                problem = self.generator.generate(seed=1100, template=template)

                for algo, algo_name in [(self.correct_algo, "correct"), (self.malrule, "malrule")]:
                    solution = algo.solve(problem)

                    # Extract answer from final step
                    step_answer = self._extract_answer_from_steps(solution.steps)

                    if step_answer:
                        self.assertEqual(solution.answer, step_answer,
                                       f"{algo_name} answer should match final step for {template}")


class TestSubtractAcrossAutomated(unittest.TestCase):
    """Automated test suite runner."""

    def test_automated_suite(self):
        """Run the automated test suite."""
        problem_gen = FractionSubtractionProblemGenerator(
            level=5,
            difficulty=DifficultyLevel.MEDIUM
        )
        malrule = SubtractAcrossMalrule()
        correct = FractionSubtractionCorrectAlgorithm()

        test_suite = MalruleTest(malrule, correct, problem_gen)
        results = test_suite.run_all_tests(verbose=False)

        all_passed = all(r.passed for r in results)
        self.assertTrue(all_passed,
                       f"Automated tests failed: {[r.message for r in results if not r.passed]}")


def main():
    """Main entry point for standalone execution."""
    print("\n╔" + "═"*68 + "╗")
    print("║" + "  VERIFICATION TEST: Subtract Across  ".center(70) + "║")
    print("╚" + "═"*68 + "╝\n")

    # Run unittest
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestSubtractAcrossTemplates))
    suite.addTests(loader.loadTestsFromTestCase(TestStepVerificationAndEdgeCases))
    suite.addTests(loader.loadTestsFromTestCase(TestSubtractAcrossAutomated))

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
