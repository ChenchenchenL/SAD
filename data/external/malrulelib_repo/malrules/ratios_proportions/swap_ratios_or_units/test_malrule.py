#!/usr/bin/env python3
"""Test script for Swap-Ratios-Or-Units malrule."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.ratios_proportions.swap_ratios_or_units import (
    SwapRatiosOrUnitsProblemGenerator,
    SwapRatiosOrUnitsMalrule,
    ProportionSetupCorrectAlgorithm
)


class SameAnswerException(Exception):
    """Exception raised when malrule produces the same answer as correct algorithm."""
    pass


def print_steps(title, steps):
    """Print steps with proper formatting."""
    print(f"\n{title}:")
    print("-" * 50)
    for step in steps:
        print(f"  {step}")
    print("-" * 50)


def test_single_problem(problem, correct, malrule, test_name, expected_correct=None, expected_malrule=None):
    """
    Test a single problem and print results.

    Args:
        problem: The Problem instance to test
        correct: The correct algorithm instance
        malrule: The malrule algorithm instance
        test_name: Name of the test for display
        expected_correct: Expected correct answer (optional, for validation)
        expected_malrule: Expected malrule answer (optional, for validation)

    Returns:
        True if test passed, False otherwise
    """
    correct_sol = correct.solve(problem)
    malrule_sol = malrule.solve(problem)

    # Check for edge case: malrule produces same answer as correct
    if abs(correct_sol.answer - malrule_sol.answer) < 0.001:
        print(f"\n{'='*70}")
        print(f"EDGE CASE DETECTED: {test_name}")
        print(f"{'='*70}")
        print(f"Problem: {problem.text}")
        print(f"Correct Answer: {correct_sol.answer}")
        print(f"Malrule Answer: {malrule_sol.answer}")
        print_steps("Correct Algorithm Steps", correct_sol.steps)
        print_steps("Malrule Algorithm Steps", malrule_sol.steps)
        raise SameAnswerException(
            f"Malrule produced same answer as correct algorithm ({correct_sol.answer}). "
            "This indicates the problem values don't effectively distinguish the misconception."
        )

    # Verify expected values if provided
    passed = True
    error_messages = []

    if expected_correct is not None:
        if abs(correct_sol.answer - expected_correct) > 0.01:
            passed = False
            error_messages.append(f"Correct answer mismatch: got {correct_sol.answer}, expected {expected_correct}")

    if expected_malrule is not None:
        if abs(malrule_sol.answer - expected_malrule) > 0.01:
            passed = False
            error_messages.append(f"Malrule answer mismatch: got {malrule_sol.answer}, expected {expected_malrule}")

    if passed:
        print(f"{test_name}: Correct=${correct_sol.answer}, Malrule=${malrule_sol.answer} ... PASSED")
        return True
    else:
        print(f"\n{'='*70}")
        print(f"TEST FAILED: {test_name}")
        print(f"{'='*70}")
        print(f"Problem: {problem.text}")
        for msg in error_messages:
            print(f"ERROR: {msg}")
        print_steps("Correct Algorithm Steps", correct_sol.steps)
        print_steps("Malrule Algorithm Steps", malrule_sol.steps)
        return False


def test_basic_cost_quantity():
    """Test basic cost/quantity proportion problems."""
    print("\n" + "="*70)
    print("TESTING BASIC COST/QUANTITY PROBLEMS")
    print("="*70)

    malrule = SwapRatiosOrUnitsMalrule()
    correct = ProportionSetupCorrectAlgorithm()

    # Test case 1: 3 items for $6, how much for 5 items?
    # Correct: 3/6 = 5/x → x = 10
    # Malrule: 3/6 = x/5 → x = 2.5
    problem1 = Problem(
        text="If 3 items cost $6, how much do 5 items cost?",
        operands=[3, 6, 5],
        operation='proportion_setup',
        level=7,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'problem_type': 'basic_cost_quantity',
            'quantity1': 3,
            'cost1': 6,
            'quantity2': 5,
            'correct_answer': 10.0,
            'malrule_answer': 2.5
        }
    )

    if not test_single_problem(problem1, correct, malrule, "TEST 1: 3 items/$6 → 5 items", 10.0, 2.5):
        return False

    # Test case 2: 2 items for $8, how much for 6 items?
    problem2 = Problem(
        text="If 2 items cost $8, how much do 6 items cost?",
        operands=[2, 8, 6],
        operation='proportion_setup',
        level=7,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'problem_type': 'basic_cost_quantity',
            'quantity1': 2,
            'cost1': 8,
            'quantity2': 6,
            'correct_answer': 24.0,
            'malrule_answer': 1.5
        }
    )

    if not test_single_problem(problem2, correct, malrule, "TEST 2: 2 items/$8 → 6 items", 24.0, 1.5):
        return False

    # Test case 3: 4 items for $10, how much for 7 items?
    problem3 = Problem(
        text="If 4 items cost $10, how much do 7 items cost?",
        operands=[4, 10, 7],
        operation='proportion_setup',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'problem_type': 'basic_cost_quantity',
            'quantity1': 4,
            'cost1': 10,
            'quantity2': 7,
            'correct_answer': 17.5,
            'malrule_answer': 2.8
        }
    )

    if not test_single_problem(problem3, correct, malrule, "TEST 3: 4 items/$10 → 7 items", 17.5, 2.8):
        return False

    # Test case 4: 5 items for $15, how much for 8 items?
    problem4 = Problem(
        text="If 5 items cost $15, how much do 8 items cost?",
        operands=[5, 15, 8],
        operation='proportion_setup',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'problem_type': 'basic_cost_quantity',
            'quantity1': 5,
            'cost1': 15,
            'quantity2': 8,
            'correct_answer': 24.0,
            'malrule_answer': 2.67
        }
    )

    if not test_single_problem(problem4, correct, malrule, "TEST 4: 5 items/$15 → 8 items", 24.0, 2.67):
        return False

    print("\nAll basic cost/quantity tests PASSED")
    return True


def test_speed_time_distance():
    """Test speed/time/distance proportion problems."""
    print("\n" + "="*70)
    print("TESTING SPEED/TIME/DISTANCE PROBLEMS")
    print("="*70)

    malrule = SwapRatiosOrUnitsMalrule()
    correct = ProportionSetupCorrectAlgorithm()

    # Test: Car traveling 60 miles in 2 hours, how far in 3 hours?
    # Correct: 60/2 = x/3 → x = 90
    # Malrule: 60/2 = 3/x → x = (2*3)/60 = 0.1
    problem = Problem(
        text="A car travels 60 miles in 2 hours. At the same speed, how far will it travel in 3 hours?",
        operands=[60, 2, 3],
        operation='speed_proportion',
        level=7,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'problem_type': 'speed_time_distance',
            'distance1': 60,
            'time1': 2,
            'time2': 3,
            'correct_answer': 90.0,
            'malrule_answer': 0.1
        }
    )

    if not test_single_problem(problem, correct, malrule, "Speed/Time/Distance: 60mi/2hr → 3hr", 90.0, 0.1):
        return False

    # Additional test case
    problem2 = Problem(
        text="A car travels 80 miles in 4 hours. At the same speed, how far will it travel in 5 hours?",
        operands=[80, 4, 5],
        operation='speed_proportion',
        level=7,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'problem_type': 'speed_time_distance',
            'distance1': 80,
            'time1': 4,
            'time2': 5,
            'correct_answer': 100.0,  # (80 * 5) / 4 = 100
            'malrule_answer': 0.25    # (4 * 5) / 80 = 0.25
        }
    )

    if not test_single_problem(problem2, correct, malrule, "Speed/Time/Distance: 80mi/4hr → 5hr", 100.0, 0.25):
        return False

    print("\nAll speed/time/distance tests PASSED")
    return True


def test_recipe_scaling():
    """Test recipe scaling proportion problems."""
    print("\n" + "="*70)
    print("TESTING RECIPE SCALING PROBLEMS")
    print("="*70)

    malrule = SwapRatiosOrUnitsMalrule()
    correct = ProportionSetupCorrectAlgorithm()

    # Test: 2 cups flour for 8 servings, need 12 servings
    # Correct: 2/8 = x/12 → x = 3
    # Malrule: 2/8 = 12/x → x = (8*12)/2 = 48
    problem = Problem(
        text="A recipe for 8 servings calls for 2 cups of flour. How much do you need for 12 servings?",
        operands=[2, 8, 12],
        operation='recipe_proportion',
        level=7,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'problem_type': 'recipe_scaling',
            'ingredient_amount': 2,
            'servings1': 8,
            'servings2': 12,
            'ingredient_name': 'cups of flour',
            'correct_answer': 3.0,
            'malrule_answer': 48.0
        }
    )

    if not test_single_problem(problem, correct, malrule, "Recipe: 2 cups/8 servings → 12 servings", 3.0, 48.0):
        return False

    # Additional test case
    problem2 = Problem(
        text="A recipe for 6 servings calls for 3 eggs. How many do you need for 10 servings?",
        operands=[3, 6, 10],
        operation='recipe_proportion',
        level=7,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'problem_type': 'recipe_scaling',
            'ingredient_amount': 3,
            'servings1': 6,
            'servings2': 10,
            'ingredient_name': 'eggs',
            'correct_answer': 5.0,     # (3 * 10) / 6 = 5
            'malrule_answer': 20.0     # (6 * 10) / 3 = 20
        }
    )

    if not test_single_problem(problem2, correct, malrule, "Recipe: 3 eggs/6 servings → 10 servings", 5.0, 20.0):
        return False

    print("\nAll recipe scaling tests PASSED")
    return True


def test_map_scale():
    """Test map scale proportion problems."""
    print("\n" + "="*70)
    print("TESTING MAP SCALE PROBLEMS")
    print("="*70)

    malrule = SwapRatiosOrUnitsMalrule()
    correct = ProportionSetupCorrectAlgorithm()

    # Test: 2cm = 50km, how many cm for 100km?
    # Correct: 2/50 = x/100 → x = 4
    # Malrule: 2/50 = 100/x → x = (50*100)/2 = 2500
    problem = Problem(
        text="On a map, 2 cm represents 50 km. How many cm on the map would represent 100 km?",
        operands=[2, 50, 100],
        operation='map_scale_proportion',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'problem_type': 'map_scale',
            'map_dist1': 2,
            'actual_dist1': 50,
            'actual_dist2': 100,
            'correct_answer': 4.0,
            'malrule_answer': 2500.0
        }
    )

    if not test_single_problem(problem, correct, malrule, "Map Scale: 2cm/50km → 100km", 4.0, 2500.0):
        return False

    # Additional test case
    problem2 = Problem(
        text="On a map, 3 cm represents 75 km. How many cm on the map would represent 150 km?",
        operands=[3, 75, 150],
        operation='map_scale_proportion',
        level=8,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'problem_type': 'map_scale',
            'map_dist1': 3,
            'actual_dist1': 75,
            'actual_dist2': 150,
            'correct_answer': 6.0,      # (3 * 150) / 75 = 6
            'malrule_answer': 3750.0    # (75 * 150) / 3 = 3750
        }
    )

    if not test_single_problem(problem2, correct, malrule, "Map Scale: 3cm/75km → 150km", 6.0, 3750.0):
        return False

    print("\nAll map scale tests PASSED")
    return True


def test_density_volume_mass():
    """Test density (mass/volume) proportion problems."""
    print("\n" + "="*70)
    print("TESTING DENSITY (MASS/VOLUME) PROBLEMS")
    print("="*70)

    malrule = SwapRatiosOrUnitsMalrule()
    correct = ProportionSetupCorrectAlgorithm()

    # Test: 200g in 50mL, what mass for 100mL?
    # Correct: 200/50 = x/100 → x = 400
    # Malrule: 200/50 = 100/x → x = (50*100)/200 = 25
    problem = Problem(
        text="A substance has a mass of 200 grams in 50 mL. What mass would 100 mL of the same substance have?",
        operands=[200, 50, 100],
        operation='density_proportion',
        level=8,
        difficulty=DifficultyLevel.HARD,
        metadata={
            'problem_type': 'density_volume_mass',
            'mass1': 200,
            'volume1': 50,
            'volume2': 100,
            'mass_unit': 'grams',
            'volume_unit': 'mL',
            'correct_answer': 400.0,
            'malrule_answer': 25.0
        }
    )

    if not test_single_problem(problem, correct, malrule, "Density: 200g/50mL → 100mL", 400.0, 25.0):
        return False

    # Additional test case
    problem2 = Problem(
        text="A substance has a mass of 300 grams in 100 cm3. What mass would 150 cm3 of the same substance have?",
        operands=[300, 100, 150],
        operation='density_proportion',
        level=8,
        difficulty=DifficultyLevel.HARD,
        metadata={
            'problem_type': 'density_volume_mass',
            'mass1': 300,
            'volume1': 100,
            'volume2': 150,
            'mass_unit': 'grams',
            'volume_unit': 'cm3',
            'correct_answer': 450.0,    # (300 * 150) / 100 = 450
            'malrule_answer': 50.0      # (100 * 150) / 300 = 50
        }
    )

    if not test_single_problem(problem2, correct, malrule, "Density: 300g/100cm3 → 150cm3", 450.0, 50.0):
        return False

    print("\nAll density tests PASSED")
    return True


def test_template_generation():
    """Test that all problem templates can be generated and solved."""
    print("\n" + "="*70)
    print("TESTING TEMPLATE GENERATION")
    print("="*70)

    generator = SwapRatiosOrUnitsProblemGenerator(
        level=7,
        difficulty=DifficultyLevel.MEDIUM
    )

    malrule = SwapRatiosOrUnitsMalrule()
    correct = ProportionSetupCorrectAlgorithm()

    # Expected template types for level 7+
    expected_templates = {
        'basic_cost_quantity',
        'speed_time_distance',
        'recipe_scaling',
        'map_scale',
        'density_volume_mass'
    }

    # Generate problems and track which templates appear
    template_counts = {}
    generated_problems = []

    for i in range(100):  # Generate enough to hit all templates
        problem = generator.generate(seed=1000 + i)
        problem_type = problem.metadata.get('problem_type', 'basic_cost_quantity')
        template_counts[problem_type] = template_counts.get(problem_type, 0) + 1

        # Store first problem of each type
        if problem_type not in [p.metadata.get('problem_type') for p in generated_problems]:
            generated_problems.append(problem)

    print(f"\nGenerated template distribution:")
    for template, count in sorted(template_counts.items()):
        print(f"  {template}: {count} problems")

    # Verify we found all expected templates
    found_templates = set(template_counts.keys())
    missing_templates = expected_templates - found_templates
    if missing_templates:
        print(f"\nWARNING: Missing templates: {missing_templates}")
        # This is not necessarily a failure - basic_cost_quantity is always available
        # but others require level >= 7

    # Test each generated template type
    print("\nTesting each template type:")
    all_passed = True

    for problem in generated_problems:
        problem_type = problem.metadata.get('problem_type', 'basic_cost_quantity')

        try:
            correct_sol = correct.solve(problem)
            malrule_sol = malrule.solve(problem)

            # Check for edge case
            if abs(correct_sol.answer - malrule_sol.answer) < 0.001:
                print(f"\n  {problem_type}: EDGE CASE - same answer!")
                print_steps("Correct Steps", correct_sol.steps)
                print_steps("Malrule Steps", malrule_sol.steps)
                all_passed = False
                continue

            print(f"  {problem_type}: Correct={correct_sol.answer}, Malrule={malrule_sol.answer} ... OK")

        except Exception as e:
            print(f"\n  {problem_type}: ERROR - {e}")
            all_passed = False

    if all_passed:
        print("\nAll template generation tests PASSED")
    else:
        print("\nSome template generation tests FAILED")

    return all_passed


def test_edge_case_detection():
    """Test that edge cases (same answer) are properly detected."""
    print("\n" + "="*70)
    print("TESTING EDGE CASE DETECTION")
    print("="*70)

    malrule = SwapRatiosOrUnitsMalrule()
    correct = ProportionSetupCorrectAlgorithm()

    # This problem would produce same answer if values were chosen poorly
    # Let's verify our formulas don't accidentally produce same answers

    # For basic_cost_quantity with q1=2, c1=4, q2=4:
    # Correct: (4 * 4) / 2 = 8
    # Malrule: (2 * 4) / 4 = 2
    # Different - good!

    # Edge case that WOULD be same (if we had it): q1=c1=q2
    # With q1=3, c1=3, q2=3:
    # Correct: (3 * 3) / 3 = 3
    # Malrule: (3 * 3) / 3 = 3
    # Same! This is an edge case.

    edge_problem = Problem(
        text="If 3 items cost $3, how much do 3 items cost?",
        operands=[3, 3, 3],
        operation='proportion_setup',
        level=7,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'problem_type': 'basic_cost_quantity',
            'quantity1': 3,
            'cost1': 3,
            'quantity2': 3,
            'correct_answer': 3.0,
            'malrule_answer': 3.0
        }
    )

    try:
        test_single_problem(edge_problem, correct, malrule, "Edge Case Test")
        print("ERROR: Edge case was not detected!")
        return False
    except SameAnswerException as e:
        print(f"Edge case properly detected: {e}")
        print("Edge case detection test PASSED")
        return True


def test_automated_suite():
    """Run the automated test suite."""
    print("\n" + "="*70)
    print("RUNNING AUTOMATED TEST SUITE")
    print("="*70)

    problem_gen = SwapRatiosOrUnitsProblemGenerator(
        level=7,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = SwapRatiosOrUnitsMalrule()
    correct = ProportionSetupCorrectAlgorithm()

    test_suite = MalruleTest(malrule, correct, problem_gen)
    results = test_suite.run_all_tests(verbose=True)

    all_passed = all(r.passed for r in results)
    if all_passed:
        print("\nAll automated tests PASSED")
    return all_passed


def main():
    print("\n" + "="*70)
    print("  VERIFICATION TEST: Swap-Ratios-Or-Units  ".center(70))
    print("="*70 + "\n")

    all_passed = True

    try:
        # Test each problem template type
        if not test_basic_cost_quantity():
            all_passed = False

        if not test_speed_time_distance():
            all_passed = False

        if not test_recipe_scaling():
            all_passed = False

        if not test_map_scale():
            all_passed = False

        if not test_density_volume_mass():
            all_passed = False

        # Test template generation
        if not test_template_generation():
            all_passed = False

        # Test edge case detection
        if not test_edge_case_detection():
            all_passed = False

        # Run automated suite
        if not test_automated_suite():
            all_passed = False

        print("\n" + "="*70)
        if all_passed:
            print("  ALL TESTS PASSED  ".center(70))
        else:
            print("  SOME TESTS FAILED  ".center(70))
        print("="*70 + "\n")

        return 0 if all_passed else 1

    except Exception as e:
        print(f"\nTEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
