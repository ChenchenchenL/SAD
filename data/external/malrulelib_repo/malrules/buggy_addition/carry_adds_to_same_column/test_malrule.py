#!/usr/bin/env python3
"""
Test suite for Carry-Adds-To-Same-Column malrule.

"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils import DifficultyLevel, MalruleTest, Problem
from malrules.buggy_addition.carry_adds_to_same_column import (
    CarryAddsToSameColumnProblemGenerator,
    CarryAddsToSameColumnMalrule,
    AdditionCorrectAlgorithm
)


def test_specific_examples():
    """Test with known examples demonstrating the malrule."""
    print("\n" + "="*60)
    print("TEST 1: Specific Research Examples")
    print("="*60)

    malrule = CarryAddsToSameColumnMalrule()
    correct = AdditionCorrectAlgorithm()

    # Example 1: 17 + 5 = 13 (correct: 22)
    # Ones: 7+5=12, malrule: 1+2=3, write 3
    # Tens: 1+0=1, write 1
    # Result: 13
    problem1 = Problem(
        text="What is 17 + 5?",
        operands=[17, 5],
        operation='addition',
        level=3,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'correct_answer': '22',
            'malrule_answer': '13',
            'problem_type': 'basic'
        }
    )

    correct_sol1 = correct.solve(problem1)
    malrule_sol1 = malrule.solve(problem1)

    assert correct_sol1.answer == '22', f"Expected 22, got {correct_sol1.answer}"
    assert malrule_sol1.answer == '13', f"Expected 13, got {malrule_sol1.answer}"
    assert correct_sol1.answer != malrule_sol1.answer, "Answers should differ"

    print(f"  Example 1: 17 + 5")
    print(f"    Correct: {correct_sol1.answer}, Malrule: {malrule_sol1.answer}")
    print("  PASSED")

    # Example 2: 45 + 38 = 74 (correct: 83)
    # Ones: 5+8=13, malrule: 1+3=4, write 4
    # Tens: 4+3=7, write 7
    # Result: 74
    problem2 = Problem(
        text="What is 45 + 38?",
        operands=[45, 38],
        operation='addition',
        level=3,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'correct_answer': '83',
            'malrule_answer': '74',
            'problem_type': 'basic'
        }
    )

    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)

    assert correct_sol2.answer == '83', f"Expected 83, got {correct_sol2.answer}"
    assert malrule_sol2.answer == '74', f"Expected 74, got {malrule_sol2.answer}"
    assert correct_sol2.answer != malrule_sol2.answer, "Answers should differ"

    print(f"  Example 2: 45 + 38")
    print(f"    Correct: {correct_sol2.answer}, Malrule: {malrule_sol2.answer}")
    print("  PASSED")

    # Example 3: 67 + 58 = 116 (correct: 125)
    # Ones: 7+8=15, malrule: 1+5=6, write 6
    # Tens: 6+5=11, malrule: 1+1=2, write 2 (wait, this is wrong)
    # Actually: Tens: 6+5=11, malrule: 1+1=2, write 2? No wait...
    # Let me recalculate:
    # Ones: 7+8=15, malrule: 5+1=6, write 6
    # Tens: 6+5=11, malrule: 1+1=2, write 2
    # Result: 26? Let me verify...
    # Actually the malrule applies to each column independently
    # Ones: 7+8=15 -> 5+1=6
    # Tens: 6+5=11 -> 1+1=2
    # Result: 26
    problem3 = Problem(
        text="What is 67 + 58?",
        operands=[67, 58],
        operation='addition',
        level=3,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'correct_answer': '125',
            'malrule_answer': '26',
            'problem_type': 'basic'
        }
    )

    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)

    assert correct_sol3.answer == '125', f"Expected 125, got {correct_sol3.answer}"
    assert malrule_sol3.answer == '26', f"Expected 26, got {malrule_sol3.answer}"
    assert correct_sol3.answer != malrule_sol3.answer, "Answers should differ"

    print(f"  Example 3: 67 + 58")
    print(f"    Correct: {correct_sol3.answer}, Malrule: {malrule_sol3.answer}")
    print("  PASSED")

    # Example 4: 328 + 917 (from Brown & Burton example context)
    # Ones: 8+7=15, malrule: 5+1=6
    # Tens: 2+1=3 (no carry needed)
    # Hundreds: 3+9=12, malrule: 2+1=3
    # Result: 336
    problem4 = Problem(
        text="What is 328 + 917?",
        operands=[328, 917],
        operation='addition',
        level=3,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'correct_answer': '1245',
            'malrule_answer': '336',
            'problem_type': 'basic'
        }
    )

    correct_sol4 = correct.solve(problem4)
    malrule_sol4 = malrule.solve(problem4)

    assert correct_sol4.answer == '1245', f"Expected 1245, got {correct_sol4.answer}"
    assert malrule_sol4.answer == '336', f"Expected 336, got {malrule_sol4.answer}"
    assert correct_sol4.answer != malrule_sol4.answer, "Answers should differ"

    print(f"  Example 4: 328 + 917")
    print(f"    Correct: {correct_sol4.answer}, Malrule: {malrule_sol4.answer}")
    print("  PASSED")

    # Example 5: 99 + 11 = 101 (correct: 110)
    # Ones: 9+1=10, malrule: 0+1=1
    # Tens: 9+1=10, malrule: 0+1=1
    # Result: 11
    problem5 = Problem(
        text="What is 99 + 11?",
        operands=[99, 11],
        operation='addition',
        level=3,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'correct_answer': '110',
            'malrule_answer': '11',
            'problem_type': 'basic'
        }
    )

    correct_sol5 = correct.solve(problem5)
    malrule_sol5 = malrule.solve(problem5)

    assert correct_sol5.answer == '110', f"Expected 110, got {correct_sol5.answer}"
    assert malrule_sol5.answer == '11', f"Expected 11, got {malrule_sol5.answer}"
    assert correct_sol5.answer != malrule_sol5.answer, "Answers should differ"

    print(f"  Example 5: 99 + 11")
    print(f"    Correct: {correct_sol5.answer}, Malrule: {malrule_sol5.answer}")
    print("  PASSED")

    print("\n  All specific examples PASSED")


def test_all_templates():
    """Test all problem templates generate valid problems."""
    print("\n" + "="*60)
    print("TEST 2: Template Generation")
    print("="*60)

    generator = CarryAddsToSameColumnProblemGenerator(level=3, difficulty=DifficultyLevel.MEDIUM)
    malrule = CarryAddsToSameColumnMalrule()
    correct = AdditionCorrectAlgorithm()

    templates = generator.get_available_templates()
    print(f"  Testing {len(templates)} templates: {templates}")

    for i, template in enumerate(templates):
        problem = generator.generate(seed=42+i, template=template)

        # Verify problem structure
        assert problem.text, f"Template {template}: missing text"
        assert problem.operands, f"Template {template}: missing operands"
        assert 'correct_answer' in problem.metadata, f"Template {template}: missing correct_answer"
        assert 'malrule_answer' in problem.metadata, f"Template {template}: missing malrule_answer"

        # Verify solutions
        correct_sol = correct.solve(problem)
        malrule_sol = malrule.solve(problem)

        # Check that calculated answers match metadata
        assert correct_sol.answer == problem.metadata['correct_answer'], \
            f"Template {template}: correct answer mismatch"
        assert malrule_sol.answer == problem.metadata['malrule_answer'], \
            f"Template {template}: malrule answer mismatch"

        print(f"    {template}: {problem.operands[0]} + {problem.operands[1]} = {correct_sol.answer} (malrule: {malrule_sol.answer}) PASSED")

    print("\n  All templates PASSED")


def test_edge_cases():
    """Test edge cases for the malrule."""
    print("\n" + "="*60)
    print("TEST 3: Edge Cases")
    print("="*60)

    malrule = CarryAddsToSameColumnMalrule()
    correct = AdditionCorrectAlgorithm()

    # Edge case 1: No carry needed (malrule should match correct)
    problem1 = Problem(
        text="What is 23 + 14?",
        operands=[23, 14],
        operation='addition',
        level=3,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'correct_answer': '37',
            'malrule_answer': '37',
            'problem_type': 'basic'
        }
    )

    correct_sol1 = correct.solve(problem1)
    malrule_sol1 = malrule.solve(problem1)

    assert correct_sol1.answer == '37', f"Expected 37, got {correct_sol1.answer}"
    assert malrule_sol1.answer == '37', f"Expected 37, got {malrule_sol1.answer}"
    assert correct_sol1.answer == malrule_sol1.answer, "When no carry, answers should match"

    print(f"  Edge case 1 (no carry): 23 + 14 = {correct_sol1.answer}")
    print("  PASSED (malrule matches correct when no carry needed)")

    # Edge case 2: Multiple carries
    problem2 = Problem(
        text="What is 999 + 111?",
        operands=[999, 111],
        operation='addition',
        level=3,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'correct_answer': '1110',
            'malrule_answer': '111',
            'problem_type': 'basic'
        }
    )

    correct_sol2 = correct.solve(problem2)
    malrule_sol2 = malrule.solve(problem2)

    # Ones: 9+1=10, malrule: 0+1=1
    # Tens: 9+1=10, malrule: 0+1=1
    # Hundreds: 9+1=10, malrule: 0+1=1
    # Result: 111

    assert correct_sol2.answer == '1110', f"Expected 1110, got {correct_sol2.answer}"
    assert malrule_sol2.answer == '111', f"Expected 111, got {malrule_sol2.answer}"

    print(f"  Edge case 2 (multiple carries): 999 + 111")
    print(f"    Correct: {correct_sol2.answer}, Malrule: {malrule_sol2.answer}")
    print("  PASSED")

    # Edge case 3: Large sum in single column (18 = 8+1=9)
    problem3 = Problem(
        text="What is 99 + 99?",
        operands=[99, 99],
        operation='addition',
        level=3,
        difficulty=DifficultyLevel.MEDIUM,
        metadata={
            'correct_answer': '198',
            'malrule_answer': '99',
            'problem_type': 'basic'
        }
    )

    correct_sol3 = correct.solve(problem3)
    malrule_sol3 = malrule.solve(problem3)

    # Ones: 9+9=18, malrule: 8+1=9
    # Tens: 9+9=18, malrule: 8+1=9
    # Result: 99

    assert correct_sol3.answer == '198', f"Expected 198, got {correct_sol3.answer}"
    assert malrule_sol3.answer == '99', f"Expected 99, got {malrule_sol3.answer}"

    print(f"  Edge case 3 (large sums): 99 + 99")
    print(f"    Correct: {correct_sol3.answer}, Malrule: {malrule_sol3.answer}")
    print("  PASSED")

    print("\n  All edge cases PASSED")


def test_automated_suite():
    """Run automated test suite."""
    print("\n" + "="*60)
    print("TEST 4: Automated Test Suite")
    print("="*60)

    generator = CarryAddsToSameColumnProblemGenerator(level=3, difficulty=DifficultyLevel.MEDIUM)
    malrule = CarryAddsToSameColumnMalrule()
    correct = AdditionCorrectAlgorithm()

    test_suite = MalruleTest(malrule, correct, generator)
    results = test_suite.run_all_tests(verbose=True)

    all_passed = all(r.passed for r in results)
    print(f"\n  Automated suite: {'PASSED' if all_passed else 'FAILED'}")
    return all_passed


def main():
    """Main entry point."""
    print("\n" + "="*68)
    print("  VERIFICATION TEST: Carry-Adds-To-Same-Column  ".center(68))
    print("="*68)

    try:
        test_specific_examples()
        test_all_templates()
        test_edge_cases()
        all_passed = test_automated_suite()

        print("\n" + "="*68)
        if all_passed:
            print("  VERIFICATION COMPLETE  ".center(68))
        else:
            print("  SOME TESTS FAILED  ".center(68))
        print("="*68 + "\n")

        return 0 if all_passed else 1

    except Exception as e:
        print(f"\n  TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
