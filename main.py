from class_utils.display import Display
from class_utils.cursor import Cursor
from class_utils.node import Node
from class_utils.keys import Keys
import class_utils.globals as globals

from class_utils.enumeration import ModeCreationFile
from class_utils.enumeration import ModeOnOff

import tty
import termios
import sys
import os
import json



def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)  # Read a single character
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def resolve_keys(display : Display, command : str):
    # open settings.json in a dictionnary
    settings = json.load(open(os.path.join(os.path.dirname(__file__), 'settings.json')))
    keyboardMapping = settings['keybord']

    display.display()
    if command == keyboardMapping['quit']:
        return 1
    elif command == keyboardMapping['down']:
        display.cursor.cursor_down()
    elif command == keyboardMapping['up']:
        display.cursor.cursor_up()
    elif command == keyboardMapping['next']:
        display.cursor.select()
    elif command == keyboardMapping['previous']:
        display.cursor.get_parent()
        
        
    elif command == keyboardMapping['showHidden']:
        display.cursor.get_toggle_hidden()
    elif command == keyboardMapping['showPermissions']:
        display.showPermission = not display.showPermission
        display.display()
    elif command == keyboardMapping['showSettings']:
        display.showSettings = ModeOnOff.ON
        display.display()
    
    
    elif command == keyboardMapping['copy']:
        display.cursor.copySet()
    elif command == keyboardMapping['cut']:
        display.cursor.cutSet()
    elif command == keyboardMapping['paste']:
        display.cursor.paste()
    elif command == keyboardMapping['delete']:
        display.cursor.delete()
        
    elif command == keyboardMapping['rename']:
        display.renameMode = ModeOnOff.ON
        display.display()
    
    
    elif command == keyboardMapping['new']:
        display.mode = ModeCreationFile.UNKNOWN
        display.display()

        
    
    elif command == keyboardMapping['filter']:
        display.filterMode = ModeOnOff.ON
        display.display()
    elif command == keyboardMapping['changeSort']:
        display.cursor.changeSort()
        display.display()    
    
        
    
    else:
        print('Unknown command')
    
    return 0
    

def resolve_keys_new(display : Display, command : str):
    # open settings.json in a dictionnary
    settings = json.load(open(os.path.join(os.path.dirname(__file__), 'settings.json')))
    keyboardMapping = settings['keybord']

    if command == keyboardMapping['down']:
        display.cursor.cursor_down()
    elif command == keyboardMapping['up']:
        display.cursor.cursor_up()
    elif command == keyboardMapping['next']:
        display.select_new()
        display.display()
    elif command == keyboardMapping['previous']:
        display.mode = ModeCreationFile.NONE
        display.display()
    
    return 0


def resolve_keys_settings(display : Display, command : str):
    # open settings.json in a dictionnary
    settings = json.load(open(os.path.join(os.path.dirname(__file__), 'settings.json')))
    keyboardMapping = settings['keybord']

    if command == keyboardMapping['quit']:
        return 1
    elif command == keyboardMapping['previous']:
        display.showSettings = ModeOnOff.OFF
        display.display()
    
    return 0

def main(firstPath : str):
        
    settings = json.load(open(os.path.join(os.path.dirname(__file__), 'settings.json')))
    

    # Test on home folder
    display = Display(Cursor(Node(firstPath)), settings)
    
    keys = Keys(display)
    
    try:
        res = 0
        display.display()
        while res == 0:
            display.display()
            command = getch()
            
            res = keys.resolve_keys(command)
    
    except KeyboardInterrupt:
        print('Goodbye!')
        sys.exit(0)

    clear = lambda: os.system("clear")
    clear()
    
    """
    os.chdir(display.cursor.node.get_path())
    os.system("bash")
    """
            
        


def print_help():
    settings = json.load(open(os.path.join(os.path.dirname(__file__), 'settings.json')))

    print("Usage: python main.py [path]")
    print("Display a folder in a terminal interface.")
    print("If no path is provided, the home folder is used.")
    print(f"Press '{settings['keybord']["quit"]}' to quit, '{settings['keybord']["showSettings"]}' for help.")


import argparse
# Parse arguments
# First argument is the path of the folder, if not provided, use the home folder

parser = argparse.ArgumentParser(description='Display a folder')
parser.add_argument('path', type=str, nargs='?', default=os.path.expanduser("~"), help='Path of the folder to display')
parser.add_argument('-i', "--info", action='store_true', help='Display information about the program')
args = parser.parse_args()




if __name__ == '__main__':
    if args.info:
        print_help()
    else:
        main(args.path)
    
