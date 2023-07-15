import os, requests
from bardapi.constants import SESSION_HEADERS
from bardapi import Bard

_1PSID = os.getenv('BARD_API_KEY0')
_1PSIDTS = os.getenv('BARD_API_KEY1')
_1PSIDCC = os.getenv('BARD_API_KEY2')

session = requests.Session()
session.headers = SESSION_HEADERS
session.cookies.set("__Secure-1PSID", _1PSID)
session.cookies.set("__Secure-1PSIDTS", _1PSIDTS)
session.cookies.set("__Secure-1PSIDCC", _1PSIDCC)

bard = Bard(token=_1PSID, session=session)

print('\n','*'*50,'Terminal Chat with BARD','*'*50, '\n')
try:
    while True:
        user_input = input('\U0001F464 You: ')
        print('')
        print('\U0001F916 Bard:', bard.get_answer(user_input.strip())['content'])
        print('-'*100, "\n")
except KeyboardInterrupt:
    print('Ended Chat!')
except:
    print('Ended Chat!')