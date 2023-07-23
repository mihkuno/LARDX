import os
import re
import time
import pickle
from queue import Queue
from threading import Thread
import requests
import browser_cookie3
from bardapi import Bard
from rich.console import Console
from bardapi.constants import SESSION_HEADERS


_LOG_STACK = []
_DISPLAY_LOG = False


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



def dir(file_path):
    return os.path.join(
        os.path.dirname(__file__),
        file_path
    )


def bard_format(text):
    # Replace list with bullet points: * -> •
    text = re.sub(r'(?m)^\*\s+', r'• ', text)

    # Bold formatting: **word** -> \033[1mword\033[0m
    text = re.sub(r'\*\*(.*?)\*\*', r'\033[1m\1\033[0m', text)

    # Italic formatting: _word_ -> \033[3mword\033[0m
    text = re.sub(r'_(.*?)_', r'\033[3m\1\033[0m', text)

    # Italic formatting: *word* -> \033[3mword\033[0m
    text = re.sub(r'\*(.*?)\*', r'\033[3m\1\033[0m', text)

    # Underline formatting: ~word~ -> \033[4mword\033[0m
    text = re.sub(r'~(.*?)~', r'\033[4m\1\033[0m', text)

    # Bullet points: • word -> • word
    text = re.sub(r'• (.*?)\n', r'• \033[1m\1\033[0m\n', text)

    # Code block background formatting: ```code``` -> \033[42mcode\033[0m
    code_block_pattern = r'```(.*?)```'
    text = re.sub(code_block_pattern, r'\033[42m\1\033[0m', text, flags=re.DOTALL)

    return text


def output_stream(string_to_print, delay=0.005):
    formatted_string = bard_format(string_to_print)
    for char in formatted_string:
        print(char, end='', flush=True)  # Setting end to '' to print without a newline
        time.sleep(delay)
    print('\n')


def save_object(name, object):
    with open(dir(f'.cache/{name}.pkl'), "wb") as f:
        pickle.dump(object, f)


def load_object(name):
    with open(dir(f'.cache/{name}.pkl'), "rb") as f:
        return pickle.load(f)


def save_cache(bard):
    save_object('bard', bard)
    save_object('token', bard.token)
    save_object('session', bard.session)
    save_object('conversation_id', bard.conversation_id)
    save_object('response_id', bard.response_id)
    save_object('choice_id', bard.choice_id)
    save_object('proxies', bard.proxies)
    save_object('SNlM0e', bard.SNlM0e)
    output(f"{Color.OKCYAN}Saving Cache..{Color.ENDC}")


def retrieve_browser_cookie():
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

        output(f"{Color.OKCYAN}Token Retrieved..{Color.ENDC}")
        return tokens

    except Exception as e:
        output(f"{Color.FAIL}Token Abandoned..{Color.ENDC}")
        return False


def create_session():
    tokens = retrieve_browser_cookie()

    session = requests.Session()
    session.headers = SESSION_HEADERS
    session.cookies.set("__Secure-1PSID", tokens["__Secure-1PSID"])
    session.cookies.set("__Secure-1PSIDTS", tokens["__Secure-1PSIDTS"])
    session.cookies.set("__Secure-1PSIDCC", tokens["__Secure-1PSIDCC"])    

    token = tokens["__Secure-1PSID"]

    output(f"{Color.OKCYAN}Session Created..{Color.ENDC}")
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

    output(f"{Color.OKGREEN}Object Created..{Color.ENDC}")


    return bard


def check_cache_files():
    
    def exists(path):
        return os.path.isfile(
            dir('.cache/'+path))
    
    if (
        exists('conversation_id.pkl') and
        exists('response_id.pkl') and
        exists('choice_id.pkl') and
        exists('proxies.pkl') and
        exists('SNlM0e.pkl')
    ):  
        return True
    
    else:
        output(f"{Color.WARNING}Missing Cache..{Color.ENDC}")
        return False


def load_bard():
    output(f"{Color.OKGREEN}Object Loaded..{Color.ENDC}")
    return load_object('bard')


def load_session():
    try:
        token   = load_object('token')
        session = load_object('session')    
        bard    = Bard(token=token, session=session)
        output(f"{Color.OKGREEN}Session Restored..{Color.ENDC}")


    except Exception as e:
        token, session = create_session()
        bard = Bard(token=token, session=session)
        output(f"{Color.WARNING}Session Expired..{Color.ENDC}")
        return bard


def load_cache(bard):
    try:
        bard.conversation_id = load_object('conversation_id')
        bard.response_id     = load_object('response_id')
        bard.choice_id       = load_object('choice_id')
        bard.proxies         = load_object('proxies')
        bard.SNlM0e          = load_object('SNlM0e')
        output(f"{Color.OKCYAN}History Restored..{Color.ENDC}")
    # TODO: make a recovery when cache is corrupted, instead of creating a new bard
    except Exception as e:
        output(f"{Color.WARNING}Corrupted Cache..{Color.ENDC}")


def output(text):
    global _LOG_STACK, _DISPLAY_LOG
    if _DISPLAY_LOG:
        print(text)
    else:
        _LOG_STACK.append(text)


def show_log_stack():
    global _DISPLAY_LOG, _LOG_STACK
    
    _DISPLAY_LOG = True
    
    for _log in _LOG_STACK:
        print(_log)


def main():
    global _LOG_STACK, _DISPLAY_LOG
    queue = Queue()


    def _init():
        bard = None

        # TODO: make a recovery when cache is corrupted, instead of creating a new bard
        
        # create the cache folder, don't create if it exists
        os.makedirs(
            os.path.join(
                os.path.dirname(__file__), '.cache/'), 
            exist_ok=True)
        
        # check if cache files are missing
        if not check_cache_files():
            # create a new bard instance
            bard = create_bard()   

        else:
            # use previous bard object
            try:
                bard = load_bard()

            # create new bard but, use cache of previous bard
            except:
                bard = load_session()
                load_cache(bard)

        return bard


    def _thread():
        bard = _init()
        queue.put(bard)    


    thread = Thread(target=_thread)

    response = ""

    try:        
        # get user input
        thread.start()
        user_input = input('\U0001F50E: ').strip()
        
        console = Console()

        with console.status(f"{Color.HEADER}Loading..{Color.ENDC}") as log:
            bard = queue.get()

            # get bard response
            log.update(f"{Color.HEADER}Querying..{Color.ENDC}")

            response = '\U0001F4EB: '
            response += bard.get_answer(user_input)['content']   

            # could be captcha
            if "Response Error:" in response[:20]:
                output(f"{Color.FAIL}Response Blocked..{Color.ENDC}")
                log.update(f"{Color.WARNING}Regenerating..{Color.ENDC}")
                
                bard = create_bard()
                response =  f"{Color.HEADER}*Cache was reset due to response traffic..*\n\n{Color.ENDC}"
                response += '\U0001F4EB: '
                response += bard.get_answer(user_input)['content']               

        output_stream(response)
        save_cache(bard)
        
        
        # uncomment to show debug logs
        # show_log_stack()

    except requests.exceptions.ConnectionError as e:
        output(f"{Color.FAIL}Connection Failed..{Color.ENDC}")

    except KeyboardInterrupt:
        output(f"{Color.OKBLUE}{Color.BOLD}Connection Closed..{Color.ENDC}")


if __name__ == "__main__":
    main()