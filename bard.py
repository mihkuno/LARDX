import os
import re
import time
import pickle
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



def bard_format(text):
    # Replace list with bullet points: * -> •
    text = re.sub(r'(?m)^\*\s+', r'• ', text)

    # Bold formatting: **word** -> \033[1mword\033[0m
    text = re.sub(r'\*\*(.*?)\*\*', r'\033[1m\1\033[0m', text)

    # Italic formatting: _word_ -> \033[3mword\033[0m
    text = re.sub(r'_(.*?)_', r'\033[3m\1\033[0m', text)

    # Underline formatting: ~word~ -> \033[4mword\033[0m
    text = re.sub(r'~(.*?)~', r'\033[4m\1\033[0m', text)

    # Bullet points: • word -> • word
    text = re.sub(r'• (.*?)\n', r'• \033[1m\1\033[0m\n', text)

    # Code block background formatting: ```code``` -> \033[42mcode\033[0m
    code_block_pattern = r'```(.*?)```'
    text = re.sub(code_block_pattern, r'\033[42m\1\033[0m', text, flags=re.DOTALL)

    return text


def print_stream(string_to_print, delay=0.005):
    formatted_string = bard_format(string_to_print)


    formatted_string = "Hello, World!"

    print('\U0001F916 Bard:', end=' ')
    for char in formatted_string:
        print(char, end='', flush=True)  # Setting end to '' to print without a newline
        time.sleep(delay)


def save_object(name, object):
    with open(name+'.pkl', "wb") as f:
        pickle.dump(object, f)


def load_object(name):
    with open(name+'.pkl', "rb") as f:
        return pickle.load(f)


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

        print(f"{Color.OKCYAN}success.. token retrieved{Color.ENDC}")
        return tokens

    except Exception as e:
        print(e)
        print(f"{Color.FAIL}failed..  token was not retrieved{Color.ENDC}")
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

    print(f"{Color.OKCYAN}success.. session created{Color.ENDC}")

    return token, session


def create_bard():
    # create bard session from token
    token, session = create_session() 

    bard = Bard(
        token = token,
        session = session,
    ) 
    # set the title of new conversation id
    # bard.get_answer('LARDX')
    print(f"{Color.OKGREEN}success.. new bard spawned{Color.ENDC}")

    return bard
    

def create_cache_directory():
    # create bard if cache not found
    if not os.path.isdir('cache'):
        os.mkdir('cache')
        return True
    
    return False


def check_cache_files():    
    if (
        os.path.isfile('cache/conversation_id.pkl') and
        os.path.isfile('cache/response_id.pkl') and
        os.path.isfile('cache/choice_id.pkl') and
        os.path.isfile('cache/proxies.pkl') and
        os.path.isfile('cache/SNlM0e.pkl')
    ):  
        return True
    else:
        print(f"{Color.WARNING}missing.. cache not found{Color.ENDC}")
        return False


def load_bard():
    try:
        token   = load_object('cache/token')
        session = load_object('cache/session')    
        bard    = Bard(token=token, session=session)
        print(f"{Color.OKGREEN}success.. bard respawned{Color.ENDC}")

    except Exception as e:
        print(f"{Color.WARNING}failed..  session expired{Color.ENDC}")
        token, session = create_session()
        bard = Bard(token=token, session=session)
    
    return bard


def load_cache(bard):
    try:
        bard.conversation_id = load_object('cache/conversation_id')
        bard.response_id     = load_object('cache/response_id')
        bard.choice_id       = load_object('cache/choice_id')
        bard.proxies         = load_object('cache/proxies')
        bard.SNlM0e          = load_object('cache/SNlM0e')
        print(f"{Color.OKCYAN}success.. history restored{Color.ENDC}")

    # TODO: make a recovery when cache is corrupted, instead of creating a new bard
    except Exception as e:
        print(f"{Color.WARNING}failed..  cache corrupted{Color.ENDC}")
