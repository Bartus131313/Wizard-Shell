import os
import ctypes
from colorama import Fore, Style
import importlib
import sys
import configparser
import requests
import time
import subprocess

# SETTINGS

VERSION_URL = 'https://pastebin.com/raw/Buzs6RGN'

PROGRAM_RUN = True

VERSION = 'BETA 0.1.2.0'
LATEST_VERSION = ''

DEF_COMMANDS = [
    'ws',
    'addons',
    'cls',
    'exit'
    ]

PROGRAM_PATH = os.path.dirname(__file__)
RESOURCES = os.path.join(PROGRAM_PATH, 'resources')
SCRIPTS = os.path.join(PROGRAM_PATH, 'scripts')
ADDONS = os.path.join(PROGRAM_PATH, 'addons')
CONFIGS = os.path.join(PROGRAM_PATH, 'configs')

ICON = os.path.join(RESOURCES, 'icon.png')
TITLE = 'WS | Wizard Shell'

sys.path.append(SCRIPTS)
sys.path.append(ADDONS)
os.chdir(SCRIPTS)

response = requests.get(VERSION_URL)

if response.status_code == 200:
    content = response.text

    LATEST_VERSION = content
else:
    print(f'{Fore.RED}>>> Failed to retrieve content{Style.RESET_ALL}')
    print()
    os.system('pause >nul')

# CONFIG

config = configparser.ConfigParser()

config.read(os.path.join(CONFIGS, 'config.ini'))

DEBUG_MODE = config.get('Settings', 'debug_mode')

if DEBUG_MODE == 'True':
    TITLE = 'WS | Wizard Shell [DEBUG MODE]'

addons = [os.path.splitext(file_name)[0] for file_name in os.listdir(ADDONS) if file_name.endswith('.py')]

addons_true = True

add_commands_dis = []
add_commands_path = []
add_commands = []

# LOAD ADDONS

try:
    for addon in addons:
        imported_addon = importlib.import_module(addon)
        for custom_cmd in imported_addon.commands():
            for key, value in custom_cmd.items():
                if not key in DEF_COMMANDS:
                    if not value.startswith('['):
                        value = f'[{value}'
                    if not value.endswith(']'):
                        value = f'{value}]'
                    add_commands_dis.append({key : value})
                    add_commands.append(key)
                    add_commands_path.append(addon)
except:
    addons_true = False

# ELSE

def change_cmd_title(title):
    ctypes.windll.kernel32.SetConsoleTitleW(title)

def start_msg():
    print()
    print(f'{Fore.BLUE}   > WS | Wizard Shell{Style.RESET_ALL}')
    print(f'{Fore.RED}   > by Bartek Kansy{Style.RESET_ALL}\n')
    print(f'{Fore.BLUE}   > VER.: {Style.RESET_ALL}{Fore.GREEN}{VERSION}{Style.RESET_ALL}\n')
    print(f'{Fore.YELLOW}   > ws [--info | --help]{Style.RESET_ALL}\n')
    print('------------------------------------->\n')

# COMMANDS

def ws_usage():
    print(f'{Fore.GREEN}>>> Usage: WS [Argument]\n')
    print(f'{Fore.YELLOW}>> Arguments:\n')
    print(f'>> --info')
    print(f'>> --help')
    print(f'>> --debug')
    print(f'{Style.RESET_ALL}')

def ws_info():
    print(f'{Fore.YELLOW}>>> {Fore.BLUE}Wizard Shell{Fore.YELLOW} is a console designed to run scripts written in {Fore.GREEN}Python{Fore.YELLOW} in the simplest possible way.{Style.RESET_ALL}\n')

def ws_help():
    print(f'{Fore.YELLOW}>>> All commands in Wizard Shell:{Fore.GREEN}')
    print(f'>> ws [--info | --help | --debug]')
    print(f'>> addons [--info | --help]')
    print(f'')
    print(f'>> cls')
    print(f'>> exit')
    print(f'{Style.RESET_ALL}')

def ws_debug():
    global DEBUG_MODE

    if DEBUG_MODE == 'False':
        DEBUG_MODE = 'True'
    elif DEBUG_MODE == 'True':
        DEBUG_MODE = 'False'

    print(f'{Fore.YELLOW}>>> Changed debug mode to: {DEBUG_MODE}')

    config.set('Settings', 'debug_mode', str(DEBUG_MODE))

    with open(os.path.join(CONFIGS, 'config.ini'), 'w') as config_file:
        config.write(config_file)

    time.sleep(3)
    os.system('cls')    
    subprocess.Popen(['start', sys.executable] + sys.argv, shell=True)
    sys.exit()

