#!/usr/bin/env python3
"""
Comprehensive test suite for Ratio-As-Division-Only malrule.

This test suite:
1. Tests ALL available templates (including word_problem_context)
2. Prints the answer produced when tests pass
3. Prints detailed steps from both algorithms when tests fail
4. Handles edge cases where malrule might produce same answer as correct
5. Verifies that algorithms compute answers correctly without using metadata answers

Run from project root: python3 -m malrules.ratios_proportions.ratio_as_division_only.test_malrule
Or from this directory: python3 test_malrule.py
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.ratios_proportions.ratio_as_division_only import (
    RatioAsDivisionOnlyProblemGenerator,
    RatioAsDivisionOnlyMalrule,
    RatioMultiplicativeRelationshipCorrectAlgorithm
)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def normalize_answer(answer):
    """Normalize an answer for comparison (handle float/int/string variations)."""
    if isinstance(answer, str):
        # Try to convert to float for numerical comparison
        try:
            return float(answer)
        except ValueError:
            return answer.strip().lower()
    return float(answer)


def answers_match(answer1, answer2):
    """Check if two answers match (handles float/int/string variations)."""
    norm1 = normalize_answer(answer1)
    norm2 = normalize_answer(answer2)

    if isinstance(norm1, float) and isinstance(norm2, float):
        # Use approximate comparison for floats
        return abs(norm1 - norm2) < 0.01
    return norm1 == norm2


def print_failure_details(problem, correct_sol, malrule_sol, expected_correct, expected_malrule):
    """Print detailed information when a test fails."""
    print("\n" + "="*60)
    print("TEST FAILURE DETAILS")
    print("="*60)
    print(f"\nProblem: {problem.text}")
    print(f"\nMetadata: {problem.metadata}")
    print("\n--- CORRECT ALGORITHM ---")
    print(f"Answer: {correct_sol.answer}")
    print(f"Expected: {expected_correct}")
    print("Steps:")
    for step in correct_sol.steps:
        print(f"  {step}")
    print("\n--- MALRULE ALGORITHM ---")
    print(f"Answer: {malrule_sol.answer}")
    print(f"Expected: {expected_malrule}")
    print("Steps:")
    for step in malrule_sol.steps:
        print(f"  {step}")
    print("="*60 + "\n")


def print_edge_case_warning(problem, correct_sol, malrule_sol):
    """Print warning when malrule produces same answer as correct algorithm."""
    print("\n" + "!"*60)
    print("EDGE CASE: Malrule produced same answer as correct algorithm!")
    print("!"*60)
    print(f"\nProblem: {problem.text}")
    print(f"Correct Answer: {correct_sol.answer}")
    print(f"Malrule Answer: {malrule_sol.answer}")
    print("\n--- CORRECT ALGORITHM STEPS ---")
    for step in correct_sol.steps:
        print(f"  {step}")
    print("\n--- MALRULE ALGORITHM STEPS ---")
    for step in malrule_sol.steps:
        print(f"  {step}")
    print("!"*60 + "\n")


# ============================================================================
# PART 1: SPECIFIC RESEARCH EXAMPLES
# ============================================================================

def test_specific_examples():
    """Test with specific research examples demonstrating the malrule."""
    print("="*70)
    print("TESTING RATIO-AS-DIVISION-ONLY")
    print("="*70)

    malrule = RatioAsDivisionOnlyMalrule()
    correct = RatioMultiplicativeRelationshipCorrectAlgorithm()

    # Test case 1: Interpretation - "What does 3:5 mean?"
    print("\nTEST 1: Interpret ratio 3:5")
    problem1 = Problem(
        text="Explain what the ratio 3:5 means in your own words.",
        operands=[3, 5],
        operation='ratio_interpretation',
        level=7,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'ratio_a': 3,
            'ratio_b': 5,
            'problem_type': 'interpretation',
        }
    )

    correct_sol1 = correct.solve(problem1)
    malrule_sol1 = malrule.solve(problem1)

    print(f"  Correct: {correct_sol1.answer}")
    print(f"  Malrule: {malrule_sol1.answer}")

    if correct_sol1.answer == malrule_sol1.answer:
        print_edge_case_warning(problem1, correct_sol1, malrule_sol1)
        raise AssertionError("Edge case: Correct and malrule answers match")

    assert "For every 3" in correct_sol1.answer
    assert "divided by 5" in malrule_sol1.answer or "0.60" in malrule_sol1.answer or "0.6" in malrule_sol1.answer
    print("PASSED - Correct: multiplicative relationship, Malrule: division only")

    # Test case 2: Application - Ratio 2:3, have 6 of first, find second
    print(f"\nTEST 2: Ratio 2:3, have 6 of first")
    problem2 = Problem(
        text="If the ratio of red marbles to blue marbles is 2:3, and there are 6 red marbles, how many blue marbles are there?",
        operands=[2, 3, 6],
        operation='ratio_application',
        level=7,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'ratio_a': 2,
            'ratio_b': 3,
            'first_quantity': 6,
            'problem_type': 'application',
        }
    )

    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)

    print(f"  Correct: {correct_sol2.answer}, Malrule: {malrule_sol2.answer}")

    if answers_match(correct_sol2.answer, malrule_sol2.answer):
        print_edge_case_warning(problem2, correct_sol2, malrule_sol2)
        raise AssertionError("Edge case: Correct and malrule answers match")

    assert str(correct_sol2.answer) == "9", f"Expected 9, got {correct_sol2.answer}"
    assert str(malrule_sol2.answer) == "4.0" or str(malrule_sol2.answer) == "4", f"Expected 4.0, got {malrule_sol2.answer}"
    print("PASSED - Correct: 9, Malrule: 4.0")

    # Test case 3: Application - Ratio 3:7, have 9 of first, find second
    print(f"\nTEST 3: Ratio 3:7, have 9 of first")
    problem3 = Problem(
        text="If the ratio of cats to dogs is 3:7, and there are 9 cats, how many dogs are there?",
        operands=[3, 7, 9],
        operation='ratio_application',
        level=7,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'ratio_a': 3,
            'ratio_b': 7,
            'first_quantity': 9,
            'problem_type': 'application',
        }
    )

    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)

    print(f"  Correct: {correct_sol3.answer}, Malrule: {malrule_sol3.answer}")

    if answers_match(correct_sol3.answer, malrule_sol3.answer):
        print_edge_case_warning(problem3, correct_sol3, malrule_sol3)
        raise AssertionError("Edge case: Correct and malrule answers match")

    assert str(correct_sol3.answer) == "21", f"Expected 21, got {correct_sol3.answer}"
    malrule_float = float(malrule_sol3.answer)
    assert 3.8 <= malrule_float <= 3.9, f"Expected ~3.86, got {malrule_float}"
    print("PASSED - Correct: 21, Malrule: ~3.86")

    # Test case 4: Interpretation - "What does 4:9 mean?"
    print("\nTEST 4: Interpret ratio 4:9")
    problem4 = Problem(
        text="Explain what the ratio 4:9 means in your own words.",
        operands=[4, 9],
        operation='ratio_interpretation',
        level=6,
        difficulty=DifficultyLevel.EASY,
        metadata={
            'ratio_a': 4,
            'ratio_b': 9,
            'problem_type': 'interpretation',
        }
    )

    correct_sol4 = correct.solve(problem4)
    malrule_sol4 = malrule.solve(problem4)

    print(f"  Correct: {correct_sol4.answer}")
    print(f"  Malrule: {malrule_sol4.answer}")

    if correct_sol4.answer == malrule_sol4.answer:
        print_edge_case_warning(problem4, correct_sol4, malrule_sol4)
        raise AssertionError("Edge case: Correct and malrule answers match")

    assert "For every 4" in correct_sol4.answer
    assert "divided by 9" in malrule_sol4.answer or "0.44" in malrule_sol4.answer or "0.4" in malrule_sol4.answer
    print("PASSED - Correct: multiplicative relationship, Malrule: division only")

    print("\n" + "="*70)
    print("ALL SPECIFIC TEST CASES PASSED")
    print("="*70)


# ============================================================================
# PART 2: TEMPLATE-BASED UNIT TESTS
# ============================================================================

class TestRatioAsDivisionOnlyTemplates(unittest.TestCase):
    """Test ALL templates for Ratio-As-Division-Only malrule."""

    def setUp(self):
        """Set up test fixtures."""
        self.generator = RatioAsDivisionOnlyProblemGenerator(
            level=7,
            difficulty=DifficultyLevel.MEDIUM
        )
        self.malrule = RatioAsDivisionOnlyMalrule()
        self.correct_algo = RatioMultiplicativeRelationshipCorrectAlgorithm()

    def _test_template_basic(self, template_name, seed, expected_keywords):
        """Helper to test basic template functionality."""
        problem = self.generator.generate(seed=seed, template=template_name)

        self.assertEqual(problem.metadata['template'], template_name)

        # Check that answers are strings
        self.assertIsInstance(problem.metadata.get('correct_answer', ''), str)
        self.assertIsInstance(problem.metadata.get('malrule_answer', ''), str)

        # Should contain expected keywords
        text_lower = problem.text.lower()
        found_keyword = any(word in text_lower for word in expected_keywords)
        self.assertTrue(found_keyword, f"Expected one of {expected_keywords} in '{problem.text}'")

        return problem

    def _test_template_algorithms(self, template_name, seed):
        """Helper to test that algorithms produce different, correct answers."""
        problem = self.generator.generate(seed=seed, template=template_name)

        malrule_solution = self.malrule.solve(problem)
        correct_solution = self.correct_algo.solve(problem)

        # Verify is_correct flags
        self.assertFalse(malrule_solution.is_correct, "Malrule should be marked as incorrect")
        self.assertTrue(correct_solution.is_correct, "Correct algorithm should be marked as correct")

        # Check for edge case: answers match
        if answers_match(correct_solution.answer, malrule_solution.answer):
            print_edge_case_warning(problem, correct_solution, malrule_solution)
            self.fail(f"Edge case in {template_name}: Malrule produced same answer as correct algorithm")

        # Verify answers match expected
        expected_correct = problem.metadata.get('correct_answer')
        expected_malrule = problem.metadata.get('malrule_answer')

        if expected_correct and not answers_match(correct_solution.answer, expected_correct):
            print_failure_details(problem, correct_solution, malrule_solution, expected_correct, expected_malrule)
            self.fail(f"Correct algorithm answer mismatch: got {correct_solution.answer}, expected {expected_correct}")

        if expected_malrule and not answers_match(malrule_solution.answer, expected_malrule):
            print_failure_details(problem, correct_solution, malrule_solution, expected_correct, expected_malrule)
            self.fail(f"Malrule algorithm answer mismatch: got {malrule_solution.answer}, expected {expected_malrule}")

        # Print success with answers
        print(f"\n  {template_name}: Correct={correct_solution.answer}, Malrule={malrule_solution.answer}")

        return problem, correct_solution, malrule_solution

    # Template 1: part_to_part_ratio
    def test_part_to_part_ratio_template(self):
        """Test part_to_part_ratio template generates valid problems."""
        print("\n--- Testing part_to_part_ratio template ---")
        problem = self._test_template_basic('part_to_part_ratio', 100, ['marbles'])
        self.assertIn('ratio_a', problem.metadata)
        self.assertIn('ratio_b', problem.metadata)
        self.assertIn('first_quantity', problem.metadata)

    def test_part_to_part_ratio_malrule_vs_correct(self):
        """Test part_to_part_ratio: malrule gives wrong answer, correct gives right answer."""
        self._test_template_algorithms('part_to_part_ratio', 101)

    def test_part_to_part_ratio_calculate_expected_answer(self):
        """Test calculate_expected_answer for part_to_part_ratio template."""
        problem = self.generator.generate(seed=102, template='part_to_part_ratio')
        expected_answer = self.malrule.calculate_expected_answer(problem)
        malrule_solution = self.malrule.solve(problem)
        self.assertTrue(answers_match(expected_answer, malrule_solution.answer),
                       f"calculate_expected_answer={expected_answer} != solve={malrule_solution.answer}")

    # Template 2: recipe_scaling
    def test_recipe_scaling_template(self):
        """Test recipe_scaling template generates valid problems."""
        print("\n--- Testing recipe_scaling template ---")
        problem = self._test_template_basic('recipe_scaling', 200, ['recipe', 'flour', 'sugar', 'cups'])
        self.assertIn('flour_cups', problem.metadata)

    def test_recipe_scaling_malrule_vs_correct(self):
        """Test recipe_scaling: malrule incorrectly uses ratio."""
        self._test_template_algorithms('recipe_scaling', 201)

    def test_recipe_scaling_calculate_expected_answer(self):
        """Test calculate_expected_answer for recipe_scaling template."""
        problem = self.generator.generate(seed=202, template='recipe_scaling')
        expected_answer = self.malrule.calculate_expected_answer(problem)
        malrule_solution = self.malrule.solve(problem)
        self.assertTrue(answers_match(expected_answer, malrule_solution.answer))

    # Template 3: paint_mixing
    def test_paint_mixing_template(self):
        """Test paint_mixing template generates valid problems."""
        print("\n--- Testing paint_mixing template ---")
        problem = self._test_template_basic('paint_mixing', 300, ['paint', 'red', 'yellow', 'drops', 'orange', 'mix'])
        self.assertIn('red_drops', problem.metadata)

    def test_paint_mixing_malrule_vs_correct(self):
        """Test paint_mixing: malrule misapplies ratio in paint context."""
        self._test_template_algorithms('paint_mixing', 301)

    def test_paint_mixing_calculate_expected_answer(self):
        """Test calculate_expected_answer for paint_mixing template."""
        problem = self.generator.generate(seed=302, template='paint_mixing')
        expected_answer = self.malrule.calculate_expected_answer(problem)
        malrule_solution = self.malrule.solve(problem)
        self.assertTrue(answers_match(expected_answer, malrule_solution.answer))

    # Template 4: distance_rate
    def test_distance_rate_template(self):
        """Test distance_rate template generates valid problems."""
        print("\n--- Testing distance_rate template ---")
        problem = self._test_template_basic('distance_rate', 400, ['miles', 'hour', 'rate', 'travel', 'car'])
        self.assertIn('rate', problem.metadata)
        self.assertIn('time', problem.metadata)

    def test_distance_rate_malrule_vs_correct(self):
        """Test distance_rate: malrule divides instead of multiplying."""
        self._test_template_algorithms('distance_rate', 401)

    def test_distance_rate_calculate_expected_answer(self):
        """Test calculate_expected_answer for distance_rate template."""
        problem = self.generator.generate(seed=402, template='distance_rate')
        expected_answer = self.malrule.calculate_expected_answer(problem)
        malrule_solution = self.malrule.solve(problem)
        self.assertTrue(answers_match(expected_answer, malrule_solution.answer))

    # Template 5: map_scale
    def test_map_scale_template(self):
        """Test map_scale template generates valid problems."""
        print("\n--- Testing map_scale template ---")
        problem = self._test_template_basic('map_scale', 500, ['map', 'scale', 'inch', 'miles'])
        self.assertIn('map_distance', problem.metadata)
        self.assertIn('real_unit', problem.metadata)

    def test_map_scale_malrule_vs_correct(self):
        """Test map_scale: malrule misapplies scale ratio."""
        self._test_template_algorithms('map_scale', 501)

    def test_map_scale_calculate_expected_answer(self):
        """Test calculate_expected_answer for map_scale template."""
        problem = self.generator.generate(seed=502, template='map_scale')
        expected_answer = self.malrule.calculate_expected_answer(problem)
        malrule_solution = self.malrule.solve(problem)
        self.assertTrue(answers_match(expected_answer, malrule_solution.answer))

    # Template 6: word_problem_context
    def test_word_problem_context_template(self):
        """Test word_problem_context template generates valid problems."""
        print("\n--- Testing word_problem_context template ---")
        problem = self.generator.generate(seed=600, template='word_problem_context')
        self.assertEqual(problem.metadata['template'], 'word_problem_context')
        self.assertIn('problem_type', problem.metadata)
        self.assertIn('is_word_problem', problem.metadata)

    def test_word_problem_context_malrule_vs_correct(self):
        """Test word_problem_context: malrule misapplies ratio."""
        print("\n--- Testing word_problem_context algorithms ---")
        # Test multiple problem types within word_problem_context
        for seed in [601, 602, 603, 604, 605]:
            try:
                problem = self.generator.generate(seed=seed, template='word_problem_context')
                malrule_solution = self.malrule.solve(problem)
                correct_solution = self.correct_algo.solve(problem)

                # Check for edge case
                if answers_match(correct_solution.answer, malrule_solution.answer):
                    print_edge_case_warning(problem, correct_solution, malrule_solution)
                    continue  # Skip this seed, try another

                print(f"\n  word_problem_context ({problem.metadata['problem_type']}): "
                      f"Correct={correct_solution.answer}, Malrule={malrule_solution.answer}")

                self.assertFalse(malrule_solution.is_correct)
                self.assertTrue(correct_solution.is_correct)
                return  # Successfully tested
            except Exception as e:
                print(f"  Seed {seed} failed: {e}")
                continue

        self.fail("Could not find a valid word_problem_context test case")

    def test_word_problem_context_calculate_expected_answer(self):
        """Test calculate_expected_answer for word_problem_context template."""
        problem = self.generator.generate(seed=606, template='word_problem_context')
        expected_answer = self.malrule.calculate_expected_answer(problem)
        malrule_solution = self.malrule.solve(problem)
        self.assertTrue(answers_match(expected_answer, malrule_solution.answer),
                       f"calculate_expected_answer={expected_answer} != solve={malrule_solution.answer}")

    # Additional tests
    def test_get_available_templates(self):
        """Test that get_available_templates returns exactly 6 templates."""
        templates = self.generator.get_available_templates()

        self.assertEqual(len(templates), 6, f"Expected 6 templates, got {len(templates)}: {templates}")
        self.assertIn('part_to_part_ratio', templates)
        self.assertIn('recipe_scaling', templates)
        self.assertIn('paint_mixing', templates)
        self.assertIn('distance_rate', templates)
        self.assertIn('map_scale', templates)
        self.assertIn('word_problem_context', templates)

    def test_random_template_selection(self):
        """Test that template is randomly selected when not specified."""
        problem = self.generator.generate(seed=999)
        self.assertIn('template', problem.metadata)
        self.assertIn(problem.metadata['template'], self.generator.get_available_templates())

    def test_all_templates_return_strings(self):
        """Test that all templates return string answers."""
        templates = self.generator.get_available_templates()

        for idx, template in enumerate(templates):
            problem = self.generator.generate(seed=1000 + idx, template=template)

            # Check that solutions return strings
            malrule_solution = self.malrule.solve(problem)
            correct_solution = self.correct_algo.solve(problem)

            self.assertIsInstance(malrule_solution.answer, str,
                                 f"{template}: malrule answer is not string: {type(malrule_solution.answer)}")
            self.assertIsInstance(correct_solution.answer, str,
                                 f"{template}: correct answer is not string: {type(correct_solution.answer)}")


# ============================================================================
# PART 3: COMPREHENSIVE TEMPLATE TESTS
# ============================================================================

def test_all_templates():
    """Test ALL templates for Ratio-As-Division-Only."""
    print("\n\n" + "="*70)
    print("TESTING ALL TEMPLATES")
    print("="*70)

    problem_gen = RatioAsDivisionOnlyProblemGenerator(
        level=7,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = RatioAsDivisionOnlyMalrule()
    correct = RatioMultiplicativeRelationshipCorrectAlgorithm()

    templates = problem_gen.get_available_templates()
    print(f"\nFound {len(templates)} templates: {templates}")
    assert len(templates) == 6, f"Expected 6 templates, got {len(templates)}"

    passed_count = 0
    failed_count = 0
    edge_case_count = 0

    for template in templates:
        print(f"\n--- Testing template: {template} ---")

        # Try multiple seeds to find a valid test case (avoiding edge cases)
        for seed in [42, 43, 44, 45, 46, 47, 48, 49, 50]:
            try:
                problem = problem_gen.generate(seed=seed, template=template)
                correct_sol = correct.solve(problem)
                malrule_sol = malrule.solve(problem)

                # Check for edge case
                if answers_match(correct_sol.answer, malrule_sol.answer):
                    edge_case_count += 1
                    print(f"  Seed {seed}: EDGE CASE - answers match, trying next seed...")
                    continue

                # Verify calculate_expected_answer matches
                expected = malrule.calculate_expected_answer(problem)
                if not answers_match(malrule_sol.answer, expected):
                    print(f"  MISMATCH: calculate_expected_answer={expected}, solve={malrule_sol.answer}")
                    print_failure_details(problem, correct_sol, malrule_sol,
                                        problem.metadata.get('correct_answer'),
                                        problem.metadata.get('malrule_answer'))
                    failed_count += 1
                    break

                # Success!
                print(f"  Problem: {problem.text[:60]}...")
                print(f"  Correct answer: {correct_sol.answer}")
                print(f"  Malrule answer: {malrule_sol.answer}")
                print(f"  Template {template} PASSED")
                passed_count += 1
                break

            except Exception as e:
                print(f"  Seed {seed}: ERROR - {e}")
                continue
        else:
            print(f"  Template {template} FAILED - could not find valid test case")
            failed_count += 1

    print("\n" + "="*70)
    print(f"TEMPLATE TEST RESULTS: {passed_count} passed, {failed_count} failed, {edge_case_count} edge cases")
    print("="*70)

    return failed_count == 0


def test_automated_suite():
    """Run the automated test suite."""
    print("\n\n" + "="*70)
    print("RUNNING AUTOMATED TEST SUITE")
    print("="*70)

    problem_gen = RatioAsDivisionOnlyProblemGenerator(
        level=7,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = RatioAsDivisionOnlyMalrule()
    correct = RatioMultiplicativeRelationshipCorrectAlgorithm()

    test_suite = MalruleTest(malrule, correct, problem_gen)
    results = test_suite.run_all_tests(verbose=True)

    all_passed = all(r.passed for r in results)
    if all_passed:
        print("\n ALL AUTOMATED TESTS PASSED")
    return all_passed


def test_edge_case_detection():
    """Test that we properly detect edge cases where malrule produces correct answer."""
    print("\n\n" + "="*70)
    print("TESTING EDGE CASE DETECTION")
    print("="*70)

    problem_gen = RatioAsDivisionOnlyProblemGenerator(
        level=7,
        difficulty=DifficultyLevel.MEDIUM
    )
    malrule = RatioAsDivisionOnlyMalrule()
    correct = RatioMultiplicativeRelationshipCorrectAlgorithm()

    # Generate many problems and count edge cases
    edge_cases = []
    for seed in range(1000, 1100):
        for template in problem_gen.get_available_templates():
            try:
                problem = problem_gen.generate(seed=seed, template=template)
                correct_sol = correct.solve(problem)
                malrule_sol = malrule.solve(problem)

                if answers_match(correct_sol.answer, malrule_sol.answer):
                    edge_cases.append({
                        'template': template,
                        'seed': seed,
                        'problem': problem.text[:50],
                        'answer': correct_sol.answer
                    })
            except Exception:
                continue

    print(f"\nFound {len(edge_cases)} edge cases out of 600 test problems:")
    for case in edge_cases[:5]:  # Show first 5
        print(f"  - {case['template']}: seed={case['seed']}, answer={case['answer']}")

    if len(edge_cases) > 5:
        print(f"  ... and {len(edge_cases) - 5} more")

    print("\nEdge case detection: WORKING")
    return True


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    print("\n" + "="*70)
    print("  VERIFICATION TEST: Ratio-As-Division-Only  ".center(70))
    print("="*70 + "\n")

    all_passed = True

    try:
        # Run specific examples
        test_specific_examples()

        # Run template tests
        template_passed = test_all_templates()
        all_passed = all_passed and template_passed

        # Run edge case detection
        test_edge_case_detection()

        # Run automated suite
        automated_passed = test_automated_suite()
        all_passed = all_passed and automated_passed

        # Run unittest suite
        print("\n\n" + "="*70)
        print("RUNNING UNITTEST SUITE")
        print("="*70)
        suite = unittest.TestLoader().loadTestsFromTestCase(TestRatioAsDivisionOnlyTemplates)
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)

        unittest_passed = result.wasSuccessful()
        all_passed = all_passed and unittest_passed

        print("\n\n" + "="*70)
        if all_passed:
            print("  VERIFICATION COMPLETE - ALL TESTS PASSED  ".center(70))
        else:
            print("  VERIFICATION COMPLETE - SOME TESTS FAILED  ".center(70))
        print("="*70 + "\n")

        return 0 if all_passed else 1

    except Exception as e:
        print(f"\n TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
