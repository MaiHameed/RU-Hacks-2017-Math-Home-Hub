#Created by Dillium Chandrasiri, Mai Hameed, Anson Chan, Dan Stingaciu
import random
from flask import Flask
from flask_ask import Ask, question, statement
import json
import requests

app = Flask(__name__)
ask = Ask(app, "/")

total = 0
correct = 0
r1 = 0
r2 = 0


def randize():
    global r1
    global r2
    global r3
    r1 = random.randint(0, 10)
    r2 = random.randint(0, 10)
    r3 = random.randint(0, 2)


def addCorrect():
    global correct
    correct += 1


def addTotal():
    global total
    total += 1


@ask.launch
def start_skill():
    welcome_message = 'Are you ready for a quiz?'
    return question(welcome_message)


@ask.intent("yesIntent")
def ask_question():
    randize()
    if r3 == 0:
        askstring = "What is the answer to " + str(r1) + " plus " + str(r2) + " ?"
    elif r3 == 1:
        askstring = "What is the answer to " + str(r1) + " minus " + str(r2) + " ?"
    elif r3 == 2:
        askstring = "What is the answer to " + str(r1) + " times " + str(r2) + " ?"
    srt = "Okay, starting math quiz, to end, say stop. "
    lateanswer = "I'm sorry I didn't catch that, "
    return question(srt + askstring).reprompt(lateanswer + askstring)


@ask.intent("AnswerIntent", convert={'first': int})
def answer(first):
    addTotal()
    msg = 'Incorrect'
    if r3 == 0:
        if first == r1 + r2:
            msg = 'Correct'
            addCorrect()
    elif r3 == 1:
        if first == r1 - r2:
            msg = 'Correct'
            addCorrect()
    elif r3 == 2:
        if first == r1 * r2:
            msg = 'Correct'
            addCorrect()
    randize()
    if r3 == 0:
        askstring = " What is the answer to " + str(r1) + " plus " + str(r2) + " ?"
    elif r3 == 1:
        askstring = " What is the answer to " + str(r1) + " minus " + str(r2) + " ?"
    elif r3 == 2:
        askstring = " What is the answer to " + str(r1) + " times " + str(r2) + " ?"
    next = ". Okay, next question!"
    lateanswer = "I'm sorry I didn't catch that."
    return question(msg + next + askstring).reprompt(lateanswer + askstring)


@ask.intent('AMAZON.StopIntent')
def stop():
    Score = 'your score is' + str(correct) + 'out of' + str(total) + ". "
    return statement(Score + "Thanks for playing, goodbye!")


@ask.intent('EndIntent')
def stop():
    return statement("Maybe another time then, goodbye!")


@ask.session_ended
def session_ended():
    log.debug("Session Ended")
    return "", 200


if __name__ == '__main__':
    app.run(debug=True)
