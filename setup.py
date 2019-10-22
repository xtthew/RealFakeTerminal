#!/usr/bin/python3.5
import time
from environment import type_out, confirm_response

def get_name(userName):
    type_out("I'm curious though..") if userName != True else type_out("No worries, let's try that again!")
    type_out("What's your name?")
    return input(">> ")

def confirm_name(userName):
    type_out("Your name is " + userName + "? Is this correct?")
    nameConfirmation = input(">> ")
    nameSetConfirmation = True if confirm_response(nameConfirmation) != 0  else False
    return nameSetConfirmation