#!/usr/bin/env python3

import json

def repeat(c, n):
    r = ""
    for i in range(n):
        r = r + c
    return r

# Structure of the data
# {
#   "subject": "Maths",
#   "topic": "AddSubtract",
#   "questions": [
#     {
#       "question": "What is 24 + 3?",
#       "type": "choice",
#       "answer": {
#           "options": ["25", "26", "27", "28"],
#           "correct": "27"
#       }
#     },
#     {
#       "question": "What is 15 + 2?",
#       "type": "choice",
#       "answer": {
#           "options": ["16", "17", "18"],
#           "correct": "17"
#       }
#     }
#   ]
with open('questions.json') as json_file:
    try:
        data = json.load(json_file)

        print(data["subject"])
        print(repeat("-", len(data["subject"])))
        print(data["topic"])
        print(repeat("-", len(data["topic"])))

        questions = data["questions"]
        for question in questions:
            print("")
            print(question["question"])
            for i, option in enumerate(question["answer"]["options"], start=1):
                print(f"{i}: {option}")
            res = input("Answer: ")
            if res == question["answer"]["correct"]:
                print("You are correct!")
            else:
                print("That's not correct!")

    except:
        print("There is an error parsing the questions!")
    finally:
        print("You are done!")
