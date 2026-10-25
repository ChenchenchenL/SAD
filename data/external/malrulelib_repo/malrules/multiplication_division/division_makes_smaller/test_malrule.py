#!/usr/bin/env python3
"""
Comprehensive test suite for Division Makes Smaller malrule.

This file combines:
1. Template validation tests (all templates)
2. Automated test suite functionality

Run from project root: python3 -m malrules.multiplication_division.division_makes_smaller.test_malrule
Or from this directory: python3 test_malrule.py
"""

import sys
import os
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.multiplication_division.division_makes_smaller import (
    DivisionWithDecimalsProblemGenerator,
    DivisionMakesSmallerMalrule,
    DivisionCorrectAlgorithm
)


class TestDivisionMakesSmaller(unittest.TestCase):
    """Test cases for Division-Makes-Smaller malrule."""

    def setUp(self):
        """Set up test fixtures."""
        self.generator = DivisionWithDecimalsProblemGenerator(
            level=4,
            difficulty=DifficultyLevel.MEDIUM
        )
        self.malrule = DivisionMakesSmallerMalrule()
        self.correct_algo = DivisionCorrectAlgorithm()

    def test_get_available_templates(self):
        """Test that all 10 templates are available."""
        templates = self.generator.get_available_templates()
        self.assertEqual(len(templates), 10)
        expected = ['basic_decimal_division', 'fraction_division',
                    'measurement_context', 'sharing_context', 'rate_context',
                    'time_conversion', 'capacity_division', 'speed_calculation',
                    'recipe_scaling_up', 'unit_conversion']
        for template in expected:
            self.assertIn(template, templates)

    def test_basic_decimal_division_template(self):
        """Test basic_decimal_division template."""
        problem = self.generator.generate(seed=42, template='basic_decimal_division')

        # Check problem structure
        self.assertEqual(problem.operation, 'division')
        self.assertIn('template', problem.metadata)
        self.assertEqual(problem.metadata['template'], 'basic_decimal_division')

        # Check metadata has required fields
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)
        self.assertIn('dividend', problem.metadata)
        self.assertIn('divisor', problem.metadata)
        self.assertIn('problem_type', problem.metadata)
        self.assertEqual(problem.metadata['problem_type'], 'basic_division')

        # Divisor should be less than 1
        self.assertLess(problem.metadata['divisor'], 1)

        # Verify answers are strings
        self.assertIsInstance(problem.metadata['correct_answer'], str)
        self.assertIsInstance(problem.metadata['malrule_answer'], str)

    def test_fraction_division_template(self):
        """Test fraction_division template."""
        problem = self.generator.generate(seed=42, template='fraction_division')

        self.assertEqual(problem.metadata['template'], 'fraction_division')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)
        self.assertIn('fraction_str', problem.metadata)
        self.assertIn('problem_type', problem.metadata)
        self.assertEqual(problem.metadata['problem_type'], 'fraction_division')

        # Should have fraction notation
        self.assertIn('/', problem.metadata['fraction_str'])

    def test_measurement_context_template(self):
        """Test measurement_context template."""
        problem = self.generator.generate(seed=42, template='measurement_context')

        self.assertEqual(problem.metadata['template'], 'measurement_context')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)
        self.assertIn('unit', problem.metadata)
        self.assertIn('problem_type', problem.metadata)
        self.assertEqual(problem.metadata['problem_type'], 'measurement_division')

        # Should have measurement context
        self.assertTrue(
            any(word in problem.text.lower() for word in ['rope', 'board', 'meter', 'feet', 'inch', 'yard', 'segment'])
        )

        # Correct answer should have 'pieces' unit
        self.assertIn('pieces', problem.metadata['correct_answer'])

    def test_sharing_context_template(self):
        """Test sharing_context template."""
        problem = self.generator.generate(seed=42, template='sharing_context')

        self.assertEqual(problem.metadata['template'], 'sharing_context')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)
        self.assertIn('problem_type', problem.metadata)
        self.assertEqual(problem.metadata['problem_type'], 'sharing_division')

        # Should have sharing context
        self.assertTrue(
            any(word in problem.text.lower() for word in ['pizza', 'juice', 'cookie', 'people', 'glass', 'portion'])
        )

    def test_rate_context_template(self):
        """Test rate_context template."""
        problem = self.generator.generate(seed=42, template='rate_context')

        self.assertEqual(problem.metadata['template'], 'rate_context')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)
        self.assertIn('problem_type', problem.metadata)
        self.assertEqual(problem.metadata['problem_type'], 'rate_calculation')

        # Should have price/money context
        self.assertTrue(
            any(word in problem.text.lower() for word in ['$', 'dollar', 'cost', 'spend', 'buy', 'price'])
        )

        # Malrule answer should start with $
        self.assertTrue(problem.metadata['malrule_answer'].startswith('$'))

    def test_time_conversion_template(self):
        """Test time_conversion template."""
        problem = self.generator.generate(seed=42, template='time_conversion')

        self.assertEqual(problem.metadata['template'], 'time_conversion')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)
        self.assertIn('problem_type', problem.metadata)
        self.assertEqual(problem.metadata['problem_type'], 'time_division')

        # Should have time context
        self.assertTrue(
            any(word in problem.text.lower() for word in ['hour', 'shift', 'task', 'workday'])
        )

    def test_capacity_division_template(self):
        """Test capacity_division template."""
        problem = self.generator.generate(seed=42, template='capacity_division')

        self.assertEqual(problem.metadata['template'], 'capacity_division')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)
        self.assertIn('problem_type', problem.metadata)
        self.assertEqual(problem.metadata['problem_type'], 'capacity_calculation')

        # Should have capacity context
        self.assertTrue(
            any(word in problem.text.lower() for word in ['liter', 'bottle', 'container', 'tank'])
        )

    def test_speed_calculation_template(self):
        """Test speed_calculation template."""
        problem = self.generator.generate(seed=42, template='speed_calculation')

        self.assertEqual(problem.metadata['template'], 'speed_calculation')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)
        self.assertIn('problem_type', problem.metadata)
        self.assertEqual(problem.metadata['problem_type'], 'speed_calculation')
        self.assertIn('distance', problem.metadata)
        self.assertIn('time', problem.metadata)

        # Should have speed context
        self.assertTrue(
            any(word in problem.text.lower() for word in ['speed', 'travel', 'car', 'cover'])
        )

    def test_recipe_scaling_up_template(self):
        """Test recipe_scaling_up template."""
        problem = self.generator.generate(seed=42, template='recipe_scaling_up')

        self.assertEqual(problem.metadata['template'], 'recipe_scaling_up')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)
        self.assertIn('problem_type', problem.metadata)
        self.assertEqual(problem.metadata['problem_type'], 'recipe_scaling')
        self.assertIn('unit', problem.metadata)

        # Should have recipe context
        self.assertTrue(
            any(word in problem.text.lower() for word in ['recipe', 'batch', 'portion'])
        )

    def test_unit_conversion_template(self):
        """Test unit_conversion template."""
        problem = self.generator.generate(seed=42, template='unit_conversion')

        self.assertEqual(problem.metadata['template'], 'unit_conversion')
        self.assertIn('correct_answer', problem.metadata)
        self.assertIn('malrule_answer', problem.metadata)
        self.assertIn('problem_type', problem.metadata)
        self.assertEqual(problem.metadata['problem_type'], 'unit_conversion')
        self.assertIn('from_unit', problem.metadata)
        self.assertIn('to_unit', problem.metadata)

        # Should have conversion context
        self.assertTrue(
            any(word in problem.text.lower() for word in ['convert', 'unit', 'meter', 'kilogram', 'feet'])
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
                    # Has unit like "7.5 meters" or "16 pieces"
                    metadata_numeric = metadata_answer.split()[0]
                else:
                    metadata_numeric = metadata_answer

                # Compare as floats (allowing small precision differences)
                self.assertAlmostEqual(float(expected), float(metadata_numeric), places=2,
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

                # Answers should be different
                self.assertNotEqual(malrule_answer, correct_answer,
                                  f"Malrule and correct should differ for {template}")

    def test_specific_example_4_div_0_5(self):
        """Test the classic example: 4 ÷ 0.5 = 2 (malrule) vs 8 (correct)."""
        # 4 ÷ 0.5:
        # Correct: 4 ÷ 0.5 = 8 (because 0.5 fits into 4 eight times)
        # Malrule: 8 > 4, so switch to multiplication: 4 × 0.5 = 2
        problem = Problem(
            text="What is 4 ÷ 0.5?",
            operands=[4.0, 0.5],
            operation='division',
            level=4,
            difficulty=DifficultyLevel.MEDIUM,
            metadata={
                'dividend': 4.0,
                'divisor': 0.5,
                'correct_answer': '8.00',
                'malrule_answer': '2.00',
                'template': 'basic_decimal_division'
            }
        )

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        # Correct: 8.00
        self.assertEqual(correct_solution.answer, '8.00')

        # Malrule: 2.00 (switched to multiplication instead)
        self.assertEqual(malrule_solution.answer, '2.00')

    def test_specific_example_6_div_one_half(self):
        """Test fraction example: 6 ÷ 1/2 = 3 (malrule) vs 12 (correct)."""
        # 6 ÷ 1/2:
        # Correct: 6 ÷ 0.5 = 12
        # Malrule: 12 > 6, so switch to multiplication: 6 × 0.5 = 3
        problem = Problem(
            text="What is 6 ÷ 1/2?",
            operands=[6.0, 0.5],
            operation='division',
            level=4,
            difficulty=DifficultyLevel.MEDIUM,
            metadata={
                'dividend': 6.0,
                'divisor': 0.5,
                'fraction_str': '1/2',
                'numerator': 1,
                'denominator': 2,
                'correct_answer': '12.00',
                'malrule_answer': '3.00',
                'template': 'fraction_division'
            }
        )

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        # Correct: 12.00
        self.assertEqual(correct_solution.answer, '12.00')

        # Malrule: 3.00 (switched to multiplication)
        self.assertEqual(malrule_solution.answer, '3.00')

    def test_backwards_compatibility(self):
        """Test that old problems without metadata still work."""
        # Create old-style problem without template metadata
        old_problem = Problem(
            text="What is 10 ÷ 0.5?",
            operands=[10.0, 0.5],
            operation='division',
            level=4,
            difficulty=DifficultyLevel.MEDIUM,
            metadata={
                'dividend': 10.0,
                'divisor': 0.5
            }
        )

        # Should still work
        malrule_solution = self.malrule.solve(old_problem)
        correct_solution = self.correct_algo.solve(old_problem)

        self.assertIsInstance(malrule_solution.answer, str)
        self.assertIsInstance(correct_solution.answer, str)

        # Verify logic: 10 ÷ 0.5 = 20 (correct), so malrule switches to multiplication
        # Malrule: 10 × 0.5 = 5.00 (formatted to 2 decimals)
        self.assertEqual(malrule_solution.answer, '5.00')
        self.assertEqual(correct_solution.answer, '20.00')

    def test_malrule_behavior_divisor_less_than_one(self):
        """Test that malrule uses multiplication when divisor < 1 (triggers misconception)."""
        problem = self.generator.generate(seed=100, template='basic_decimal_division')

        dividend = problem.metadata['dividend']
        divisor = problem.metadata['divisor']

        # Divisor should be less than 1
        self.assertLess(divisor, 1)

        # Get solutions
        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        # Correct answer: dividend / divisor (should be larger than dividend)
        correct_quotient = dividend / divisor
        self.assertGreater(correct_quotient, dividend)

        # Malrule should use multiplication: dividend * divisor
        expected_malrule = dividend * divisor

        # Extract numeric part of malrule answer
        malrule_answer = malrule_solution.answer
        if malrule_answer.startswith('$'):
            malrule_answer = malrule_answer[1:]

        self.assertEqual(float(malrule_answer), round(expected_malrule, 2))

    def test_unit_stripping_in_calculate_expected_answer(self):
        """Test that calculate_expected_answer properly strips units."""
        # Test with measurement context (has unit like "7.5 meters")
        problem_measurement = self.generator.generate(seed=50, template='measurement_context')
        expected = self.malrule.calculate_expected_answer(problem_measurement)

        # Should be numeric only, no units
        self.assertFalse(any(unit in expected for unit in ['meters', 'feet', 'inches', 'yards', 'pieces']))

        # Test with rate context (has $ sign)
        problem_rate = self.generator.generate(seed=51, template='rate_context')
        expected_rate = self.malrule.calculate_expected_answer(problem_rate)

        # Should not start with $
        self.assertFalse(expected_rate.startswith('$'))

        # Should be a valid number
        float(expected)
        float(expected_rate)



class TestDivisionMakesSmallerAutomated(unittest.TestCase):
    """Automated test suite runner."""

    def test_automated_suite(self):
        """Run the automated test suite."""
        problem_gen = DivisionWithDecimalsProblemGenerator(
            level=5,
            difficulty=DifficultyLevel.MEDIUM
        )
        malrule = DivisionMakesSmallerMalrule()
        correct = DivisionCorrectAlgorithm()

        test_suite = MalruleTest(malrule, correct, problem_gen)
        results = test_suite.run_all_tests(verbose=False)

        all_passed = all(r.passed for r in results)
        self.assertTrue(all_passed,
                       f"Automated tests failed: {[r.message for r in results if not r.passed]}")


def main():
    """Main entry point for standalone execution."""
    print("\n╔" + "═"*68 + "╗")
    print("║" + "  VERIFICATION TEST: Division Makes Smaller  ".center(70) + "║")
    print("╚" + "═"*68 + "╝\n")

    # Run unittest
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestDivisionMakesSmaller))
    suite.addTests(loader.loadTestsFromTestCase(TestDivisionMakesSmallerAutomated))

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
