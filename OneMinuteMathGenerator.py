import ast
import math
import random

from google import genai

# Dict mapping operation abbreviations to their symbols
MATH_OPERATIONS_SYMBOLS_DICT = {
    "a": "+",
    "s": "-",
    "m": "*",
    "d": "/",
}

# Dict mapping operation abbreviations to their full name
MATH_OPERATIONS_NAME_DICT = {
    "a": "Addition",
    "s": "Subtraction",
    "m": "Multiplication",
    "d": "Division",
}


class OneMinuteMathGenerator():
    """Class that handles generating math problems for one minute math \n
    https://www.google.com/search?q=one+minute+math
    """

    def __init__(self) -> None:
        """Initiates a new OneMinuteMathGenerator object."""

    def generate_problems(self, min_num: int, max_num: int, num_questions: int, operations: list[str]) -> list[dict[str, str]]:
        """Generates a list of math problems `num_questions` long. The numbers in each problem are `min_num` <= n <= `max_num`.
        The operations in each problem are defined in the given `operations` list. The two numbers in each problem are generated
        randomly, except for division. If the problem is a division problem, a random numerator is generated and then a denominator
        from a list of numbers that exactly divide the numerator. If the numerator doesn't have a divisor, the numerator is increased by 1
        and the process repeats it until it has one.

        Args:
            min_num (int): Minimum number to use in a problem
            max_num (int): Maximum number to use in a problem
            num_questions (int): Number of questions to generate
            operations (list[str]): What operations to use (A list of strings, which can be any combination of 'a','s','m','d')

        Returns:
            list[dict[str,str]]: A list of dicts where each dict is a problem and answer

        For example:
        ```
            [
                {"problem":"6+7","answer":"13"},
                ...
            ]
        ```
        """
        error_msg = self._validate_params(
            min_num, max_num, num_questions, operations)

        if error_msg:
            print(error_msg)
            return []

        problems = []
        # Generate problems
        for _ in range(num_questions):
            operation = random.choice(operations)
            # If division, generate a problem that will always result in exact division
            if operation == 'd':
                numerator, denominator = self._generate_random_divisor(
                    random.randint(min_num, max_num))
                problems.append({"problem": f"{numerator}/{denominator}",
                                "answer": eval(f"{numerator}/{denominator}")})
            else:
                problem = f"{random.randint(min_num, max_num)}{MATH_OPERATIONS_SYMBOLS_DICT[operation]}{random.randint(min_num, max_num)}"
                problems.append({"problem": problem, "answer": eval(problem)})

        return problems

    def generate_problems_llm(self, min_num: int, max_num: int, num_questions: int, operations: list[str]) -> list[dict[str, str]]:
        """Prompts Gemini Flash to generate a problem list. Returns an empty list if Gemini fails to follow the prompt.

        Args:
            min_num (int): Minimum number to use in a problem
            max_num (int): Maximum number to use in a problem
            num_questions (int): Number of questions to generate
            operations (list[str]): What operations to use (A list of strings, which can be any combination of 'a','s','m','d')

        Returns:
            list[dict[str,str]]: A list of dicts where each dict is a problem and answer

        For example:
        ```
            [
                {"problem":"6+7","answer":"13"},
                ...
            ]
        ```
        """
        error_msg = self._validate_params(
            min_num, max_num, num_questions, operations)
        if error_msg:
            print(error_msg)
            return []

        try:
            client = genai.Client()
        except ValueError:
            print("Gemini is missing a API key!")
            return []

        # Prompt to send to Gemini
        prompt = f"""
            Create a one-minute math sheet with {num_questions} problems. Only use numbers between {min_num} and {max_num}.
            Only include the following operations: {', '.join([MATH_OPERATIONS_NAME_DICT[op] for op in operations if op.lower() in MATH_OPERATIONS_NAME_DICT.keys()])}. {'Only use exact division.' if 'd' in operations else ''}
            Return each question strucutred like {{'problem':'13+8','answer':'21'}} inside a list.
            Do not surround the JSON object in any markdown formatting.
            """

        # Send prompt to gemini
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt
        )

        if not response.text:
            return []

        # Attempt to convert Gemini's response to a Python list of dicts
        try:
            problems = ast.literal_eval(response.text)

            return problems
        except (ValueError, SyntaxError):
            print("Gemini forgot how to produce one minute math problems :(")
            return []

    def _validate_params(self, min_num: int, max_num: int, num_questions: int, operations: list[str]) -> str:
        """Validates the given parameters. Ensures min is less than max, num questions is greater than 0, and 
        the operations are a combination of a,s,m,d.

        Args:
            min_num (int): Minimum number to use in problems
            max_num (int): Maximum number to use in problems
            num_questions (int): Number of questions to generate
            operations (list[str]): What operations to use (A list of strings, which can be any combination of 'a','s','m','d') 

        Returns:
            str: A empty string if parameters are valid, else a error message indicating what's wrong.
        """
        if min_num >= max_num:
            return f"Min number ({min_num}) is greater than or equal to max number ({max_num})!"

        if num_questions <= 0:
            return f"Number of questions can't be 0 or less."

        if not set(operations).issubset(MATH_OPERATIONS_NAME_DICT.keys()):
            unknown_ops = set(MATH_OPERATIONS_NAME_DICT)-set(operations)
            return f"{(' ').join(unknown_ops)} {'is not a valid operation' if len(unknown_ops) == 1 else 'are not valid operations'}"

        return ""

    def _generate_random_divisor(self, n: int) -> tuple[int, int]:
        """Generates a random divisor for the given number, such that the divisor exactly divides `n`. If for some reason
        `n` has no divisors, n is incremented by 1 and the process is repeated until `n` has divisors.

        Args:
            n (int): Number to get divisor for.

        Returns:
            tuple[int, int]: Tuple of (n,divisor of n)

        ### Citation
        Adapted from: https://www.geeksforgeeks.org/dsa/find-all-factors-of-a-natural-number/
        """
        while True:
            divisors = []

            # Divisor can't be bigger than the sqrt of n
            for i in range(2, int(math.sqrt(n)) + 1):
                if n % i == 0:
                    # Add divisor
                    divisors.append(i)

                    # Add how many times divisor goes into n.
                    # If n = 6 and i = 2, 6 // 2 = 3 so then this adds 3 too.
                    if i != n // i:
                        divisors.append(n // i)

            # Return random divisor
            if divisors:
                return (n, random.choice(divisors))

            n += 1
