#!/usr/bin/env python3

import sys
from bard import *
from rich.console import Console

console = Console()    

with console.status("[bold light_slate_blue]Loading...") as status:
    
    bard = None

    try:
        # TODO: make a recovery when cache is corrupted, instead of creating a new bard
        if create_cache_directory() or not check_cache_files():
            bard = create_bard()   
                
        else:
            bard = load_bard()
            load_cache(bard)

        # message = bard.get_answer("what's the darkest place in the universe")['content']

        save_cache(bard)
    
    except ConnectionError as e:
        print(f"{Color.FAIL}failed..  session timeout{Color.ENDC}")

print_stream("")