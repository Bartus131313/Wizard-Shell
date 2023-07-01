from colorama import Fore, Style
import subprocess
import webbrowser

def main(command, arg):
    if command == 'print':
        print_cmd(arg)
    if command == 'start':
        start_cmd(arg)

# Commands

def print_cmd(arg):
    RED = arg.lower().find("#f00")
    GREEN = arg.lower().find("#0f0")
    BLUE = arg.lower().find("#00f")
    if RED == 0:
        color_input = arg[arg.lower().find("#f00") + len("#f00"):].strip()
        print(f'{Fore.RED}{color_input}{Style.RESET_ALL}')
    elif GREEN == 0:
        color_input = arg[arg.lower().find("#0f0") + len("#0f0"):].strip()
        print(f'{Fore.GREEN}{color_input}{Style.RESET_ALL}')
    elif BLUE == 0:
        color_input = arg[arg.lower().find("#00f") + len("#00f"):].strip()
        print(f'{Fore.BLUE}{color_input}{Style.RESET_ALL}')
    else:
        print(arg)
    print()

def start_cmd(arg):
    try:
        subprocess.Popen(arg)
        print()
    except:
        print(f'{Fore.RED}>>> Could not open "{arg}"{Style.RESET_ALL}\n')

# Settings

def commands():
    return ['print', 'start']

def commands_display():
    return ['print [Color (#f00 / #0f0 / #00f)] [Message]', 'start [Argument]']