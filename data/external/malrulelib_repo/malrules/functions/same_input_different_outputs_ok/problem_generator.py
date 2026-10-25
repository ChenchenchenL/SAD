"""
Problem generator for Same-Input-Different-Outputs-OK malrule.

Generates function definition problems (is this a function?) where
the relation has repeated inputs with different outputs.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Tuple, Optional
from utils import ProblemGenerator, Problem, DifficultyLevel


class SameInputDifferentOutputsOKProblemGenerator(ProblemGenerator):
    """
    Generates function definition problems to elicit Same-Input-Different-Outputs-OK.

    Creates problems where students must determine if a relation is a function,
    with some relations having repeated inputs (which makes them NOT functions).
    """

    def get_available_templates(self) -> list:
        """Return list of available problem templates."""
        return [
            'ordered_pairs_set',
            'table_format',
            'graph_points',
            'mapping_diagram',
            'word_problem'
        ]

    def get_name(self) -> str:
        return "Same Input Different Outputs OK Problem Generator"

    def get_description(self) -> str:
        return (
            "Generates function definition problems where students must "
            "identify if a relation is a function based on the one-to-one "
            "or many-to-one input-output mapping rule."
        )

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        """Get appropriate value ranges based on level."""
        ranges = {
            8: {
                DifficultyLevel.EASY: (1, 10),
                DifficultyLevel.MEDIUM: (1, 15),
                DifficultyLevel.HARD: (1, 20),
            },
            9: {
                DifficultyLevel.EASY: (1, 15),
                DifficultyLevel.MEDIUM: (1, 20),
                DifficultyLevel.HARD: (1, 30),
            },
            10: {
                DifficultyLevel.EASY: (1, 20),
                DifficultyLevel.MEDIUM: (1, 30),
                DifficultyLevel.HARD: (1, 40),
            }
        }

        lvl = self.level if self.level in ranges else 9
        return {'values': ranges[lvl][self.difficulty]}

    def generate(self, seed: Optional[int] = None, template: Optional[str] = None) -> Problem:
        """
        Generate a function definition problem based on selected template.

        Args:
            seed: Optional random seed for reproducibility
            template: Specific template to use, or None for random selection

        Returns:
            Problem instance
        """
        if seed is not None:
            random.seed(seed)

        # Select template
        if template is None:
            template = random.choice(self.get_available_templates())

        # Generate based on template
        if template == 'ordered_pairs_set':
            return self._generate_ordered_pairs_set(seed)
        elif template == 'table_format':
            return self._generate_table_format(seed)
        elif template == 'graph_points':
            return self._generate_graph_points(seed)
        elif template == 'mapping_diagram':
            return self._generate_mapping_diagram(seed)
        elif template == 'word_problem':
            return self._generate_word_problem(seed)
        else:
            raise ValueError(f"Unknown template: {template}")

    def _generate_pairs(self, min_val: int, max_val: int, include_repeated: bool = None):
        """
        Helper method to generate ordered pairs.

        Args:
            min_val: Minimum value for numbers
            max_val: Maximum value for numbers
            include_repeated: If True, create invalid function; if False, create valid function;
                            if None, randomly choose

        Returns:
            tuple: (pairs, is_function, repeated_input_if_any)
        """
        if include_repeated is None:
            # Randomly decide to make it a function or not
            # Bias toward NOT a function (70%) to better test the malrule
            include_repeated = random.random() < 0.7

        num_pairs = random.randint(3, 5)

        if not include_repeated:
            # Create a valid function - all inputs are unique
            inputs = random.sample(range(min_val, max_val + 1), num_pairs)
            outputs = [random.randint(min_val, max_val + 1) for _ in range(num_pairs)]
            pairs = list(zip(inputs, outputs))
            return pairs, True, None
        else:
            # Create invalid function - at least one repeated input with different output
            unique_count = num_pairs - 1
            inputs = random.sample(range(min_val, max_val + 1), unique_count)
            outputs = [random.randint(min_val, max_val + 1) for _ in range(unique_count)]

            # Add a repeated input with different output
            repeated_input = random.choice(inputs)
            original_output = outputs[inputs.index(repeated_input)]
            new_output = random.randint(min_val, max_val + 1)
            while new_output == original_output:
                new_output = random.randint(min_val, max_val + 1)

            inputs.append(repeated_input)
            outputs.append(new_output)

            # Shuffle to make it less obvious
            combined = list(zip(inputs, outputs))
            random.shuffle(combined)
            return combined, False, repeated_input

    def _generate_ordered_pairs_set(self, seed=None) -> Problem:
        """Generate basic ordered pairs set problem."""
        if seed is not None:
            random.seed(seed)

        min_val, max_val = self.get_value_ranges()['values']
        pairs, is_function, repeated_input = self._generate_pairs(min_val, max_val)

        # Format as ordered pairs
        pairs_str = ", ".join([f"({x}, {y})" for x, y in pairs])

        # Create problem text
        problem_texts = [
            f"Is the following relation a function? {{{pairs_str}}}",
            f"Does this set represent a function? {{{pairs_str}}}",
            f"Determine if this relation is a function: {{{pairs_str}}}",
        ]
        problem_text = random.choice(problem_texts)

        return Problem(
            text=problem_text,
            operands=[len(pairs)],
            operation='function_definition',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'pairs': pairs,
                'pairs_str': pairs_str,
                'is_function': is_function,
                'num_pairs': len(pairs),
                'repeated_input': repeated_input,
                'template': 'ordered_pairs_set'
            }
        )

    def _generate_table_format(self, seed=None) -> Problem:
        """Generate table format problem."""
        if seed is not None:
            random.seed(seed)

        min_val, max_val = self.get_value_ranges()['values']
        pairs, is_function, repeated_input = self._generate_pairs(min_val, max_val)

        # Format as a table
        inputs = [str(x) for x, y in pairs]
        outputs = [str(y) for x, y in pairs]

        # Create table representation
        table_str = f"""
