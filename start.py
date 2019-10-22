#!/usr/bin/python3.5
import setup, dialogue, terminal,sys,re
import environment as env
import subprocess as sp

tmp = sp.call('clear',shell=True)

env.type_out(dialogue.setup.hello)

nameSet = None
nameTyped = None
nameAttempts = 0
while (nameSet != True):
    if nameAttempts > 5:
        print(dialogue.errors.tooManytries)
        sys.exit()
    userName = setup.get_name(nameTyped)
    if userName.lower() == "ais":
        env.type_out("No, that's my name.. I want your name!")
    else:
        nameSet = setup.confirm_name(userName)
    nameTyped = True
    nameAttempts += 1
env.type_out("Alright "+userName+". It's nice to meet you! I'm loading the terminal now.")
env.type_out(". . . . . .")
userName = re.sub(' ', '',userName)
userName = userName[:10] if len(userName) > 10 else userName
tmp = sp.call('clear',shell=True)
env.type_out("To see a list of supported commands at this time type: help")
terminal.prompt(userName, "~")