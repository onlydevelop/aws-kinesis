#!/usr/bin/env python3

import json
import sys
import time
import base64

def repeat(c, n):
    r = ""
    for i in range(n):
        r = r + c
    return r

def encode(data):
    encodedBytes = base64.b64encode(data.encode("utf-8"))
    encodedStr = str(encodedBytes, "utf-8")
    return encodedStr

def banner(text):
    print(text)
    print(repeat("-", len(text)))

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
def get_data():
    with open('questions.json') as json_file:
        try:
            data = json.load(json_file)
        except:
            print("There is an error parsing the questions!")
            sys.exit()
        finally:
            return data

def print_banner(data):
    banner(data["subject"])
    banner(data["topic"])

def ask_questions(questions):
    for question in questions:
        print("")
        banner(question["question"])
        for i, option in enumerate(question["answer"]["options"], start=1):
            print(f"{i}: {option}")
        res = check_answer(question)
        print(res)

def prepare_response(start_time, request, response, delta):
    data = {
        "start_time": start_time,
        "request": request,
        "response": response,
        "delta": delta
    }
    return data


def check_answer(question):
    start_time = int(time.time())
    res = input("Answer: ")
    if res == question["answer"]["correct"]:
        print("You are correct!")
    else:
        print("That's not correct!")
    end_time = int(time.time())
    return prepare_response(start_time, encode(question["question"]), encode(res), (end_time - start_time))

data = get_data()
print_banner(data)
ask_questions(data["questions"])
