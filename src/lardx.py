import os, re, time
import pickle
import browser_cookie3
import requests
from rich.console import Console
from bardapi.constants import SESSION_HEADERS
from bardapi import Bard
from threading import Thread
from queue import Queue


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
    

class Stream:
    def __init__(self, string, end = None):
        self.__print(string, end)    
    
        
    def __format(self, text):
        # Extract code blocks and store them in a list
        code_blocks = []
        def extract_code_block(match):
            code_blocks.append(match.group())
            return f"<codeblock{len(code_blocks) - 1}>"

        # Code block formatting: ```(language)\n code ``` -> <codeblock0>
        code_block_pattern = r'```(.*?)```'
        text = re.sub(code_block_pattern, extract_code_block, text, flags=re.DOTALL)

        # Single backticks formatting: `word` -> <backtick0>
        backtick_pattern = r'`([^`]+)`'  # Modified pattern to avoid matching backticks
        text = re.sub(backtick_pattern, rf'{Color.HEADER}\1{Color.ENDC}', text)

        # Bold formatting: **word** -> \033[1mword\033[0m (with backtick exclusion)
        text = re.sub(r'(?<!`)\*\*((?:(?!\*\*).)*)\*\*(?!`)', f'{Color.BOLD}\\1{Color.ENDC}', text)

        # Italic formatting: _word_ -> \033[3mword\033[0m (with backtick exclusion)
        text = re.sub(r'(?<!`|_)_((?:(?!_).)*)_(!`|_)', f'{Color.UNDERLINE}\\1{Color.ENDC}', text)

        # Underline formatting: __word__ -> \033[4mword\033[0m (with backtick exclusion)
        text = re.sub(r'(?<!`)__([^_]+)__(?!`)', f'{Color.UNDERLINE}\\1{Color.ENDC}', text)

        # Replace bullet points with •
        text = re.sub(r'(?m)^\* ', '• ', text)

        # Re-insert code blocks with their own formatting
        for i, code_block in enumerate(code_blocks):
            code_content = re.search(r'```(?:.*?)\n(.*?)```', code_block, flags=re.DOTALL).group(1)
            language = re.search(r'```(.*?)\n', code_block).group(1).strip()

            # Format code block content and language
            formatted_content = f"{Color.OKCYAN}{code_content}{Color.ENDC}"
            formatted_language = f"{Color.BOLD}{language}{Color.ENDC}"
            code_block_formatted = f"{formatted_language}\n{'-' * 50}\n{formatted_content}{'-' * 50}\n"

            # Replace code block placeholder with formatted code block
            text = text.replace(f"<codeblock{i}>", code_block_formatted)

        return text
    
    
    def __print(self, string, end, delay=0.005):
        for char in self.__format(string):
            print(char, end='', flush=True)
            time.sleep(delay)
            
        if end == None: print('')
        else:           print('', end=end) 


class Profile:
    def __init__(self):
        self.path_list   = self.__chrome_linux()
        self.cookie_file = ''

        Stream('\n')
                
        if not self.path_list:
            Stream(f"{Color.FAIL}Lookes like there aren't any chrome users found :({Color.ENDC}")
            exit()
            
        elif len(self.path_list) == 1:
            self.cookie_file = self.path_list[0] + '/Cookies' 

        else:
            Stream(f'{Color.OKBLUE}chrome://version{Color.ENDC} on the url to find your chrome profile directory\n')
            
            for idx, path in enumerate(self.path_list, 1):
                Stream(f"{Color.OKGREEN}{idx}.{Color.ENDC} {path}")
                        
            while True:
                try:
                    Stream(f"\n{Color.HEADER}Select a profile to log in Bard's cookies: {Color.ENDC}{Color.OKGREEN}", end = '')
                    option = int(input())
                    Stream(Color.ENDC)
                    
                    if 1 <= option <= len(self.path_list):
                        selected_path    = self.path_list[option - 1]
                        self.cookie_file = selected_path + '/Cookies'
                        break
                    
                    else:
                        Stream(f"{Color.WARNING}Invalid option. Please select a valid number.{Color.ENDC}")
                        
                except ValueError:
                    Stream(f"{Color.WARNING}Invalid input. Please enter a number.{Color.ENDC}")
                    
            
    def __chrome_linux(self):
        # Find paths and store them in a list
        paths = []

        # Option 1
        default_path = os.path.expanduser("~/.config/google-chrome/Default")
        if os.path.exists(default_path) and os.path.isdir(default_path):
            paths.append(default_path)

        # Option 2
        profile_paths = [p for p in os.listdir("/home/mihkuno/.config/google-chrome/") if p.startswith("Profile")]
        for profile_path in profile_paths:
            profile_path = os.path.join("/home/mihkuno/.config/google-chrome/", profile_path)
            if os.path.exists(profile_path) and os.path.isdir(profile_path):
                paths.append(profile_path)

        # Option 3
        default_var_path = os.path.expanduser("~/.var/app/com.google.Chrome/config/google-chrome/Default")
        if os.path.exists(default_var_path) and os.path.isdir(default_var_path):
            paths.append(default_var_path)

        # Option 4
        profile_var_paths = [p for p in os.listdir("/home/mihkuno/.var/app/com.google.Chrome/config/google-chrome/") if p.startswith("Profile")]
        for profile_var_path in profile_var_paths:
            profile_var_path = os.path.join("/home/mihkuno/.var/app/com.google.Chrome/config/google-chrome/", profile_var_path)
            if os.path.exists(profile_var_path) and os.path.isdir(profile_var_path):
                paths.append(profile_var_path)

        return paths


