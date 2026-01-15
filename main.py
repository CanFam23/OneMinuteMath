import os
import threading
import time

from dotenv import load_dotenv
from google.genai.errors import ClientError
import httpx

from OneMinuteMathGenerator import OneMinuteMathGenerator

# Max number of problems the user can try to answer
MAX_NUM_QUESTIONS = 250

MIN_NUM = -100
MAX_NUM = 100

# Time user has to answer questions
TIME_LIMIT_SECONDS = 60

# Abbreviations for operations
OPERATIONS = ["a", "s", "m", "d"]


def check_quit(user_input: str) -> None:
    """Exits the program if the given string is 'q'.

    Args:
        user_input (str): String to check
    """
    if user_input == 'q':
        print("You're really quiting?")
        os._exit(0)


def get_answers(start_time: float, problem_list: list[dict[str, str]], user_answers_list: list, display_time: bool) -> None:
    """Prompts the user for each question in the given problem list and adds their answer to `user_answers_list`.

    Args:
        start_time (float): Time the game started
        problem_list (list[dict[str,str]]): List of problems to ask user
        user_answers_list (list): List to add user's answer to
        display_time (bool): Whether to display the time left through the game or not
    """
    for problem in problem_list:
        print()
        if display_time:
            print(
                f"You have {round(TIME_LIMIT_SECONDS - (time.time() - start_time),1)} seconds remaining")
        try:
            user_answer = input(f"{problem['problem']} = ").strip()

            check_quit(user_answer)

            user_answers_list.append(user_answer)
        except:
            # I don't care if an error occurs, I want the program to keep running.
            pass


