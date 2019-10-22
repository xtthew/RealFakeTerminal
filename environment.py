#!/usr/bin/python3.5
import time

def type_out(type_text):
    type_text = list(type_text)
    for letter in type_text:
        print(letter, end = '', flush=True)
        time.sleep(0.075) #set to .075
    print('')

def confirm_response(response):
    response = response.lower()
    yesArray = ["yes", "yeah", "ok", "o.k.", "alright", "fine", "yup"]
    noArray = ["no", "don't", "dont"]
    if any(c in response for c in yesArray):
        x = 1
    elif any(c in response for c in noArray):
        x = 0
    else:
        x = 2
    return x