Input (x):  {' | '.join(inputs)}
Output (y): {' | '.join(outputs)}"""

        problem_text = f"Does this table represent a function?{table_str}"

        pairs_str = ", ".join([f"({x}, {y})" for x, y in pairs])

        return Problem(
            text=problem_text,
            operands=[len(pairs)],
            operation='function_definition_table',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'pairs': pairs,
                'pairs_str': pairs_str,
                'is_function': is_function,
                'num_pairs': len(pairs),
                'repeated_input': repeated_input,
                'table_format': True,
                'template': 'table_format'
            }
        )

    def _generate_graph_points(self, seed=None) -> Problem:
        """Generate graph points problem."""
        if seed is not None:
            random.seed(seed)

        min_val, max_val = self.get_value_ranges()['values']
        pairs, is_function, repeated_input = self._generate_pairs(min_val, max_val)

        # Format as graph description
        points_list = [f"({x}, {y})" for x, y in pairs]
        points_str = ", ".join(points_list)

        problem_texts = [
            f"A graph contains the following points: {points_str}. Does this graph represent a function?",
            f"The points {points_str} are plotted on a coordinate plane. Do they represent a function?",
            f"If we plot these points on a graph: {points_str}, will they pass the vertical line test?",
        ]
        problem_text = random.choice(problem_texts)

        pairs_str = ", ".join([f"({x}, {y})" for x, y in pairs])

        return Problem(
            text=problem_text,
            operands=[len(pairs)],
            operation='function_definition_graph',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'pairs': pairs,
                'pairs_str': pairs_str,
                'is_function': is_function,
                'num_pairs': len(pairs),
                'repeated_input': repeated_input,
                'template': 'graph_points'
            }
        )

    def _generate_mapping_diagram(self, seed=None) -> Problem:
        """Generate mapping diagram problem."""
        if seed is not None:
            random.seed(seed)

        min_val, max_val = self.get_value_ranges()['values']
        pairs, is_function, repeated_input = self._generate_pairs(min_val, max_val)

        # Format as mapping diagram description
        mapping_lines = []
        for x, y in pairs:
            mapping_lines.append(f"  {x} → {y}")

        mapping_str = "\n".join(mapping_lines)

        problem_text = f"Consider this mapping diagram:\n{mapping_str}\n\nDoes this mapping represent a function?"

        pairs_str = ", ".join([f"({x}, {y})" for x, y in pairs])

        return Problem(
            text=problem_text,
            operands=[len(pairs)],
            operation='function_definition_mapping',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'pairs': pairs,
                'pairs_str': pairs_str,
                'is_function': is_function,
                'num_pairs': len(pairs),
                'repeated_input': repeated_input,
                'template': 'mapping_diagram'
            }
        )

    def _generate_word_problem(self, seed=None) -> Problem:
        """Generate word problem context."""
        if seed is not None:
            random.seed(seed)

        min_val, max_val = self.get_value_ranges()['values']
        pairs, is_function, repeated_input = self._generate_pairs(min_val, max_val)

        # Real-world contexts for function definition
        contexts = [
            {
                'scenario': 'student ID',
                'input_label': 'Student ID',
                'output_label': 'Name',
                'question': 'Does this represent a valid student ID system (is it a function)?'
            },
            {
                'scenario': 'phone number',
                'input_label': 'Phone Number',
                'output_label': 'Person',
                'question': 'Can this be a valid phone directory (is it a function)?'
            },
            {
                'scenario': 'locker number',
                'input_label': 'Locker Number',
                'output_label': 'Student',
                'question': 'Is this a valid locker assignment system (is it a function)?'
            },
            {
                'scenario': 'seat number',
                'input_label': 'Seat Number',
                'output_label': 'Person',
                'question': 'Does this represent a valid seating arrangement (is it a function)?'
            }
        ]

        context = random.choice(contexts)

        # Create description of mappings
        mapping_lines = []
        for x, y in pairs:
            mapping_lines.append(f"  {context['input_label']} {x} → {context['output_label']} #{y}")

        mapping_str = "\n".join(mapping_lines)

        problem_text = f"A system has the following {context['scenario']} assignments:\n{mapping_str}\n\n{context['question']}"

        pairs_str = ", ".join([f"({x}, {y})" for x, y in pairs])

        return Problem(
            text=problem_text,
            operands=[len(pairs)],
            operation='function_definition_word',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'pairs': pairs,
                'pairs_str': pairs_str,
                'is_function': is_function,
                'num_pairs': len(pairs),
                'repeated_input': repeated_input,
                'context': context['scenario'],
                'template': 'word_problem'
            }
        )
