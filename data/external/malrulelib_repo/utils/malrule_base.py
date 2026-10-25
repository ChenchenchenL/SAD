"""
Base classes for malrule implementations.

This module provides abstract base classes that all malrule implementations
should inherit from, ensuring consistent structure across the project.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple, Optional
from enum import Enum

class DifficultyLevel(Enum):
    """Difficulty levels for problem generation."""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

@dataclass
class Problem:
    """
    Represents a mathematical problem instance.

    Attributes:
        text: Natural language problem statement
        operands: The numbers/values involved in the problem
        operation: The mathematical operation(s) required
        level: Complexity level (1-10)
        difficulty: Problem difficulty level
        metadata: Additional problem-specific information
    """
    text: str
    operands: List[Any]
    operation: str
    level: int
    difficulty: DifficultyLevel
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

@dataclass
class Solution:
    """
    Represents a solution to a problem (correct or incorrect).

    Attributes:
        answer: The final answer
        steps: List of solution steps with explanations
        is_correct: Whether this solution is correct
        algorithm_name: Name of the algorithm used (e.g., "Borrow-No-Decrement")
    """
    answer: Any
    steps: List[str]
    is_correct: bool
    algorithm_name: str

    def show_work(self) -> str:
        """Returns formatted string showing all solution steps."""
        work = f"\n{self.algorithm_name}\n" + "="*50 + "\n"
        for i, step in enumerate(self.steps, 1):
            work += f"Step {i}: {step}\n"
        work += f"\nFinal Answer: {self.answer}\n"
        return work

class ProblemGenerator(ABC):
    """
    Abstract base class for problem generators.

    Each malrule should implement this to generate appropriate problem instances.
    """

    def __init__(self, level: int, difficulty: DifficultyLevel = DifficultyLevel.MEDIUM):
        """
        Initialize problem generator.

        Args:
            level: Complexity level for problems (1-10)
            difficulty: Difficulty level for problem generation
        """
        self.level = level
        self.difficulty = difficulty

    @abstractmethod
    def generate(self, seed: Optional[int] = None) -> Problem:
        """
        Generate a single problem instance.

        Args:
            seed: Optional random seed for reproducibility

        Returns:
            Problem instance
        """
        pass

    @abstractmethod
    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        """
        Get appropriate value ranges for the complexity level.

        Returns:
            Dictionary mapping parameter names to (min, max) tuples
        """
        pass

    def generate_batch(self, count: int, seed: Optional[int] = None) -> List[Problem]:
        """
        Generate multiple problem instances.

        Args:
            count: Number of problems to generate
            seed: Optional random seed for reproducibility

        Returns:
            List of Problem instances
        """
        import random
        if seed is not None:
            random.seed(seed)

        return [self.generate() for _ in range(count)]

class Algorithm(ABC):
    """
    Abstract base class for solution algorithms (correct or malrule).

    Each implementation provides a step-by-step solution procedure.
    """

    @abstractmethod
    def solve(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Solve the problem using this algorithm.

        Args:
            problem: Problem instance to solve
            verbose: If True, generate verbose explanatory steps; if False, generate concise steps

        Returns:
            Solution with answer and steps
        """
        pass

    @abstractmethod
    def get_name(self) -> str:
        """
        Get the name of this algorithm.

        Returns:
            Algorithm name (e.g., "Correct Algorithm" or "Borrow-No-Decrement")
        """
        pass

    @abstractmethod
    def get_description(self) -> str:
        """
        Get a description of how this algorithm works.

        Returns:
            Algorithm description
        """
        pass