class Cache:
    
    @classmethod
    def init(cls):
        # create cache folder if not exists
        os.makedirs(
            os.path.join(
                os.path.dirname(__file__), '.cache/'), 
            exist_ok=True)

    @classmethod
    def __path(cls, name):
        """
        Get the absolute path of this file's directory
        """
        return os.path.join(os.path.dirname(__file__), name)    
    
    @classmethod
    def __save(cls, name, object):
        with open(cls.__path('.cache/'+name+'.pkl'), "wb") as f:
            pickle.dump(object, f)

    @classmethod
    def __load(cls, name):
        with open(cls.__path('.cache/'+name+'.pkl'), "rb") as f:
            return pickle.load(f)

    @classmethod
    def __exists(cls, name):
        return os.path.exists(
            cls.__path('.cache/'+name+'.pkl'))

    @classmethod
    def save(cls, bard):
        cls.__save('bard', bard)
        cls.__save('profile', bard.profile)

    @classmethod
    def exists(cls):        
        if (
            cls.__exists('profile') and
            cls.__exists('bard')
        ):  
            return True
        return False

    @classmethod
    def load(cls, filename):
        return cls.__load(filename)


class Lardx(Bard):
    
    def __init__(self, cookie_file=''):
        self.profile  = cookie_file     
        self.token, self.session = self.__session(self.profile)
        super().__init__(token=self.token, session=self.session)

    
    def ask(self, string):
        try:
            message = self.get_answer(string)['content']
            
        except:
            print('looks like the session is expired... refreshing cookies')
            self.token, self.session = self.__session(self.cookie_file)
            message = self.get_answer(string)['content']
            
        return message
    
    
    def __session(self, cookie_file):
        try:
            cookie_names = ["__Secure-1PSID", "__Secure-1PSIDTS", "__Secure-1PSIDCC"]
            cookie_list  = []
            cookie_json  = {}
            
            # get updated cookies
            if cookie_file:
                cookie_list = list(browser_cookie3.chrome(cookie_file=cookie_file, domain_name='.google.com'))
            else:
                cookie_list = list(browser_cookie3.chrome(domain_name='.google.com'))  
            
            for cookie in cookie_list:
                if cookie.name in cookie_names:
                    cookie_json[cookie.name] = cookie.value
                    
            # create the session
            token = cookie_json["__Secure-1PSID"]
            session = requests.Session()
            session.headers = SESSION_HEADERS
            
            for key, value in cookie_json.items():
                session.cookies.set(key, value)
                
            return token, session
                
        except Exception:
            print(f"{Color.FAIL}Invalid cookies, make sure bard.google.com is logged in..{Color.ENDC}")



if __name__ == "__main__":
    

    console = Console()

    queue = Queue()

    def _generate(cookie):
        Cache.init()
        bard = Lardx(cookie)
        queue.put(bard)

    def _recycle():
        bard = Cache.load('bard')
        queue.put(bard)

    if not Cache.exists(): 
        Thread(target=_generate, args=(Profile().cookie_file,)).start()
    else:
        Thread(target=_recycle).start()   
        
    message = input('\U0001F50E: ')

    bard = None
    with console.status(f"{Color.HEADER}Loading..{Color.ENDC}") as status:
        if not Cache.exists():     
            status.update(f"{Color.HEADER}Generating..{Color.ENDC}")
            bard = queue.get()
        else:                  
            status.update(f"{Color.HEADER}Recycling..{Color.ENDC}")
            bard = queue.get()
        
    response = ''
    with console.status(f"{Color.OKCYAN}Querying..{Color.ENDC}"):
        response = '\n\U0001F4EB: ' + bard.ask(message) + '\n'
        
    Stream(response)
    Cache.save(bard)