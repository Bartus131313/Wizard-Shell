import os
import sys
from colorama import Fore, Style
import importlib

SCRIPT_DIR = os.path.dirname(__file__)
WIZARD_SHELL_DIR = os.path.dirname(SCRIPT_DIR)

sys.path.append(WIZARD_SHELL_DIR)

ws = importlib.import_module('main')

def main(command):
    if command == 'start':
        start()
    if command == 'info':
        info()

def start_msg():
    os.system('cls')
    print('> EXAMPLE SCRIPT < \n')

def start():
    start_msg()

    while True:
        user_input = input('> ')

        if user_input == 'exit':
            sys.exit()
        if user_input == 'cls':
            start_msg()
        else:
            print(user_input)

def info():
    os.system('cls')
    print(f'')
    print(f'{Fore.GREEN}   > EXAMPLE SCRIPT for {Fore.BLUE}Wizard Shell')
    print(f'{Fore.YELLOW}   > VERSION 0.0.1.0 \n')
    print(f'{Fore.LIGHTBLACK_EX}   > Click any button to return')
    print(f'{Style.RESET_ALL}')
    os.system('pause >NUL')
    ws.ws_return() # Return to Wizard Shell

# SETTINGS

def commands():
    return ['start', 'info']