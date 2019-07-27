#!/usr/bin/env python3

import json
import sys
import time
import base64
import re
import os
import requests
import random

from os.path import join, dirname
from dotenv import load_dotenv

# Create .env file path.
dotenv_path = join(dirname(__file__), '.env')

# Load file from the path.
load_dotenv(dotenv_path)

def repeat(c, n):
    r = ""
    for i in range(n):
        r = r + c
    return r

def encode(data):
    encodedBytes = base64.b64encode(data.encode("utf-8"))
    encodedStr = str(encodedBytes, "utf-8")
    return encodedStr

def get_questions():
    url = os.getenv('s3url')
    try:
        r = requests.get(url, allow_redirects=True)
        open('questions.json', 'wb').write(r.content)
    except:
        print("Internet connection is down. Please check the Wifi modem!")
        sys.exit(1)

def banner(text):
    print(text)
    print(repeat("-", len(text)))

# Structure of the data
# [
#   {
#     "subject": "Science",
#     "disabled": "yes",
#     "topics": [
#       {
#         "topic": "Houses",
#         "questions": [
#           {
#             "question": "House on wheels is called ____",
#             "type": "choice",
#             "answer": {
#               "options": ["caravan", "houseboat", "stilt house", "building"],
#               "correct": "caravan"
#             }
#           }
#         ]
#       }
#     ]
#   },
#   {
#     "subject": "Maths",
#     "topics": [
#       {
#         "topic": "AddSubtract",
#         "questions": [
#           {
#             "question": "23 + 4 = ____",
#             "type": "choice",
#             "answer": {
#               "options": ["25", "26", "27", "28"],
#               "correct": "27"
#             }
#           }
#         ]
#       }
#     ]
#   }
# ]

def get_data():
    get_questions()
    with open('questions.json') as json_file:
        try:
            data = json.load(json_file)
        except:
            print("There is an error parsing the questions!")
            sys.exit()
        finally:
            return data

def ask_questions(data):
    random.shuffle(data)
    for item in data:
        if "disabled" in item:
            continue
        banner(item["subject"])
        for topic in item["topics"]:
            if "disabled" in topic:
                continue
            banner(topic["topic"])
            questions = topic["questions"]
            random.shuffle(questions)
            for question in questions:
                if "disabled" in question:
                    continue
                print("")
                banner(question["question"])
                options = question["answer"]["options"]
                random.shuffle(options)
                for i, option in enumerate(options, start=1):
                    print(f"{i}: {option}")
                res = check_answer(item["subject"], topic["topic"], question)
                print(res)

def post_activity(response):
    url = os.getenv('url')
    data = json.dumps(response)
    try:
        requests.post(url = url, data = data)
    except:
        print("Internet connection is down. Please check the Wifi modem!")
        sys.exit(1)

def prepare_response(subject, topic, start_time, request, response, correct, delta):
    data = {
        "sub_topic": f"{subject}-{topic}",
        "start_time": start_time,
        "request": request,
        "response": response,
        "correct": correct,
        "delta": delta
    }
    post_activity(data)
    return data

def check_answer(subject, topic, question):
    start_time = int(time.time())
    res = input("Answer: ")
    if res == question["answer"]["correct"]:
        correct = 'yes'
        print("You are correct!")
    else:
        correct = 'no'
        print("That's not correct!")
    end_time = int(time.time())
    return prepare_response(subject, topic, start_time, encode(question["question"]), encode(res), correct, (end_time - start_time))

data = get_data()
ask_questions(data)