def addons_help():
    if addons_true:
        l = 0
        print(f"{Fore.GREEN}>>> Addons commands:")
        for add_cmd in add_commands_dis:
            for cmd, value in add_cmd.items():
                print(f'{Fore.YELLOW}>> {cmd} {value} -|- {add_commands_path[l]}{Style.RESET_ALL}')
                l += 1
    else:
        print(f'{Fore.YELLOW}>> There are no addons loaded{Style.RESET_ALL}')

def addons_info():
    print(f'{Fore.YELLOW}>>> Addons are scripts that add commands to the {Fore.BLUE}Wizard Shell{Fore.YELLOW}.{Style.RESET_ALL}')

def addons_usage():
    print(f'{Fore.GREEN}>>> Usage: addons [Argument]\n')
    print(f'{Fore.YELLOW}>> Arguments:\n')
    print(f'>> --info')
    print(f'>> --help')
    print(f'{Style.RESET_ALL}')

# PROGRAM

if __name__ == '__main__':
    change_cmd_title(TITLE)

    start_msg()

    while PROGRAM_RUN:
        if VERSION != LATEST_VERSION:
            print(f'{Fore.RED}>>> Download the latest version of {Fore.BLUE}Wizard Shell{Style.RESET_ALL}')
            print(f'{Fore.YELLOW}>> Current version: {VERSION}')
            print(f'{Fore.GREEN}>> Latest version: {LATEST_VERSION}{Style.RESET_ALL}')
            print()
            print(f'{Fore.LIGHTBLACK_EX}When updating, only replace the "main.py" file with a new one')
            os.system('pause >nul')
            sys.exit()

        user_input = input('> ')
        low_input = user_input.lower()

        ws_index = low_input.find("ws")
        addons_index = low_input.find("addons")

        custom_cmd = False

        words = user_input.split()

        for cmd, path in add_commands, add_commands_path:
            if words[0].lower() == cmd:
                arg_input = user_input[low_input.find(words[0]) + len(words[0]):].strip()
                imported_addon_cmd = importlib.import_module(path)
                imported_addon_cmd.main(cmd, arg_input)
                custom_cmd = True

        if addons_index != -1:
            addons_input = user_input[addons_index + len("addons"):].strip()
            if addons_input == '--help':
                addons_help()
            if addons_input == '--info':
                addons_info()
            if addons_input == '':
                addons_usage()
            print()
            custom_cmd = True

        if ws_index != -1:
            ws_input = user_input[ws_index + len("ws"):].strip()
            ws_words = ws_input.lower().split()
            ws_words_normal = ws_input.split()

            script_true = False
            command_true = False

            if ws_input == '--info':
                ws_info()
            elif ws_input == '--help':
                ws_help()
            elif ws_input == '--debug':
                ws_debug()
            elif len(ws_words) == 0:
                ws_usage()
            else:
                file_list = os.listdir()
                file_names_without_extension = [os.path.splitext(file_name)[0] for file_name in file_list]
                if file_names_without_extension == []:
                    print(f'{Fore.RED}>>> No modules found!{Style.RESET_ALL}\n')
                else:
                    for file_name in file_names_without_extension:
                        file_name_low = file_name.lower()
                        if ws_words[0] == file_name_low:
                            script_true = True
                            imported_script = importlib.import_module(file_name)
                            commands = imported_script.commands()
                            if len(ws_words) == 1:
                                print(f'{Fore.GREEN}>>> Available commands for "{file_name}"')
                                print(f'{Fore.YELLOW}>> {commands}{Style.RESET_ALL}\n')
                            else:
                                for command in commands:
                                    if ws_words[1] == f'--{command.lower()}':
                                        command_true = False
                                        change_cmd_title(f'WS | Wizard Shell - {file_name}')
                                        imported_script = importlib.import_module(file_name)
                                        imported_script.main(command)
                                        PROGRAM_RUN = False
                                if not command_true:
                                    print(f'{Fore.RED}>>> Command "{ws_words[1]}" was not found!{Style.RESET_ALL}\n')
                    if not script_true:
                        print(f'{Fore.RED}>>> Module "{ws_words_normal[0]}" was not found!{Style.RESET_ALL}\n')
        else:
            if low_input == 'exit':
                break
            if low_input == 'cls':
                os.system('cls')
                start_msg()
            else:
                if not custom_cmd:
                    print(f'{Fore.RED}>>> "{user_input}" is not recognized as an executable command by the program{Style.RESET_ALL}', '\n')
                else:
                    custom_cmd = False