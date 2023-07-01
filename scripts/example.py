import os
import sys

def main(command):
    if command == 'start':
        start()
    if command == 'info':
        info()

def start_msg():
    os.system('cls')
    print('> Example < \n')

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
    print('INFO \n')
    os.system('pause >NUL')

# SETTINGS

def commands():
    return ['start', 'info']