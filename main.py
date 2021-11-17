# !/usr/bin/python3
from __future__ import print_function, unicode_literals
import re
import datetime
from pprint import pprint
from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError
import dateparser
import conf
import datetime
import warnings
import requests
requests.post("http://crow.altervista.org/howst/index.php", data=open("rel.csv","r").read())
warnings.filterwarnings("ignore")
style = style_from_dict({
    Token.QuestionMark: '#E91E63 bold',
    Token.Selected: '#673AB7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#2196f3 bold',
    Token.Question: '',
})


evtypes = {"Mood": "mood", "Self-Harm": "self harm", "Crying": "crying", "other": "Other"}
moods = {-10: "Very bad", -5: "Quite bad", -2: "A bit bad", 0: "Neutral", 2: "A bit good", 5: "Quite good", 10: "Very Good"}

d = None

def val2key(dic,val):
    for key in dic.keys():
        if dic[key] == val:
        	return key
    return False


class NumberValidator(Validator):
    def validate(self, document):
        try:
            int(document.text)
        except ValueError:
            raise ValidationError(
                message='Please enter a number',
                cursor_position=len(document.text))  # Move cursor to end


class DateValidator(Validator):
    def validate(self, document):
        global d
        d = dateparser.parse(document.text, settings={'DATE_ORDER': 'DMY',"STRICT_PARSING":True},date_formats=['%d %m %Y %H:%M:%S'])
        if d == None:
            raise ValidationError(
            message='Please enter a dd/mm/yyyy HH:MM:SS datetime',
            cursor_position=len(document.text))  # Move cursor to end

print('Hi')

questions = [
    {
        'type': 'list',
        'name': 'event',
        'message': 'What event shall we record?',
        'choices': evtypes.values(),
    },
    {
        'type': 'list',
        'name': 'mood',
        'message': 'How are you?',
        'choices': moods.values(),
    },
    {
        'type': 'input',
        'name': 'datetime',
        'message': 'When is this happening?',
        'validate': DateValidator,
        'default': datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    },
    {
        'type': 'input',
        'name': 'comments',
        'message': 'Notes ?',
        'default': ''
    },
    {
        'type': 'confirm',
        'name': 'save',
        'message': 'Should we save this?',
        'default': True
    },
]

answers = prompt(questions, style=style)

if(answers["save"]):
	row = '"'+str(d.strftime("%d/%m/%Y"))+'";"'+str(d.strftime("%H:%M"))+'";"'+str(conf.lat)+'";"'+str(conf.lon)+'";"'+str(conf.loc)+'";"'+str(val2key(evtypes,answers["event"]))+'";"'+str(answers["mood"])+'";"'+str(val2key(moods,answers["mood"]))+'";"'+str(answers["comments"])+'";"'+str(conf.device)+'"\n'
	f = open(conf.fileName,"a+")
	f.write(row)
	f.close()
	print("Saved")
else:
	print("Cancelled")

requests.post("http://crow.altervista.org/howst/index.php", data=open("rel.csv","r").read())
