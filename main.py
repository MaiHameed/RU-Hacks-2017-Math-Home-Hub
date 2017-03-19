import random
from flask import Flask
from flask_ask import Ask, question, statement
import json
import requests

app = Flask(__name__)
ask = Ask(app, "/")

total=0
correct=0
r1 = 0
r2 = 0

def randize():
	global r1
	global r2
	r1 = random.randint(0,100)
	r2 = random.randint(0,100)

@ask.launch
def start_skill():
	welcome_message = 'Would you like to start a quiz?'
	return question (welcome_message)

@ask.intent("yesIntent")
def ask_question():
	randize()
	askstring = "Okay starting math quiz, whenever you want to quit just say quit. What is the answer to " + str(r1) + " plus " +  str(r2) 	+ " ?"
	reprompts = "I'm sorry I didn't catch that, What is the answer to " + str(r1) + " plus " +  str(r2) + " ?"
	return question(askstring).reprompt(reprompts)

@ask.intent("AnswerIntent", convert ={'first':int})
def answer(first):
	if first == r1+r2:
		msg = 'Correct!'
        	global correct
		correct+=1
    	else:
		msg = 'Incorrect'
    		global total
    		total+=1
	return statement(msg)
Score = 'your score is' + str(correct) + 'out of' + str(total)

@ask.intent('AMAZON.StopIntent')
def stop():
	return statement("Goodbye")

@ask.session_ended
def session_ended():
    log.debug("Session Ended")
    return "", 200

if __name__== '__main__':

	app.run(debug=True)
