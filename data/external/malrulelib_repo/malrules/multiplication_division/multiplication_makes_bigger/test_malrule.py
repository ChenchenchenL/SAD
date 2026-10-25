#!/usr/bin/env python3
"""
Comprehensive test suite for Multiplication Makes Bigger malrule.

This file combines:
1. Template validation tests (all templates)
2. Automated test suite functionality

Run from project root: python3 -m malrules.multiplication_division.multiplication_makes_bigger.test_malrule
Or from this directory: python3 test_malrule.py
"""

import sys
import os
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.multiplication_division.multiplication_makes_bigger import (
    MultiplicationProblemGenerator,
    MultiplicationMakesBiggerMalrule,
    MultiplicationCorrectAlgorithm
)


class TestMultiplicationMakesBigger(unittest.TestCase):
    """Test cases for Multiplication-Makes-Bigger malrule."""

    def setUp(self):
        """Set up test fixtures."""
        self.generator = MultiplicationProblemGenerator(
            level=4,
            difficulty=DifficultyLevel.MEDIUM
        )
        self.malrule = MultiplicationMakesBiggerMalrule()
        self.correct_algo = MultiplicationCorrectAlgorithm()

    def test_get_available_templates(self):
        """Test that all 10 templates are available."""
        templates = self.generator.get_available_templates()
        self.assertEqual(len(templates), 10)
        expected = ['basic_decimal_multiplication', 'fraction_multiplication',
                    'money_context', 'measurement_context', 'percent_discount',
                    'area_rectangle', 'probability_compound', 'compound_scaling',
                    'rate_distance', 'volume_box']
        for template in expected:
            self.assertIn(template, templates)

    def test_basic_decimal_multiplication_template(self):
        """Test basic_decimal_multiplication template."""
        problem = self.generator.generate(seed=42, template='basic_decimal_multiplication')

        # Check problem structure
        self.assertEqual(problem.operation, 'multiplication')
        self.assertIn('template', problem.metadata)
        self.assertEqual(problem.metadata['template'], 'basic_decimal_multiplication')

        # Check metadata has required fields
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)
        self.assertIn('factor1', problem.metadata)
        self.assertIn('factor2', problem.metadata)

        # Both factors should be less than 1
        self.assertLess(problem.metadata['factor1'], 1)
        self.assertLess(problem.metadata['factor2'], 1)

        # Verify answers are strings
        self.assertIsInstance(problem.metadata['correct_answer'], str)
        self.assertIsInstance(problem.metadata['malrule_answer'], str)

    def test_fraction_multiplication_template(self):
        """Test fraction_multiplication template."""
        problem = self.generator.generate(seed=42, template='fraction_multiplication')

        self.assertEqual(problem.metadata['template'], 'fraction_multiplication')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)
        self.assertIn('fraction1_str', problem.metadata)
        self.assertIn('fraction2_str', problem.metadata)

        # Should have fraction notation
        self.assertIn('/', problem.metadata['fraction1_str'])
        self.assertIn('/', problem.metadata['fraction2_str'])

    def test_money_context_template(self):
        """Test money_context template."""
        problem = self.generator.generate(seed=42, template='money_context')

        self.assertEqual(problem.metadata['template'], 'money_context')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)

        # Should have money context
        self.assertTrue(
            any(word in problem.text.lower() for word in ['$', 'dollar', 'spend', 'save', 'sale', 'price'])
        )

        # Answers should start with $
        self.assertTrue(problem.metadata['correct_answer'].startswith('$'))
        self.assertTrue(problem.metadata['malrule_answer'].startswith('$'))

    def test_measurement_context_template(self):
        """Test measurement_context template."""
        problem = self.generator.generate(seed=42, template='measurement_context')

        self.assertEqual(problem.metadata['template'], 'measurement_context')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)
        self.assertIn('unit', problem.metadata)

        # Should have measurement context
        self.assertTrue(
            any(word in problem.text.lower() for word in ['recipe', 'flour', 'water', 'cup', 'liter', 'scaling'])
        )

    def test_percent_discount_template(self):
        """Test percent_discount template."""
        problem = self.generator.generate(seed=42, template='percent_discount')

        self.assertEqual(problem.metadata['template'], 'percent_discount')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)
        self.assertIn('discount_percent', problem.metadata)

        # Should have discount context
        self.assertTrue(
            any(word in problem.text.lower() for word in ['discount', 'saved', '%', 'percent'])
        )

        # Answers should start with $
        self.assertTrue(problem.metadata['correct_answer'].startswith('$'))
        self.assertTrue(problem.metadata['malrule_answer'].startswith('$'))

    def test_area_rectangle_template(self):
        """Test area_rectangle template."""
        problem = self.generator.generate(seed=42, template='area_rectangle')

        self.assertEqual(problem.metadata['template'], 'area_rectangle')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)
        self.assertIn('length', problem.metadata)
        self.assertIn('width', problem.metadata)
        self.assertIn('unit', problem.metadata)
        self.assertIn('problem_type', problem.metadata)
        self.assertEqual(problem.metadata['problem_type'], 'area_calculation')

        # Both dimensions should be less than 1
        self.assertLess(problem.metadata['length'], 1)
        self.assertLess(problem.metadata['width'], 1)

        # Should have area context
        self.assertTrue(
            any(word in problem.text.lower() for word in ['area', 'rectangle', 'garden', 'plot'])
        )

    def test_probability_compound_template(self):
        """Test probability_compound template."""
        problem = self.generator.generate(seed=42, template='probability_compound')

        self.assertEqual(problem.metadata['template'], 'probability_compound')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)
        self.assertIn('probability1', problem.metadata)
        self.assertIn('probability2', problem.metadata)
        self.assertIn('problem_type', problem.metadata)
        self.assertEqual(problem.metadata['problem_type'], 'probability_multiplication')

        # Probabilities should be less than 1
        self.assertLess(problem.metadata['probability1'], 1)
        self.assertLess(problem.metadata['probability2'], 1)

        # Should have probability context
        self.assertTrue(
            any(word in problem.text.lower() for word in ['probability', 'event', 'chance'])
        )

    def test_compound_scaling_template(self):
        """Test compound_scaling template."""
        problem = self.generator.generate(seed=42, template='compound_scaling')

        self.assertEqual(problem.metadata['template'], 'compound_scaling')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)
        self.assertIn('scale1', problem.metadata)
        self.assertIn('scale2', problem.metadata)
        self.assertIn('problem_type', problem.metadata)
        self.assertEqual(problem.metadata['problem_type'], 'compound_fraction')

        # Scaling factors should be less than 1
        self.assertLess(problem.metadata['scale1'], 1)
        self.assertLess(problem.metadata['scale2'], 1)

        # Should have scaling context
        self.assertTrue(
            any(word in problem.text.lower() for word in ['of', 'fraction', 'cake', 'sale', 'savings'])
        )

    def test_rate_distance_template(self):
        """Test rate_distance template."""
        problem = self.generator.generate(seed=42, template='rate_distance')

        self.assertEqual(problem.metadata['template'], 'rate_distance')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)
        self.assertIn('rate', problem.metadata)
        self.assertIn('time', problem.metadata)
        self.assertIn('rate_unit', problem.metadata)
        self.assertIn('problem_type', problem.metadata)
        self.assertEqual(problem.metadata['problem_type'], 'rate_time_distance')

        # At least one should be less than 1
        self.assertTrue(problem.metadata['rate'] < 1 or problem.metadata['time'] < 1)

        # Should have distance/rate context
        self.assertTrue(
            any(word in problem.text.lower() for word in ['travel', 'distance', 'walk', 'car', 'rate'])
        )

    def test_volume_box_template(self):
        """Test volume_box template."""
        problem = self.generator.generate(seed=42, template='volume_box')

        self.assertEqual(problem.metadata['template'], 'volume_box')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)
        self.assertIn('length', problem.metadata)
        self.assertIn('width', problem.metadata)
        self.assertIn('height', problem.metadata)
        self.assertIn('unit', problem.metadata)
        self.assertIn('problem_type', problem.metadata)
        self.assertEqual(problem.metadata['problem_type'], 'volume_calculation')

        # All dimensions should be less than 1
        self.assertLess(problem.metadata['length'], 1)
        self.assertLess(problem.metadata['width'], 1)
        self.assertLess(problem.metadata['height'], 1)

        # Should have volume context
        self.assertTrue(
            any(word in problem.text.lower() for word in ['volume', 'box', 'prism', 'dimensions'])
        )

    def test_calculate_expected_answer(self):
        """Test calculate_expected_answer() for all templates."""
        for template in self.generator.get_available_templates():
            with self.subTest(template=template):
                problem = self.generator.generate(seed=42, template=template)

                # Calculate expected answer
                expected = self.malrule.calculate_expected_answer(problem)

                # Should match metadata malrule_answer (numeric part)
                metadata_answer = problem.metadata['malrule_answer']

                # Handle units
                if metadata_answer.startswith('$'):
                    metadata_numeric = metadata_answer[1:]
                elif ' ' in metadata_answer:
                    # Has unit like "2.50 cups"
                    metadata_numeric = metadata_answer.split()[0]
                else:
                    metadata_numeric = metadata_answer

                # Compare as floats (allowing small precision differences)
                self.assertAlmostEqual(float(expected), float(metadata_numeric), places=4,
                                     msg=f"Template {template}: expected {expected} != metadata {metadata_numeric}")

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
        for template in self.generator.get_available_templates():
            with self.subTest(template=template):
                problem = self.generator.generate(seed=42, template=template)

                malrule_solution = self.malrule.solve(problem)
                correct_solution = self.correct_algo.solve(problem)

                # Extract numeric parts for comparison
                malrule_answer = malrule_solution.answer
                correct_answer = correct_solution.answer

                # Remove units for comparison
                if malrule_answer.startswith('$'):
                    malrule_answer = malrule_answer[1:]
                if correct_answer.startswith('$'):
                    correct_answer = correct_answer[1:]
                if ' ' in malrule_answer:
                    malrule_answer = malrule_answer.split()[0]
                if ' ' in correct_answer:
                    correct_answer = correct_answer.split()[0]

                # Answers should be different (unless edge case where malrule accidentally correct)
                # Edge case: if the product happens to not be smaller than both factors
                factor1, factor2 = problem.operands
                product = factor1 * factor2
                if product >= factor1 and product >= factor2:
                    # Edge case: malrule might give correct answer
                    print(f"\n  [Edge case in {template}] Malrule accidentally correct: {malrule_answer} == {correct_answer}")
                    print(f"  Correct steps:\n" + "\n".join([f"    {s}" for s in correct_solution.steps]))
                    print(f"  Malrule steps:\n" + "\n".join([f"    {s}" for s in malrule_solution.steps]))
                else:
                    # Normal case: answers should differ
                    if malrule_answer == correct_answer:
                        print(f"\n  [UNEXPECTED] {template}: Malrule and correct give same answer!")
                        print(f"  Factor1: {factor1}, Factor2: {factor2}, Product: {product}")
                        print(f"  Correct steps:\n" + "\n".join([f"    {s}" for s in correct_solution.steps]))
                        print(f"  Malrule steps:\n" + "\n".join([f"    {s}" for s in malrule_solution.steps]))
                        self.fail(f"Malrule and correct should differ for {template}")
                    else:
                        print(f"  [✓] {template}: Correct={correct_answer}, Malrule={malrule_answer}")

    def test_specific_example_0_5_times_0_2(self):
        """Test the classic example: 0.5 × 0.2 = 0.7 (malrule) vs 0.1 (correct)."""
        # 0.5 × 0.2:
        # Correct: 0.5 × 0.2 = 0.1
        # Malrule: 0.1 < 0.5, so add: 0.5 + 0.2 = 0.7
        problem = Problem(
            text="What is 0.5 × 0.2?",
            operands=[0.5, 0.2],
            operation='multiplication',
            level=4,
            difficulty=DifficultyLevel.MEDIUM,
            metadata={
                'factor1': 0.5,
                'factor2': 0.2,
                'correct_answer': '0.1000',
                'malrule_answer': '0.7000',
                'template': 'basic_decimal_multiplication'
            }
        )

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        # Correct: 0.1000
        self.assertEqual(correct_solution.answer, '0.1000')

        # Malrule: 0.7000 (added instead)
        self.assertEqual(malrule_solution.answer, '0.7000')

    def test_specific_example_one_half_times_one_third(self):
        """Test fraction example: 1/2 × 1/3 = 5/6 (malrule) vs 1/6 (correct)."""
        # 1/2 × 1/3:
        # Correct: 0.5 × 0.333... ≈ 0.1667
        # Malrule: 0.1667 < 0.5, so add: 0.5 + 0.333... ≈ 0.8333
        factor1 = 1/2
        factor2 = 1/3
        correct_product = factor1 * factor2
        malrule_sum = factor1 + factor2

        problem = Problem(
            text="What is 1/2 × 1/3?",
            operands=[factor1, factor2],
            operation='multiplication',
            level=4,
            difficulty=DifficultyLevel.MEDIUM,
            metadata={
                'factor1': factor1,
                'factor2': factor2,
                'numerator1': 1,
                'denominator1': 2,
                'numerator2': 1,
                'denominator2': 3,
                'fraction1_str': '1/2',
                'fraction2_str': '1/3',
                'correct_answer': f'{correct_product:.4f}',
                'malrule_answer': f'{malrule_sum:.4f}',
                'template': 'fraction_multiplication'
            }
        )

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        # Correct: approximately 0.1667
        self.assertAlmostEqual(float(correct_solution.answer), correct_product, places=3)

        # Malrule: approximately 0.8333 (added instead)
        self.assertAlmostEqual(float(malrule_solution.answer), malrule_sum, places=3)

    def test_backwards_compatibility(self):
        """Test that old problems without metadata still work."""
        # Create old-style problem without template metadata
        old_problem = Problem(
            text="What is 0.4 × 0.3?",
            operands=[0.4, 0.3],
            operation='multiplication',
            level=4,
            difficulty=DifficultyLevel.MEDIUM,
            metadata={}
        )

        # Should still work
        malrule_solution = self.malrule.solve(old_problem)
        correct_solution = self.correct_algo.solve(old_problem)

        self.assertIsInstance(malrule_solution.answer, str)
        self.assertIsInstance(correct_solution.answer, str)

        # Verify logic: 0.4 × 0.3 = 0.12 (correct), malrule adds: 0.4 + 0.3 = 0.7
        self.assertEqual(float(correct_solution.answer), 0.12)
        self.assertEqual(float(malrule_solution.answer), 0.7)

    def test_malrule_behavior_both_less_than_one(self):
        """Test that malrule uses addition when both factors < 1."""
        problem = self.generator.generate(seed=100, template='basic_decimal_multiplication')

        factor1 = problem.metadata['factor1']
        factor2 = problem.metadata['factor2']

        # Both factors should be less than 1
        self.assertLess(factor1, 1)
        self.assertLess(factor2, 1)

        # Get solutions
        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        # Correct answer: factor1 * factor2 (should be smaller than both)
        correct_product = factor1 * factor2
        self.assertLess(correct_product, factor1)
        self.assertLess(correct_product, factor2)

        # Malrule should use addition: factor1 + factor2
        expected_malrule = factor1 + factor2

        # Extract numeric part of malrule answer
        malrule_answer = malrule_solution.answer
        if malrule_answer.startswith('$'):
            malrule_answer = malrule_answer[1:]
        if ' ' in malrule_answer:
            malrule_answer = malrule_answer.split()[0]

        self.assertAlmostEqual(float(malrule_answer), expected_malrule, places=3)

    def test_unit_stripping_in_calculate_expected_answer(self):
        """Test that calculate_expected_answer properly strips units."""
        # Test with measurement context (has unit like "2.50 cups")
        problem_measurement = self.generator.generate(seed=50, template='measurement_context')
        expected = self.malrule.calculate_expected_answer(problem_measurement)

        # Should be numeric only, no units
        self.assertFalse(any(unit in expected for unit in ['cups', 'liters', 'kilograms', 'ounces', 'tablespoons']))

        # Test with money context (has $ sign)
        problem_money = self.generator.generate(seed=51, template='money_context')
        expected_money = self.malrule.calculate_expected_answer(problem_money)

        # Should not start with $
        self.assertFalse(expected_money.startswith('$'))

        # Should be a valid number
        float(expected)
        float(expected_money)



class TestMultiplicationMakesBiggerAutomated(unittest.TestCase):
    """Automated test suite runner."""

    def test_automated_suite(self):
        """Run the automated test suite."""
        problem_gen = MultiplicationProblemGenerator(
            level=5,
            difficulty=DifficultyLevel.MEDIUM
        )
        malrule = MultiplicationMakesBiggerMalrule()
        correct = MultiplicationCorrectAlgorithm()

        test_suite = MalruleTest(malrule, correct, problem_gen)
        results = test_suite.run_all_tests(verbose=True)

        all_passed = all(r.passed for r in results)
        self.assertTrue(all_passed,
                       f"Automated tests failed: {[r.message for r in results if not r.passed]}")


def main():
    """Main entry point for standalone execution."""
    print("\n╔" + "═"*68 + "╗")
    print("║" + "  VERIFICATION TEST: Multiplication Makes Bigger  ".center(70) + "║")
    print("╚" + "═"*68 + "╝\n")

    # Run unittest
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestMultiplicationMakesBigger))
    suite.addTests(loader.loadTestsFromTestCase(TestMultiplicationMakesBiggerAutomated))

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
