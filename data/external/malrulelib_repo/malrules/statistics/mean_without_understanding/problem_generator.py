"""
Problem generator for Mean-Without-Understanding malrule.

Generates data sets where the mean is misleading or where median/mode
would be more appropriate measures of center. Tests whether students
understand when mean is representative vs. non-representative.
"""

import sys
sys.path.append('/home/user/malrule-coding')

import random
from typing import Dict, Tuple, Optional, List
from utils import ProblemGenerator, Problem, DifficultyLevel


class MeanUnderstandingProblemGenerator(ProblemGenerator):
    """
    Generates statistics problems to elicit Mean-Without-Understanding malrule.

    Focus on data sets with outliers, skewed distributions, or situations
    where mean is not the most appropriate measure of center.
    """

    def get_name(self) -> str:
        return "Mean-Without-Understanding Problem Generator"

    def get_description(self) -> str:
        return (
            "Generates data sets where mean is misleading or not representative. "
            "Tests whether students understand when to use mean vs. median/mode "
            "and whether they recognize outliers affecting the mean."
        )

    def get_value_ranges(self) -> Dict[str, Tuple[int, int]]:
        """Get appropriate value ranges based on level and difficulty."""
        ranges = {
            5: {
                DifficultyLevel.EASY: (1, 10),       # Simple numbers 1-10
                DifficultyLevel.MEDIUM: (1, 20),
                DifficultyLevel.HARD: (1, 50),
            },
            6: {
                DifficultyLevel.EASY: (1, 20),
                DifficultyLevel.MEDIUM: (1, 50),
                DifficultyLevel.HARD: (1, 100),
            },
            7: {
                DifficultyLevel.EASY: (1, 50),
                DifficultyLevel.MEDIUM: (1, 100),
                DifficultyLevel.HARD: (1, 500),
            },
            8: {
                DifficultyLevel.EASY: (1, 100),
                DifficultyLevel.MEDIUM: (1, 500),
                DifficultyLevel.HARD: (1, 1000),
            },
            9: {
                DifficultyLevel.EASY: (1, 100),
                DifficultyLevel.MEDIUM: (1, 1000),
                DifficultyLevel.HARD: (1, 5000),
            }
        }

        lvl = self.level if self.level in ranges else 6
        return {'values': ranges[lvl][self.difficulty]}

    def get_available_templates(self) -> List[str]:
        """Return list of available problem templates."""
        return [
            'outlier_high',
            'outlier_low',
            'bimodal',
            'skewed_right',
            'best_measure_question',
            'income_inequality_context',
            'real_estate_market',
            'environmental_data',
            'daily_routine_outliers',
            'word_problem_context'  # NEW: Structured word problems with formula types
        ]

    def generate(self, seed: Optional[int] = None, template: Optional[str] = None) -> Problem:
        """
        Generate a statistics problem involving mean interpretation.

        Args:
            seed: Optional random seed for reproducibility
            template: Specific template to use, or None for random selection

        Returns:
            Problem instance
        """
        if seed is not None:
            random.seed(seed)

        # If template specified, generate that specific template
        if template == 'word_problem_context':
            return self._generate_word_problem_context(seed)

        min_val, max_val = self.get_value_ranges()['values']

        # Choose problem type
        problem_types = [
            'outlier_high',           # Data with one very high outlier
            'outlier_low',            # Data with one very low outlier
            'bimodal',                # Two clusters, mean between them
            'skewed_right',           # Right-skewed data
            'best_measure_question',  # Which measure is most appropriate?
        ]

        # Add enhanced problem types for higher levels
        if self.level >= 7:
            problem_types.extend([
                'income_inequality_context',  # Wage data with executive compensation
                'real_estate_market',          # Housing prices with luxury outliers
                'environmental_data',          # Scientific measurements with anomalies
                'daily_routine_outliers',      # Time durations with occasional extremes
            ])

        # Use template if specified and valid, otherwise random choice
        if template and template in problem_types:
            problem_type = template
        else:
            problem_type = random.choice(problem_types)

        if problem_type == 'outlier_high':
            # Create data with high outlier
            cluster_size = random.randint(4, 7)
            cluster_center = random.randint(min_val, min(max_val // 10, 20))
            data = [cluster_center + random.randint(-2, 2) for _ in range(cluster_size)]
            # Add outlier (much higher)
            outlier = cluster_center * random.randint(5, 15)
            data.append(outlier)
            random.shuffle(data)

            question_type = random.choice(['calculate', 'interpret', 'representative'])
            if question_type == 'calculate':
                problem_text = f"Calculate the mean of this data set: {data}"
            elif question_type == 'interpret':
                problem_text = f"The mean of {data} is {sum(data)/len(data):.1f}. Is this mean representative of the typical value? Explain."
            else:  # representative
                problem_text = f"For the data set {data}, which measure of center (mean, median, or mode) is most representative? Why?"

        elif problem_type == 'outlier_low':
            # Create data with low outlier (e.g., test scores with one failure)
            cluster_size = random.randint(4, 7)
            # Use upper 2/3 of range for cluster center (not hardcoded 50)
            cluster_center = random.randint(max(min_val, max_val * 2 // 3), max_val)
            data = [cluster_center + random.randint(-5, 5) for _ in range(cluster_size)]
            # Add outlier (much lower)
            outlier = max(0, cluster_center // random.randint(3, 8))
            data.append(outlier)
            random.shuffle(data)

            question_type = random.choice(['calculate', 'interpret'])
            if question_type == 'calculate':
                problem_text = f"Calculate the mean of: {data}"
            else:
                problem_text = f"Which measure of center is most appropriate for {data}: mean, median, or mode?"

        elif problem_type == 'bimodal':
            # Two clusters
            cluster1_size = random.randint(3, 5)
            cluster2_size = random.randint(3, 5)
            cluster1_center = random.randint(min_val, max_val // 3)
            cluster2_center = random.randint(2 * max_val // 3, max_val)

            data = [cluster1_center + random.randint(-2, 2) for _ in range(cluster1_size)]
            data.extend([cluster2_center + random.randint(-2, 2) for _ in range(cluster2_size)])
            random.shuffle(data)

            problem_text = f"For the data set {data}, is the mean a good measure of center? Why or why not?"

        elif problem_type == 'skewed_right':
            # Right-skewed: many low values, few high values
            low_values = [random.randint(min_val, min_val + 5) for _ in range(random.randint(5, 8))]
            high_values = [random.randint(max_val // 2, max_val) for _ in range(random.randint(1, 3))]
            data = low_values + high_values
            random.shuffle(data)

            problem_text = f"Which measure of center (mean, median, or mode) best describes the typical value in {data}?"

        elif problem_type == 'best_measure_question':
            # Create scenario with clear answer
            scenario_type = random.choice(['salaries', 'test_scores', 'ages'])

            if scenario_type == 'salaries':
                # Typical case: median better for salaries with outliers
                employees = random.randint(8, 12)
                typical_salary = random.randint(30, 60)  # thousands
                data = [typical_salary + random.randint(-5, 5) for _ in range(employees - 1)]
                ceo_salary = typical_salary * random.randint(5, 15)
                data.append(ceo_salary)
                random.shuffle(data)
                problem_text = f"A company has {employees} employees with salaries (in thousands): {data}. Which measure of center best represents a 'typical' salary: mean, median, or mode?"

            elif scenario_type == 'test_scores':
                # Test scores where one person failed
                students = random.randint(7, 10)
                typical_score = random.randint(75, 95)
                data = [typical_score + random.randint(-5, 5) for _ in range(students - 1)]
                failing_score = random.randint(20, 40)
                data.append(failing_score)
                random.shuffle(data)
                problem_text = f"Test scores: {data}. Which measure of center is most representative?"

            else:  # ages
                # Ages with one very different value
                group_size = random.randint(6, 9)
                typical_age = random.randint(8, 12)
                data = [typical_age + random.randint(-1, 1) for _ in range(group_size - 1)]
                different_age = random.randint(35, 50)  # Adult supervisor
                data.append(different_age)
                random.shuffle(data)
                problem_text = f"Ages in a group: {data}. Which measure best represents the typical age?"

        elif problem_type == 'income_inequality_context':
            # Wage/salary data with executive compensation outlier
            num_workers = random.randint(8, 12)
            typical_wage = random.randint(40, 65)  # thousands
            data = [typical_wage + random.randint(-8, 8) for _ in range(num_workers - 1)]

            # Add executive salary (much higher)
            executive_multiplier = random.randint(8, 20)
            executive_salary = typical_wage * executive_multiplier
            data.append(executive_salary)
            random.shuffle(data)

            contexts = [
                f"A tech startup has {num_workers} employees with annual salaries (in thousands): {data}. The company claims the 'average' salary demonstrates competitive pay. Which measure of center (mean, median, or mode) actually represents a typical employee's salary?",
                f"Annual salaries at a small company (in $1000s): {data}. Management reports the mean salary in recruiting materials. Is this representative of what a typical employee earns?",
                f"Employee compensation data (in thousands): {data}. For salary negotiations, which measure of center best represents typical employee pay: mean, median, or mode?"
            ]
            problem_text = random.choice(contexts)

        elif problem_type == 'real_estate_market':
            # Housing prices with luxury property outliers
            num_homes = random.randint(7, 11)
            typical_price = random.randint(200, 400)  # thousands
            data = [typical_price + random.randint(-50, 50) for _ in range(num_homes - 2)]

            # Add 1-2 luxury properties
            luxury_count = random.randint(1, 2)
            for _ in range(luxury_count):
                luxury_price = typical_price * random.randint(3, 8)
                data.append(luxury_price)
            random.shuffle(data)

            contexts = [
                f"Home sale prices in a neighborhood (in $1000s): {data}. A real estate agent says the 'average' home price is ${sum(data)/len(data):.0f},000. Does this represent what a typical buyer should expect to pay?",
                f"Recent home sales (in thousands): {data}. Which measure of center best describes the typical home price in this area: mean, median, or mode?",
                f"Housing market data (prices in $1000s): {data}. For a buyer researching the neighborhood, which statistic is most useful: mean, median, or mode?"
            ]
            problem_text = random.choice(contexts)

        elif problem_type == 'environmental_data':
            # Scientific measurements with anomalous readings
            num_readings = random.randint(8, 12)
            typical_reading = random.randint(15, 35)
            data = [typical_reading + random.randint(-3, 3) for _ in range(num_readings - 1)]

            # Add anomalous reading (equipment malfunction or unusual event)
            anomaly_type = random.choice(['high', 'low'])
            if anomaly_type == 'high':
                anomaly = typical_reading * random.randint(3, 6)
            else:
                anomaly = max(0, typical_reading // random.randint(2, 4))
            data.append(anomaly)
            random.shuffle(data)

            measurement_types = [
                ('daily temperature readings (°C)', 'temperature'),
                ('air quality index measurements', 'air quality'),
                ('water pH levels', 'pH'),
                ('noise level readings (dB)', 'noise level')
            ]
            measurement_desc, measurement_name = random.choice(measurement_types)

            contexts = [
                f"A scientist collected {measurement_desc}: {data}. One reading appears anomalous (equipment error or unusual event). Which measure of center best represents typical {measurement_name}: mean or median?",
                f"Environmental monitoring data ({measurement_name}): {data}. Calculate the mean. Does it represent typical conditions, or would median be better?",
                f"Data set: {data}. This represents {measurement_desc}. Which measure is most appropriate for summarizing this data: mean, median, or mode?"
            ]
            problem_text = random.choice(contexts)

        elif problem_type == 'daily_routine_outliers':
            # Daily time measurements with occasional extreme values
            num_days = random.randint(7, 10)
            typical_time = random.randint(20, 45)  # minutes
            data = [typical_time + random.randint(-5, 5) for _ in range(num_days - 1)]

            # Add outlier day (unusual circumstance)
            outlier_time = typical_time * random.randint(2, 5)
            data.append(outlier_time)
            random.shuffle(data)

            activity_types = [
                ('commute times to school/work (in minutes)', 'commute'),
                ('time spent on homework each day (in minutes)', 'homework time'),
                ('daily exercise duration (in minutes)', 'exercise time'),
                ('time waiting in line at lunch (in minutes)', 'wait time')
            ]
            activity_desc, activity_name = random.choice(activity_types)

            contexts = [
                f"Daily {activity_desc}: {data}. One day was unusual (traffic jam, special event, etc.). Which measure best represents typical {activity_name}: mean or median?",
                f"Over {num_days} days, recorded {activity_desc}: {data}. Is the mean representative of a typical day?",
                f"Time data (in minutes): {data} representing {activity_desc}. Which measure of center is most appropriate?"
            ]
            problem_text = random.choice(contexts)

        return Problem(
            text=problem_text,
            operands=data if isinstance(data, list) else [data],
            operation='statistical_interpretation',
            level=self.level,
            difficulty=self.difficulty,
            metadata={
                'data': data,
                'problem_type': problem_type,
                'has_outlier': problem_type in ['outlier_high', 'outlier_low', 'best_measure_question',
                                                 'income_inequality_context', 'real_estate_market',
                                                 'environmental_data', 'daily_routine_outliers']
            }
        )

    def _generate_word_problem_context(self, seed: Optional[int] = None) -> Problem:
        """
        Generate word problem covering ALL formula types with 3 variants each.

        Formula types covered:
        1. calculate_mean_with_outlier: Calculate mean when outliers present
        2. compare_mean_median: Determine which measure is more appropriate
        3. interpret_representativeness: Evaluate if mean represents typical values
        """
        if seed is not None:
            random.seed(seed)

        # Select which formula type to embed
        formula_types = ['calculate_mean_with_outlier', 'compare_mean_median', 'interpret_representativeness']
        formula_type = random.choice(formula_types)
        variant = random.randint(0, 2)  # 3 variants per formula type

        min_val, max_val = self.get_value_ranges()['values']

        if formula_type == 'calculate_mean_with_outlier':
            # Generate data with clear outlier
            cluster_size = random.randint(4, 6)
            cluster_center = random.randint(min_val, min(max_val // 10, 20))
            data = [cluster_center + random.randint(-2, 2) for _ in range(cluster_size)]
            # Add outlier (much higher)
            outlier = cluster_center * random.randint(5, 10)
            data.append(outlier)
            random.shuffle(data)

            mean = sum(data) / len(data)
            sorted_data = sorted(data)
            median = sorted_data[len(sorted_data) // 2] if len(sorted_data) % 2 == 1 else \
                     (sorted_data[len(sorted_data) // 2 - 1] + sorted_data[len(sorted_data) // 2]) / 2

            # 3 different word problem contexts
            templates = [
                (
                    f"Sarah tracked the number of pages she read each day for a week: {data}. "
                    f"Calculate the mean number of pages read per day.",
                    "pages read per day"
                ),
                (
                    f"A store recorded the number of customers each hour: {data}. "
                    f"What is the mean number of customers per hour?",
                    "customers per hour"
                ),
                (
                    f"Test scores for a quiz were: {data}. "
                    f"Find the mean score.",
                    "test score"
                )
            ]

            problem_text, context = templates[variant]
            correct_answer = f"{mean:.1f}, but median ({median}) is more representative due to outlier"
            malrule_answer = f"{mean:.1f}"  # Just calculates mean without considering outlier

            return Problem(
                text=problem_text,
                operands=data,
                operation='statistical_interpretation',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'data': data,
                    'mean': mean,
                    'median': median,
                    'outlier': outlier,
                    'has_outlier': True,
                    'correct_answer': correct_answer,
                    'malrule_answer': malrule_answer,
                    'template': 'word_problem_context',
                    'is_word_problem': True,
                    'word_problem_type': formula_type,
                    'word_problem_variant': variant,
                    'context': context
                }
            )

        elif formula_type == 'compare_mean_median':
            # Generate data with outlier to compare measures
            cluster_size = random.randint(5, 7)
            cluster_center = random.randint(min_val, min(max_val // 8, 25))
            data = [cluster_center + random.randint(-3, 3) for _ in range(cluster_size)]
            # Add high outlier
            outlier = cluster_center * random.randint(4, 8)
            data.append(outlier)
            random.shuffle(data)

            mean = sum(data) / len(data)
            sorted_data = sorted(data)
            median = sorted_data[len(sorted_data) // 2] if len(sorted_data) % 2 == 1 else \
                     (sorted_data[len(sorted_data) // 2 - 1] + sorted_data[len(sorted_data) // 2]) / 2

            # 3 different word problem contexts
            templates = [
                (
                    f"Home prices in a neighborhood (in $1000s): {data}. "
                    f"Should a real estate agent use mean or median to describe typical home price?",
                    "home prices"
                ),
                (
                    f"Employee salaries at a small company (in $1000s): {data}. "
                    f"Which measure better represents a typical employee's salary: mean or median?",
                    "salaries"
                ),
                (
                    f"Daily commute times in minutes: {data}. "
                    f"Which measure of center is most appropriate: mean or median?",
                    "commute times"
                )
            ]

            problem_text, context = templates[variant]
            correct_answer = f"Median ({median}) is better; mean ({mean:.1f}) is distorted by outlier"
            malrule_answer = f"Mean ({mean:.1f}) is always the best measure"

            return Problem(
                text=problem_text,
                operands=data,
                operation='statistical_interpretation',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'data': data,
                    'mean': mean,
                    'median': median,
                    'outlier': outlier,
                    'has_outlier': True,
                    'correct_answer': correct_answer,
                    'malrule_answer': malrule_answer,
                    'template': 'word_problem_context',
                    'is_word_problem': True,
                    'word_problem_type': formula_type,
                    'word_problem_variant': variant,
                    'context': context
                }
            )

        elif formula_type == 'interpret_representativeness':
            # Generate data with outlier for representativeness evaluation
            cluster_size = random.randint(6, 8)
            cluster_center = random.randint(min_val, min(max_val // 10, 20))
            data = [cluster_center + random.randint(-2, 2) for _ in range(cluster_size)]
            # Add outlier
            outlier = cluster_center * random.randint(5, 12)
            data.append(outlier)
            random.shuffle(data)

            mean = sum(data) / len(data)
            sorted_data = sorted(data)
            median = sorted_data[len(sorted_data) // 2] if len(sorted_data) % 2 == 1 else \
                     (sorted_data[len(sorted_data) // 2 - 1] + sorted_data[len(sorted_data) // 2]) / 2

            # 3 different word problem contexts
            templates = [
                (
                    f"A teacher recorded homework completion times in minutes: {data}. "
                    f"The mean is {mean:.1f} minutes. Does this represent the typical time students spend?",
                    "homework times"
                ),
                (
                    f"Monthly rainfall amounts (in inches): {data}. "
                    f"The mean rainfall is {mean:.1f} inches. Is this representative of typical monthly rainfall?",
                    "rainfall amounts"
                ),
                (
                    f"Points scored per game by a basketball player: {data}. "
                    f"The mean is {mean:.1f} points. Does this accurately represent typical performance?",
                    "points per game"
                )
            ]

            problem_text, context = templates[variant]
            correct_answer = f"No, mean ({mean:.1f}) is not representative due to outlier ({outlier}). Median ({median}) better represents typical values."
            malrule_answer = f"Yes, mean ({mean:.1f}) represents the data"

            return Problem(
                text=problem_text,
                operands=data,
                operation='statistical_interpretation',
                level=self.level,
                difficulty=self.difficulty,
                metadata={
                    'data': data,
                    'mean': mean,
                    'median': median,
                    'outlier': outlier,
                    'has_outlier': True,
                    'correct_answer': correct_answer,
                    'malrule_answer': malrule_answer,
                    'template': 'word_problem_context',
                    'is_word_problem': True,
                    'word_problem_type': formula_type,
                    'word_problem_variant': variant,
                    'context': context
                }
            )
