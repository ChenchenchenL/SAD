"""
Problem generator for Decimal-Places-Same-As-Sig-Figs malrule.

Generates numbers with leading zeros to round to N significant figures.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Tuple
from utils import ProblemGenerator, Problem, DifficultyLevel


class DecimalPlacesSameAsSigFigsProblemGenerator(ProblemGenerator):
    """Generates significant figures rounding problems with leading zeros."""

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        """Get appropriate value ranges based on level and difficulty."""
        ranges = {
            7: {
                DifficultyLevel.EASY: {'leading_zeros': (2, 3), 'sig_figs': 2, 'digits': (2, 4)},
                DifficultyLevel.MEDIUM: {'leading_zeros': (2, 4), 'sig_figs': 3, 'digits': (3, 5)},
                DifficultyLevel.HARD: {'leading_zeros': (3, 5), 'sig_figs': 4, 'digits': (4, 6)}
            },
            8: {
                DifficultyLevel.EASY: {'leading_zeros': (2, 3), 'sig_figs': 3, 'digits': (3, 5)},
                DifficultyLevel.MEDIUM: {'leading_zeros': (2, 4), 'sig_figs': 3, 'digits': (3, 6)},
                DifficultyLevel.HARD: {'leading_zeros': (3, 5), 'sig_figs': 4, 'digits': (4, 7)}
            },
            9: {
                DifficultyLevel.EASY: {'leading_zeros': (2, 3), 'sig_figs': 3, 'digits': (3, 5)},
                DifficultyLevel.MEDIUM: {'leading_zeros': (2, 4), 'sig_figs': 3, 'digits': (3, 6)},
                DifficultyLevel.HARD: {'leading_zeros': (3, 5), 'sig_figs': 4, 'digits': (4, 8)}
            },
            10: {
                DifficultyLevel.EASY: {'leading_zeros': (2, 4), 'sig_figs': 3, 'digits': (3, 6)},
                DifficultyLevel.MEDIUM: {'leading_zeros': (2, 5), 'sig_figs': 4, 'digits': (4, 7)},
                DifficultyLevel.HARD: {'leading_zeros': (3, 6), 'sig_figs': 4, 'digits': (4, 8)}
            },
            11: {
                DifficultyLevel.EASY: {'leading_zeros': (2, 4), 'sig_figs': 3, 'digits': (3, 6)},
                DifficultyLevel.MEDIUM: {'leading_zeros': (3, 5), 'sig_figs': 4, 'digits': (4, 7)},
                DifficultyLevel.HARD: {'leading_zeros': (3, 6), 'sig_figs': 5, 'digits': (5, 9)}
            }
        }
        lvl = self.level if self.level in ranges else 9
        return ranges[lvl][self.difficulty]

    def generate(self, seed=None) -> Problem:
        """
        Generate a significant figures rounding problem.

        Args:
            seed: Optional random seed for reproducibility

        Returns:
            Problem instance
        """
        if seed is not None:
            random.seed(seed)

        # Choose problem type
        problem_types = ['basic_rounding']

        # Add enhanced problem types for higher levels
        if self.level >= 8:
            problem_types.extend([
                'scientific_notation',      # Express in scientific notation with N sig figs
                'measurement_context',      # Real-world measurement problems
                'calculation_result',       # Calculation results needing rounding
                'trailing_zeros_context',   # Numbers with trailing zeros
                # New word problem types
                'multiplication_area',      # Area calculation word problem
                'division_density',         # Density calculation word problem
                'division_speed',           # Speed calculation word problem
                'multiplication_cost',      # Cost calculation word problem
                'unit_conversion',          # Unit conversion word problem
            ])

        problem_type = random.choice(problem_types)

        ranges = self.get_value_ranges()
        sig_figs_to_round = ranges['sig_figs']

        # Handle new word problem types first
        if problem_type == 'multiplication_area':
            return self._generate_multiplication_area(sig_figs_to_round, seed)
        elif problem_type == 'division_density':
            return self._generate_division_density(sig_figs_to_round, seed)
        elif problem_type == 'division_speed':
            return self._generate_division_speed(sig_figs_to_round, seed)
        elif problem_type == 'multiplication_cost':
            return self._generate_multiplication_cost(sig_figs_to_round, seed)
        elif problem_type == 'unit_conversion':
            return self._generate_unit_conversion(sig_figs_to_round, seed)
        # Handle enhanced problem types
        elif problem_type == 'scientific_notation':
            # Generate a small decimal number and ask to express in scientific notation
            leading_zeros_min, leading_zeros_max = ranges['leading_zeros']
            num_leading_zeros = random.randint(leading_zeros_min, leading_zeros_max)

            # Generate significant digits
            first_digit = random.randint(1, 9)
            num_extra_digits = random.randint(2, 4)
            remaining_digits = [random.randint(0, 9) for _ in range(num_extra_digits)]
            sig_digits_str = str(first_digit) + ''.join(str(d) for d in remaining_digits)

            number_str = "0." + ("0" * num_leading_zeros) + sig_digits_str
            number = float(number_str)

            text = f"Express {number_str} in scientific notation with {sig_figs_to_round} significant figures."

            return Problem(
                text=text,
                operands=[sig_figs_to_round],  # Only sig_figs, number comes from text/metadata
                operation='round_to_sig_figs',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'problem_type': problem_type,
                    'number': number,
                    'number_str': number_str,
                    'sig_figs_requested': sig_figs_to_round,
                    'leading_zeros': num_leading_zeros,
                    'sig_digits': sig_digits_str
                }
            )

        elif problem_type == 'measurement_context':
            # Real-world measurement context
            contexts = [
                ('A microscope measures a cell diameter as', 'mm'),
                ('A scale measures a sample mass as', 'grams'),
                ('A sensor detects a voltage of', 'volts'),
                ('An instrument measures the thickness as', 'cm')
            ]
            context, unit = random.choice(contexts)

            leading_zeros_min, leading_zeros_max = ranges['leading_zeros']
            num_leading_zeros = random.randint(leading_zeros_min, leading_zeros_max)

            first_digit = random.randint(1, 9)
            num_extra_digits = random.randint(2, 4)
            remaining_digits = [random.randint(0, 9) for _ in range(num_extra_digits)]
            sig_digits_str = str(first_digit) + ''.join(str(d) for d in remaining_digits)

            number_str = "0." + ("0" * num_leading_zeros) + sig_digits_str
            number = float(number_str)

            text = f"{context} {number_str} {unit}. Record this measurement with {sig_figs_to_round} significant figures."

            return Problem(
                text=text,
                operands=[sig_figs_to_round],  # Only sig_figs, number comes from text/metadata
                operation='round_to_sig_figs',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'problem_type': problem_type,
                    'number': number,
                    'number_str': number_str,
                    'sig_figs_requested': sig_figs_to_round,
                    'leading_zeros': num_leading_zeros,
                    'sig_digits': sig_digits_str,
                    'context': context,
                    'unit': unit
                }
            )

        elif problem_type == 'calculation_result':
            # Calculation that needs rounding
            # Generate a division problem that results in a small decimal
            divisors = [(5, 12.3), (7, 15.8), (11, 25.4), (13, 31.7)]
            numerator, denominator = random.choice(divisors)

            result = numerator / denominator
            result_str = f"{result:.8f}".rstrip('0')

            text = f"Calculate {numerator} ÷ {denominator} and round the result to {sig_figs_to_round} significant figures."

            return Problem(
                text=text,
                operands=[sig_figs_to_round],  # Only sig_figs, no pre-computed answer!
                operation='round_to_sig_figs',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'problem_type': problem_type,
                    'number': result,
                    'number_str': result_str,
                    'sig_figs_requested': sig_figs_to_round,
                    'calculation_inputs': {'numerator': numerator, 'denominator': denominator, 'operation': 'divide'}
                }
            )

        elif problem_type == 'trailing_zeros_context':
            # Number with trailing zeros to test understanding
            leading_zeros_min, leading_zeros_max = ranges['leading_zeros']
            num_leading_zeros = random.randint(leading_zeros_min, leading_zeros_max)

            first_digit = random.randint(1, 9)
            middle_digits = [random.randint(0, 9) for _ in range(2)]
            # Add trailing zeros
            num_trailing_zeros = random.randint(2, 3)
            sig_digits_str = str(first_digit) + ''.join(str(d) for d in middle_digits) + ('0' * num_trailing_zeros)

            number_str = "0." + ("0" * num_leading_zeros) + sig_digits_str
            number = float(number_str)

            text = f"Round {number_str} to {sig_figs_to_round} significant figures."

            return Problem(
                text=text,
                operands=[sig_figs_to_round],  # Only sig_figs, number comes from text/metadata
                operation='round_to_sig_figs',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'problem_type': problem_type,
                    'number': number,
                    'number_str': number_str,
                    'sig_figs_requested': sig_figs_to_round,
                    'leading_zeros': num_leading_zeros,
                    'sig_digits': sig_digits_str,
                    'trailing_zeros': num_trailing_zeros
                }
            )

        # Original basic problem type
        leading_zeros_min, leading_zeros_max = ranges['leading_zeros']
        digits_min, digits_max = ranges['digits']

        # Generate number of leading zeros
        num_leading_zeros = random.randint(leading_zeros_min, leading_zeros_max)

        # Generate significant digits (more than what we'll round to)
        num_sig_digits = random.randint(digits_min, digits_max)

        # Ensure we have more sig digits than we're rounding to
        num_sig_digits = max(num_sig_digits, sig_figs_to_round + 1)

        # Generate the significant digits (first digit can't be 0)
        first_digit = random.randint(1, 9)
        remaining_digits = [random.randint(0, 9) for _ in range(num_sig_digits - 1)]

        # Construct the number as a string
        sig_digits_str = str(first_digit) + ''.join(str(d) for d in remaining_digits)

        # Create the decimal number with leading zeros
        number_str = "0." + ("0" * num_leading_zeros) + sig_digits_str
        number = float(number_str)

        text = f"Round {number_str} to {sig_figs_to_round} significant figures."

        return Problem(
            text=text,
            operands=[sig_figs_to_round],  # Only sig_figs, number comes from text/metadata
            operation='round_to_sig_figs',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'problem_type': 'basic_rounding',
                'number': number,
                'number_str': number_str,
                'sig_figs_requested': sig_figs_to_round,
                'leading_zeros': num_leading_zeros,
                'sig_digits': sig_digits_str
            }
        )

    def _generate_multiplication_area(self, sig_figs_to_round, seed=None):
        """Generate area calculation word problem - 3 variants."""
        if seed is not None:
            random.seed(seed)

        # Generate small decimal dimensions that will produce result with leading zeros
        # For example: 0.0045 m × 0.0067 m = 0.00003015 m²
        ranges = self.get_value_ranges()
        leading_zeros_min, leading_zeros_max = ranges['leading_zeros']

        # Pick which variant (3 variants per template)
        variant = random.randint(1, 3)

        if variant == 1:
            # Variant 1: Rectangle area in meters
            length = round(random.uniform(0.001, 0.01), 6)
            width = round(random.uniform(0.001, 0.01), 6)
            area = length * width
            text = f"A rectangular sensor has dimensions {length} meters by {width} meters. Calculate the area and express your answer with {sig_figs_to_round} significant figures."
            context = "rectangular sensor area"
            calc_inputs = {'length': length, 'width': width, 'operation': 'multiply'}
        elif variant == 2:
            # Variant 2: Square area in centimeters
            side = round(random.uniform(0.001, 0.01), 6)
            area = side * side
            text = f"A square microchip has a side length of {side} cm. Find the area and report it with {sig_figs_to_round} significant figures."
            context = "square microchip area"
            calc_inputs = {'side': side, 'operation': 'square'}
        else:
            # Variant 3: Circle area (simplified as rectangle for easier calculation)
            base = round(random.uniform(0.001, 0.01), 6)
            height = round(random.uniform(0.001, 0.01), 6)
            area = base * height
            text = f"A triangular component has a base of {base} mm and height of {height} mm. Calculate the area (base × height) and express it with {sig_figs_to_round} significant figures."
            context = "triangular component area"
            calc_inputs = {'base': base, 'height': height, 'operation': 'multiply'}

        area_str = f"{area:.15f}".rstrip('0').rstrip('.')

        return Problem(
            text=text,
            operands=[sig_figs_to_round],  # Only sig_figs, no pre-computed answer!
            operation='round_to_sig_figs',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'problem_type': 'multiplication_area',
                'number': area,
                'number_str': area_str,
                'sig_figs_requested': sig_figs_to_round,
                'context': context,
                'variant': variant,
                'calculation_type': 'multiplication',
                'calculation_inputs': calc_inputs  # Store inputs for algorithm to compute
            }
        )

    def _generate_division_density(self, sig_figs_to_round, seed=None):
        """Generate density calculation word problem - 3 variants."""
        if seed is not None:
            random.seed(seed)

        variant = random.randint(1, 3)

        if variant == 1:
            # Variant 1: Density = mass / volume (small mass, large volume)
            mass = round(random.uniform(0.5, 5.0), 3)  # grams
            volume = round(random.uniform(500, 2000), 1)  # cm³
            density = mass / volume
            text = f"A sample has a mass of {mass} grams and occupies a volume of {volume} cubic centimeters. Calculate the density in g/cm³ and express your answer with {sig_figs_to_round} significant figures."
            context = "material density"
            calc_inputs = {'numerator': mass, 'denominator': volume, 'operation': 'divide'}
        elif variant == 2:
            # Variant 2: Concentration calculation
            solute = round(random.uniform(0.1, 1.0), 3)  # grams
            solution = round(random.uniform(100, 500), 1)  # mL
            concentration = solute / solution
            text = f"A solution contains {solute} grams of solute dissolved in {solution} mL of solution. Calculate the concentration in g/mL with {sig_figs_to_round} significant figures."
            context = "solution concentration"
            calc_inputs = {'numerator': solute, 'denominator': solution, 'operation': 'divide'}
        else:
            # Variant 3: Rate calculation
            distance = round(random.uniform(1.0, 10.0), 3)  # meters
            time = round(random.uniform(500, 2000), 1)  # seconds
            rate = distance / time
            text = f"A particle travels {distance} meters in {time} seconds. Calculate the speed in m/s and express it with {sig_figs_to_round} significant figures."
            context = "particle speed"
            calc_inputs = {'numerator': distance, 'denominator': time, 'operation': 'divide'}

        result = density if variant == 1 else (concentration if variant == 2 else rate)
        result_str = f"{result:.15f}".rstrip('0').rstrip('.')

        return Problem(
            text=text,
            operands=[sig_figs_to_round],  # Only sig_figs, no pre-computed answer!
            operation='round_to_sig_figs',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'problem_type': 'division_density',
                'number': result,
                'number_str': result_str,
                'sig_figs_requested': sig_figs_to_round,
                'context': context,
                'variant': variant,
                'calculation_type': 'division',
                'calculation_inputs': calc_inputs  # Store inputs for algorithm to compute
            }
        )

    def _generate_division_speed(self, sig_figs_to_round, seed=None):
        """Generate speed/rate calculation word problem - 3 variants."""
        if seed is not None:
            random.seed(seed)

        variant = random.randint(1, 3)

        if variant == 1:
            # Variant 1: Speed = distance / time
            distance = round(random.uniform(0.5, 5.0), 3)  # km
            time = round(random.uniform(500, 2000), 1)  # hours
            speed = distance / time
            text = f"A snail travels {distance} kilometers in {time} hours. Calculate the average speed in km/h and express your answer with {sig_figs_to_round} significant figures."
            context = "snail speed"
            calc_inputs = {'numerator': distance, 'denominator': time, 'operation': 'divide'}
        elif variant == 2:
            # Variant 2: Flow rate
            volume = round(random.uniform(1.0, 10.0), 3)  # liters
            time = round(random.uniform(100, 1000), 1)  # seconds
            flow_rate = volume / time
            text = f"A dropper releases {volume} liters of liquid over {time} seconds. Find the flow rate in L/s with {sig_figs_to_round} significant figures."
            context = "liquid flow rate"
            calc_inputs = {'numerator': volume, 'denominator': time, 'operation': 'divide'}
        else:
            # Variant 3: Growth rate
            growth = round(random.uniform(0.5, 5.0), 3)  # mm
            days = round(random.uniform(200, 1000), 1)  # days
            growth_rate = growth / days
            text = f"A plant grows {growth} millimeters over {days} days. Calculate the growth rate in mm/day and report it with {sig_figs_to_round} significant figures."
            context = "plant growth rate"
            calc_inputs = {'numerator': growth, 'denominator': days, 'operation': 'divide'}

        result = speed if variant == 1 else (flow_rate if variant == 2 else growth_rate)
        result_str = f"{result:.15f}".rstrip('0').rstrip('.')

        return Problem(
            text=text,
            operands=[sig_figs_to_round],  # Only sig_figs, no pre-computed answer!
            operation='round_to_sig_figs',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'problem_type': 'division_speed',
                'number': result,
                'number_str': result_str,
                'sig_figs_requested': sig_figs_to_round,
                'context': context,
                'variant': variant,
                'calculation_type': 'division',
                'calculation_inputs': calc_inputs  # Store inputs for algorithm to compute
            }
        )

    def _generate_multiplication_cost(self, sig_figs_to_round, seed=None):
        """Generate cost/pricing calculation word problem - 3 variants."""
        if seed is not None:
            random.seed(seed)

        variant = random.randint(1, 3)

        if variant == 1:
            # Variant 1: Unit price × quantity (small decimal price)
            price = round(random.uniform(0.001, 0.01), 5)  # dollars per gram
            quantity = round(random.uniform(0.5, 5.0), 2)  # grams
            total_cost = price * quantity
            text = f"A rare chemical costs ${price} per gram. A lab orders {quantity} grams. Calculate the total cost and express your answer with {sig_figs_to_round} significant figures."
            context = "chemical purchase cost"
            calc_inputs = {'factor1': price, 'factor2': quantity, 'operation': 'multiply'}
        elif variant == 2:
            # Variant 2: Rate × time
            rate = round(random.uniform(0.0001, 0.001), 6)  # dollars per second
            time = round(random.uniform(100, 1000), 1)  # seconds
            total_cost = rate * time
            text = f"A machine operates at a cost of ${rate} per second. It runs for {time} seconds. Find the total operating cost with {sig_figs_to_round} significant figures."
            context = "machine operating cost"
            calc_inputs = {'factor1': rate, 'factor2': time, 'operation': 'multiply'}
        else:
            # Variant 3: Area × cost per unit area
            area = round(random.uniform(0.01, 0.1), 4)  # square meters
            cost_per_area = round(random.uniform(1, 10), 2)  # dollars per square meter
            total_cost = area * cost_per_area
            text = f"Specialized coating costs ${cost_per_area} per square meter. A surface with area {area} m² needs coating. Calculate the cost and report it with {sig_figs_to_round} significant figures."
            context = "coating cost"
            calc_inputs = {'factor1': area, 'factor2': cost_per_area, 'operation': 'multiply'}

        total_cost_str = f"{total_cost:.15f}".rstrip('0').rstrip('.')

        return Problem(
            text=text,
            operands=[sig_figs_to_round],  # Only sig_figs, no pre-computed answer!
            operation='round_to_sig_figs',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'problem_type': 'multiplication_cost',
                'number': total_cost,
                'number_str': total_cost_str,
                'sig_figs_requested': sig_figs_to_round,
                'context': context,
                'variant': variant,
                'calculation_type': 'multiplication',
                'calculation_inputs': calc_inputs  # Store inputs for algorithm to compute
            }
        )

    def _generate_unit_conversion(self, sig_figs_to_round, seed=None):
        """Generate unit conversion word problem - 3 variants."""
        if seed is not None:
            random.seed(seed)

        variant = random.randint(1, 3)

        if variant == 1:
            # Variant 1: meters to kilometers (division by 1000)
            meters = round(random.uniform(0.5, 10.0), 3)
            kilometers = meters / 1000
            text = f"Convert {meters} meters to kilometers and express your answer with {sig_figs_to_round} significant figures."
            context = "meters to kilometers"
            calc_inputs = {'numerator': meters, 'denominator': 1000, 'operation': 'divide'}
        elif variant == 2:
            # Variant 2: grams to kilograms (division by 1000)
            grams = round(random.uniform(1.0, 10.0), 3)
            kilograms = grams / 1000
            text = f"A sample has a mass of {grams} grams. Express this mass in kilograms with {sig_figs_to_round} significant figures."
            context = "grams to kilograms"
            calc_inputs = {'numerator': grams, 'denominator': 1000, 'operation': 'divide'}
        else:
            # Variant 3: milliliters to liters (division by 1000)
            milliliters = round(random.uniform(1.0, 10.0), 3)
            liters = milliliters / 1000
            text = f"A container holds {milliliters} milliliters of liquid. Convert this volume to liters and report it with {sig_figs_to_round} significant figures."
            context = "milliliters to liters"
            calc_inputs = {'numerator': milliliters, 'denominator': 1000, 'operation': 'divide'}

        result = kilometers if variant == 1 else (kilograms if variant == 2 else liters)
        result_str = f"{result:.15f}".rstrip('0').rstrip('.')

        return Problem(
            text=text,
            operands=[sig_figs_to_round],  # Only sig_figs, no pre-computed answer!
            operation='round_to_sig_figs',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'problem_type': 'unit_conversion',
                'number': result,
                'number_str': result_str,
                'sig_figs_requested': sig_figs_to_round,
                'context': context,
                'variant': variant,
                'calculation_type': 'division',
                'calculation_inputs': calc_inputs  # Store inputs for algorithm to compute
            }
        )
