#!/usr/bin/env python3

import json
import os.path
import requests
import browser_cookie3
from bardapi.constants import SESSION_HEADERS
from bardapi import Bard


bard = None
tokens = {}


# terminal colors
class Color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# extract bard cookie from browser
def get_tokens():
    global tokens
    
    tokens = {
        "__Secure-1PSID"   :  "",
        "__Secure-1PSIDTS" :  "",
        "__Secure-1PSIDCC" :  ""
    }

    cookies = list(browser_cookie3.chrome())

    for i, token in enumerate(cookies):    
        if '.google.com' == token.domain:
            if token.name in tokens:
                print(i, token.name, token.value) 
                tokens[token.name] = token.value

    with open('token.json', 'w') as file:
        json.dump(tokens, file)
        print(f"{Color.OKGREEN}success.. token.json created!{Color.ENDC}")
        


# create bard session from tokens
def set_session():
    global bard
    global tokens

    with open('token.json', 'r') as file:
        tokens = json.load(file)

    # create bard session from token
    session = requests.Session()
    session.headers = SESSION_HEADERS
    session.cookies.set("__Secure-1PSID", tokens["__Secure-1PSID"])
    session.cookies.set("__Secure-1PSIDTS", tokens["__Secure-1PSIDTS"])
    session.cookies.set("__Secure-1PSIDCC", tokens["__Secure-1PSIDCC"])    

    bard = Bard(token=tokens["__Secure-1PSID"], session=session)
    print(f"{Color.OKGREEN}success.. session instantiated!{Color.ENDC}")  


# check if token.json file exists
if not os.path.isfile('token.json'):
    print(f"{Color.WARNING}creating.. token.json{Color.ENDC}")
    get_tokens()

# try create the session
try:
    set_session()
except Exception as e:
    print(f"{Color.FAIL}{e}{Color.ENDC}")
    print(f"{Color.WARNING}resetting.. invalid token.json{Color.ENDC}")
    
    try: # recreate token 
        get_tokens()
        set_session()
    except Exception as e:
        print(f"{Color.FAIL}failed.. oh no!{Color.ENDC}")
        print(f"{Color.OKBLUE}This error would occur if cookies failed to extract from your browser. make sure that you have google bard logged and you're using Google Chrome. If all else failed, please submit an issue to github.com/ustp-core/lardx {Color.ENDC}")



print('\U0001F916 Bard:', bard.get_answer('why was git created in the first place?')['content'])
print(bard.conversation_id)


