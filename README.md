# OneMinuteMath

This project recreates [One Minute Math](https://www.google.com/search?q=one+minute+math) worksheets that you might have seen in elementary or middle school.

The user can select the smallest and largest numbers to include in each problem (this option doesn’t apply to divisor problems) and how many problems to generate.

I wanted to learn the basics of calling LLMs via an API, so there is an option to generate the problems using Gemini; otherwise, the problems are generated randomly by an algorithm I wrote.

# Prerequisites

* Python installed on your device.
* 
  * I developed this with Python 3.10.6, and it **has not been tested with other versions**.
* [Google AI API key](https://ai.google.dev/gemini-api/docs/api-key?utm_source=PMAX&utm_medium=display&utm_campaign=Cloud-SS-DR-AIS-FY26-global-pmax-1713578&utm_content=pmax&gad_source=1&gad_campaignid=23417432327&gbraid=0AAAAACn9t67dqRcupEFuQbRG4l4KHaJRN&gclid=CjwKCAiAmp3LBhAkEiwAJM2JUNTQ-lZmxtdeObesx0r68i74A2dm6D8qekbLOuFBf_wy_eJyV5OO4hoCVjEQAvD_BwE)

  * This key should be stored in a `.env` file located in the root directory of this project. The file should look like:

```txt
GEMINI_API_KEY=your_key
```

# Setup

## Virtual Environment (Optional)

If you want to set up a virtual environment, follow these steps:
0. Open a terminal and navigate to the location you'd like it to be created.

1. Create a new venv (replace `venv_name` with your preferred name):

```bash
$ python3 -m venv venv_name
```

2. Activate the venv:

```bash
$ source path/to/venv/venv_name/bin/activate
```

Successful activation will show the venv name next to the terminal cursor:

```bash
(venv_name) $ _
```

## Install requirements

1. Navigate to the root directory of the project, then install the libraries in the `requirements.txt` file:

```bash
$ pip install -r requirements.txt
```

# Running the game

To run the game through a terminal, type:

```bash
python main.py
```

Or `python3` if `python` doesn't work.

Once running, the terminal will display:

```bash
Welcome to the One Minute Math Challenge!

You will have 60 seconds to solve as many problems as possible.
To quit at any time, press 'q'.
Enter your answer and press Enter.

Would you like Gemini (AI) to generate your answers? (y/n)
```

Then you can start solving problems. Example interaction:

```
$ python main.py                         

Welcome to the One Minute Math Challenge!

You will have 60 seconds to solve as many problems as possible.
To quit at any time, press 'q'.
Enter your answer and press Enter.

Would you like Gemini (AI) to generate your answers? (y/n) n
Enter the smallest number that can be used in each problem (Doesn't apply to divisors): 1
Enter the largest number that can be used in each problem (Doesn't apply to divisors): 10
Enter the number of problems you want to try and answer: 3

What operations do you want to be included?
    Enter any combination of
    - 'a' for addition
    - 's' for subtraction
    - 'm' for multiplication
    - 'd' for division
    (Ex. 'as' for addition and subtraction, or 'asmd' for all)
Operation(s): asmd
Display time left during the game? (y/n) n

Type 'start' when you're ready to start! start

9*2 = 18

8*3 = 24

9-9 = 0
You finished with 53.7 second(s) to spare!

====================

You got every problem right!!
```

# Known Issues / Limitations

* Only tested with Python 3.10.6. Other versions may not work correctly.
* Gemini API integration requires a valid API key and internet connection.
* I'm using the free tier of Gemini AI API, so I only get 20 requests a day.
* The minimum/maximum number selection does not apply to divisor problems.

# Citations

The code in the `_generate_random_divisor` method of `OneMinuteMathGenerator` was adapted from this article posted on GeeksForGeeks:
[find-all-factors-of-a-natural-number](https://www.geeksforgeeks.org/dsa/find-all-factors-of-a-natural-number/)