class Malrule(Algorithm):
    """
    Base class for malrule (incorrect) algorithms.

    Adds additional methods specific to documenting systematic errors.
    """

    @abstractmethod
    def calculate_expected_answer(self, problem: Problem) -> Any:
        """
        Calculate the expected incorrect answer that this malrule should produce.

        This method defines what answer the malrule SHOULD produce based on its
        systematic error pattern. It's used for validation to ensure the malrule
        implementation is correct.

        IMPORTANT: This should NOT just call solve() - it should independently
        calculate the expected wrong answer based on the malrule's logic.

        Args:
            problem: Problem instance

        Returns:
            The expected incorrect answer this malrule should produce

        Example:
            For Add-Numerators-Add-Denominators malrule with problem "1/2 + 1/3":
            - Should return "2/5" (because 1+1=2, 2+3=5)
        """
        pass

    def solve(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Solve using the malrule (incorrectly).

        Args:
            problem: Problem instance to solve
            verbose: If True, generate verbose explanatory steps; if False, generate concise steps

        Returns a Solution with is_correct=False.
        """
        solution = self._apply_malrule(problem, verbose=verbose)
        solution.is_correct = False
        return solution

    @abstractmethod
    def _apply_malrule(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Internal method implementing the specific malrule logic.

        Args:
            problem: Problem to solve incorrectly
            verbose: If True, generate verbose explanatory steps; if False, generate concise steps

        Returns:
            Solution with malrule applied
        """
        pass

class CorrectAlgorithm(Algorithm):
    """
    Base class for correct solution algorithms.
    """

    def solve(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Solve using the correct algorithm.

        Args:
            problem: Problem instance to solve
            verbose: If True, generate verbose explanatory steps; if False, generate concise steps

        Returns a Solution with is_correct=True.
        """
        solution = self._apply_correct_algorithm(problem, verbose=verbose)
        solution.is_correct = True
        return solution

    @abstractmethod
    def _apply_correct_algorithm(self, problem: Problem, verbose: bool = False) -> Solution:
        """
        Internal method implementing the correct algorithm.

        Args:
            problem: Problem to solve correctly
            verbose: If True, generate verbose explanatory steps; if False, generate concise steps

        Returns:
            Solution with correct algorithm applied
        """
        pass

class MalruleComparison:
    """
    Utility class for comparing correct and malrule solutions.
    """

    @staticmethod
    def compare(problem: Problem, correct_algo: CorrectAlgorithm,
                malrule: Malrule) -> Dict[str, Any]:
        """
        Compare solutions from correct algorithm and malrule.

        Args:
            problem: Problem to solve
            correct_algo: Correct algorithm instance
            malrule: Malrule instance

        Returns:
            Dictionary with comparison data
        """
        correct_solution = correct_algo.solve(problem)
        malrule_solution = malrule.solve(problem)

        return {
            'problem': problem.text,
            'correct_answer': correct_solution.answer,
            'malrule_answer': malrule_solution.answer,
            'answers_match': correct_solution.answer == malrule_solution.answer,
            'correct_steps': correct_solution.steps,
            'malrule_steps': malrule_solution.steps,
            'malrule_name': malrule.get_name()
        }

    @staticmethod
    def format_comparison(comparison: Dict[str, Any]) -> str:
        """
        Format comparison results as readable string.

        Args:
            comparison: Comparison dictionary from compare()

        Returns:
            Formatted string
        """
        output = f"\n{'='*70}\n"
        output += f"PROBLEM: {comparison['problem']}\n"
        output += f"{'='*70}\n\n"

        output += f"CORRECT ANSWER: {comparison['correct_answer']}\n"
        output += f"MALRULE ANSWER: {comparison['malrule_answer']}"

        if comparison['answers_match']:
            output += " ✓ (Happens to be correct!)\n"
        else:
            output += " ✗ (Incorrect)\n"

        output += f"\nMALRULE: {comparison['malrule_name']}\n"
        output += f"MISCONCEPTION: {comparison['misconception']}\n\n"

        output += f"{'Correct Solution Steps:':-^70}\n"
        for i, step in enumerate(comparison['correct_steps'], 1):
            output += f"{i}. {step}\n"

        output += f"\n{'Malrule Solution Steps:':-^70}\n"
        for i, step in enumerate(comparison['malrule_steps'], 1):
            output += f"{i}. {step}\n"

        output += f"\n{'='*70}\n"
        return output
