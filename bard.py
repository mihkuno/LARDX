#!/usr/bin/env python3

import time
import pickle
import os, sys
import requests
import browser_cookie3
from bardapi.constants import SESSION_HEADERS
from bardapi import Bard


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


def save_object(name, object):
    with open(name+'.pkl', "wb") as f:
        pickle.dump(object, f)


def load_object(name):
    with open(name+'.pkl', "rb") as f:
        return pickle.load(f)


def print_stream(string_to_print, delay=0.003):
    print('\U0001F916 Bard:', end=' ')
    for char in string_to_print:
        print(char, end='', flush=True)  # Setting end to '' to print without a newline
        time.sleep(delay)


def save_cache(bard):
    save_object('cache/token', bard.token)
    save_object('cache/session', bard.session)
    save_object('cache/conversation_id', bard.conversation_id)
    save_object('cache/response_id', bard.response_id)
    save_object('cache/choice_id', bard.choice_id)
    save_object('cache/proxies', bard.proxies)
    save_object('cache/SNlM0e', bard.SNlM0e)
    
  
# extract bard cookie from browser
def retrieve_tokens():
    tokens = {
        "__Secure-1PSID"   :  "",
        "__Secure-1PSIDTS" :  "",
        "__Secure-1PSIDCC" :  ""
    }

    try:
        cookies = list(browser_cookie3.chrome())

        for i, token in enumerate(cookies):    
            if '.google.com' == token.domain:
                if token.name in tokens:
                    tokens[token.name] = token.value

        print(f"{Color.OKGREEN}success.. token retrieved!{Color.ENDC}")
        return tokens

    except Exception as e:
        print(e)
        print(f"{Color.FAIL}failed.. token was not retrieved{Color.ENDC}")
        return False


# create session from tokens
def create_session():
    tokens = retrieve_tokens()

    session = requests.Session()
    session.headers = SESSION_HEADERS
    session.cookies.set("__Secure-1PSID", tokens["__Secure-1PSID"])
    session.cookies.set("__Secure-1PSIDTS", tokens["__Secure-1PSIDTS"])
    session.cookies.set("__Secure-1PSIDCC", tokens["__Secure-1PSIDCC"])    

    token = tokens["__Secure-1PSID"]

    print(f"{Color.OKGREEN}success.. session created!{Color.ENDC}")

    return token, session


def create_bard():
    # create bard session from token
    token, session = create_session() 

    try:
        bard = Bard(
            token = token,
            session = session,
        ) 

        # set the title of new conversation id
        bard.get_answer('LARDX')
        
        print(f"{Color.OKGREEN}success.. a new bard spawned!{Color.ENDC}")
        return bard  

    except Exception as e:
        print(e)
        print(f"{Color.FAIL}failed.. invalid session{Color.ENDC}")



def prompt_bard(prompt):

    bard = None

    # create bard if cache not found
    if not os.path.isdir('cache'):
        os.mkdir('cache')
        bard = create_bard()

    else:
        try:
            conversation_id = load_object('cache/conversation_id')
            response_id     = load_object('cache/response_id')
            choice_id       = load_object('cache/choice_id')
            proxies         = load_object('cache/proxies')
            SNlM0e          = load_object('cache/SNlM0e')
            print(f"{Color.OKGREEN}success.. history restored{Color.ENDC}")

        except Exception as e:
            print(e)
            print(f"{Color.WARNING}failed.. cache is corrupted{Color.ENDC}")
            bard = create_bard()

        else: # run if preceeeding try statement has no exceptions
            try:
                token   = load_object('cache/token')
                session = load_object('cache/session')
                bard    = Bard(token=token, session=session)
            except Exception as e:
                print(e)
                print(f"{Color.WARNING}failed.. session expired{Color.ENDC}")
                token, session = create_session()
                bard = Bard(token=token, session=session)

            bard.conversation_id = conversation_id
            bard.response_id     = response_id
            bard.choice_id       = choice_id
            bard.proxies         = proxies
            bard.SNlM0e          = SNlM0e

            print(f"{Color.OKGREEN}success.. bard respawned!{Color.ENDC}")
    
    message = bard.get_answer(prompt.strip())['content']

    save_cache(bard)

    return message


print_stream(prompt_bard("can you underline this text... hello world"))