def main():
    load_dotenv()

    omm = OneMinuteMathGenerator()

    print()
    print("Welcome to the One Minute Math Challenge!")
    print()
    print("You will have 60 seconds to solve as many problems as possible.")
    print("To quit at any time, press 'q'.")
    print("Enter your answer and press Enter.")
    print()

    # Ask user if they want Gemini to generate their problems
    while True:
        llm_gen = input(
            "Would you like Gemini (AI) to generate your answers? (y/n) ").strip().lower()

        check_quit(llm_gen)

        if llm_gen not in ["y", "n"]:
            print("Please enter 'y' or 'n'")
        else:
            break

    # Get smallest number to use in problems
    while True:
        try:
            min_num = input(
                "Enter the smallest number that can be used in each problem (Doesn't apply to divisors): ").strip().lower()
            check_quit(min_num)

            min_num = int(min_num)

            if not (MIN_NUM <= min_num < MAX_NUM):
                print(
                    f"Smallest number must be between {MIN_NUM} and {MAX_NUM-1}")
            else:
                break
        except ValueError:
            print("Enter a number.")

    # Get largest number to use in problems
    while True:
        try:
            max_num = input(
                "Enter the largest number that can be used in each problem (Doesn't apply to divisors): ").strip().lower()

            check_quit(max_num)

            max_num = int(max_num)

            if max_num > min_num:
                break

            if not (MIN_NUM < min_num <= MAX_NUM):
                print(
                    f"Largest number must be between {MIN_NUM+1} and {MAX_NUM}")

            print(
                f"Largest number has to be greater than the smallest number ({min_num})")
        except ValueError:
            print("Enter a number.")

    # Get number of problems to generate
    while True:
        try:
            num_problems = input(
                "Enter the number of problems you want to try and answer: ")

            check_quit(num_problems)

            num_problems = int(num_problems)

            if not (0 < num_problems <= 250):
                print(
                    f"Must include at least one problem and no more than {MAX_NUM_QUESTIONS}")
            else:
                break
        except ValueError:
            print("Enter a number.")

    # Get operations to include
    while True:
        ops_input = input("""
What operations do you want to be included?
    Enter any combination of
    - 'a' for addition
    - 's' for subtraction
    - 'm' for multiplication
    - 'd' for division
    (Ex. 'as' for addition and subtraction, or 'asmd' for all)
Operation(s): """).strip().lower()
        check_quit(ops_input)

        ops_set = set(ops_input)

        if len(ops_set) == 0:
            print("Must choose at least one operation.")
            continue

        if not ops_set.issubset(set(OPERATIONS)):
            print("Please enter a combination of 'a', 's', 'm', and 'd'.")
        else:
            ops = list(ops_set)
            break

    # Ask user to display time during game or not
    while True:
        display_time_input = input(
            "Display time left during the game? (y/n) ").lower()

        check_quit(display_time_input)

        if display_time_input not in ["y", "n"]:
            print("Please enter 'y' or 'n'")
        else:
            display_time = True if display_time_input == "y" else False
            break

    if llm_gen == 'y':
        try:
            problems = omm.generate_problems_llm(
                min_num, max_num, num_problems, OPERATIONS)
        except ClientError:
            print()
            print(
                "Gemini has generated too many math problems today and needs a break :(")
            print(
                "Your problems will be generated by a State-of-the-art algorithm instead.")
            problems = omm.generate_problems(
                min_num, max_num, num_problems, ops)
        # If user has no internet connection
        except httpx.ConnectError:
            print()
            print("No internet connection found")
            print("Your problems will be generated by a State-of-the-art algorithm instead.")
            problems = omm.generate_problems(
                min_num, max_num, num_problems, ops)


        # Ensure problems is not empty
        if not problems:
            problems = omm.generate_problems(
                min_num, max_num, num_problems, ops)
    else:
        problems = omm.generate_problems(min_num, max_num, num_problems, ops)

    print()

    # Make sure user is ready
    while True:
        start = input(
            "Type 'start' when you're ready to start! ").strip().lower()

        check_quit(start)

        if start == "start":
            break

        print("Please enter 'start' to begin.")

    user_answers = []

    start_time = time.time()

    input_thread = threading.Thread(target=get_answers, args=(
        start_time, problems, user_answers, display_time))
    input_thread.daemon = True  # Allows program to exit even if thread is running
    input_thread.start()

    # Check if time is up as long as the input thread is alive
    while input_thread.is_alive():
        if time.time() - start_time >= TIME_LIMIT_SECONDS:
            print()
            print("Time's up!")
            # force the input thread to stop
            break
        time.sleep(0.1)  # prevents busy waiting

    # Show user how much time they had left (If they had any)
    if time.time() - start_time < TIME_LIMIT_SECONDS:
        print(
            f"You finished with {round(TIME_LIMIT_SECONDS - (time.time() - start_time),1)} second(s) to spare!")

    num_correct = 0
    incorrect_problems = []

    # Count how many problems the user got right
    for i, ua in enumerate(user_answers):
        answer = int(problems[i]["answer"])

        try:
            if int(ua.strip()) == answer:
                num_correct += 1
            else:
                incorrect_problems.append({"problem": problems[i]["problem"], "user_answer": int(
                    ua), "answer": problems[i]["answer"]})
        # If the input is not a number
        except ValueError:
            incorrect_problems.append(
                {"problem": problems[i]["problem"], "user_answer": ua, "answer": problems[i]["answer"]})

    print()
    print("="*20)
    print()

    if num_correct == len(problems):
        print("You got every problem right!!")
    elif num_correct == 0:
        print("You didn't get any problems right...")
    elif num_correct == 1:
        print("You only got 1 problem right, better than 0 right?")
    else:
        print(f"Overall, you got {num_correct} problem(s) correct!")

    if len(user_answers) != num_correct:
        if num_correct != 0:
            print(
                f"You got {len(user_answers) - num_correct} problem(s) incorrect.")
        print()
        print("Problems you got incorrect:")

        for p in incorrect_problems:
            print(
                f"{p['problem']} = {p['answer']}, you answered: {p['user_answer']}")
            print()

    if len(problems) != len(user_answers):
        print(
            f"You didn't have time to answer {len(problems) - len(user_answers)} problem(s).")


if __name__ == "__main__":
    main()
