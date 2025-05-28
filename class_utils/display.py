from .cursor import Cursor
from .color import Color
from .enumeration import *
from .globals import log

import os
import json


class Display:
    def __init__(self, cursor : Cursor, settings : dict) -> None:
        self.cursor : Cursor = cursor
        self.clear = lambda: os.system("clear")
        
        self.settings = settings
        self.keyboardMapping = settings['keybord']
                
        self.start_file : int
        self.end_file : int
        
        self.mode : ModeCreationFile = ModeCreationFile.NONE
        
        self.filterMode : ModeOnOff = ModeOnOff.OFF
        self.filter : str = ''
        self.nodeFilter = None
        
        self.showPermission : bool = False
        
        self.renameMode : ModeOnOff = ModeOnOff.OFF
        
        self.showSettings : ModeOnOff = ModeOnOff.OFF
        
        
    def display(self):
        self.clear()
        if self.nodeFilter != self.cursor.node:
            self.filter = ''
            
        if self.mode != ModeCreationFile.NONE:
            self.display_new()
        elif self.showSettings == ModeOnOff.ON:
            self.show_settings()
        else:
            self.set_start_end()
            if self.cursor.node.is_dir():
                self.display_folder()
            else:
                self.display_file()
            

            if self.renameMode == ModeOnOff.ON:
                command = input('Enter a name: ')
                self.cursor.rename(command)
            self.renameMode = ModeOnOff.OFF

            if self.filterMode == ModeOnOff.ON:
                self.nodeFilter = self.cursor.node
                command = input('Enter a filter: ')
                self.filter = command
            self.filterMode = ModeOnOff.OFF
        
            
    

    def display_folder(self):
        
        print(Color().color_text(self.cursor.node.get_name(), Color.BOLD), self.start_file, self.end_file, self.cursor.get_current_index(), os.get_terminal_size().lines, self.cursor.sortMode.value)
        for i, child in enumerate(self.cursor.get_content(self.filter)):
            if i >= self.start_file and i < self.end_file:
                if child.is_dir():
                    name = Color().color_text(child.get_name(), Color.BOLD)
                else:
                    name = child.get_name()
                
                if self.showPermission:
                    name = f'{self.transformPermission(child.get_permissions())} {name}'
                
                if i == self.cursor.get_current_index():
                    print(f'-> {name}')
                else:
                    print(f'   {name}')
                
    def display_file(self):

        
        contentOfFile = self.cursor.get_content(self.filter)
        
        # Display the name of the file
        print(Color().color_text(self.cursor.node.get_name(), Color.BOLD), self.start_file, self.end_file, self.cursor.get_current_index(), os.get_terminal_size().lines)
        
        # Delete all \n at the end of each line
        contentOfFile = [line.rstrip() for line in contentOfFile]
        
        # Display the content of the file
        for i in range(self.start_file, self.end_file):
            if i == self.cursor.get_current_index():
                print(f'· {contentOfFile[i]}')
            else:
                print(f'  {contentOfFile[i]}')
        
        print(f'Press q to go back to the folder')   
        
    def display_new(self):
        self.clear()
        selection = ['File', 'Folder']
        for i, sel in enumerate(selection):
            if i == self.cursor.get_current_index()%2:
                print(f'-> {sel}')
            else:
                print(f'   {sel}')
        
        if self.mode == ModeCreationFile.FILE:
            command = input('Enter a name: ')
            self.cursor.create_file(command)
            self.mode = ModeCreationFile.NONE
            
        elif self.mode == ModeCreationFile.DIR:
            command = input('Enter a name: ')
            self.cursor.create_dir(command)
            self.mode = ModeCreationFile.NONE



    def show_settings(self):
        self.clear()
        settings = json.load(open(os.path.join(os.path.dirname(__file__), '../settings.json')))
        keyboardMapping = settings['keybord']
        
        for i, command in enumerate(keyboardMapping):
            print(f'{command} : {keyboardMapping[command]}')
        print(f'Press {keyboardMapping["previous"]} to go back to the menu')

     
    def select_new(self):
        if self.cursor.get_current_index()%2 == 0:
            self.mode = ModeCreationFile.FILE
        else:
            self.mode = ModeCreationFile.DIR
        self.display()          
    
    
        
        
    def set_start_end(self):
        rows = os.get_terminal_size().lines
        
        max_rows = rows - 5
        
        if len(self.cursor.get_content(self.filter)) - max_rows < 0:
            self.start_file = 0
        elif self.cursor.get_current_index() > len(self.cursor.get_content(self.filter)) - max_rows:
           self.start_file = len(self.cursor.get_content(self.filter)) - max_rows
        
        else:
            self.start_file = self.cursor.get_current_index() - 2
            
        self.end_file = self.start_file + max_rows
        if self.end_file > len(self.cursor.get_content(self.filter)):
            self.end_file = len(self.cursor.get_content(self.filter))            


    def transformPermission(self, permission : str) -> str:
        res = ''
        fullSquare = '■'
        for i, p in enumerate(permission):
            pBinaire = bin(int(p))[2:]    
            for j in range(3 - len(pBinaire)):
                pBinaire = '0' + pBinaire
            # put a green full square if the permission is granted 
            # put a red full square if the permission is not granted
            for k in range(3):
                if pBinaire[k] == '1':
                    res += Color().color_text(fullSquare, Color.GREEN)
                else:
                    res += Color().color_text(fullSquare, Color.RED)
            if i != 2:
                res += ' '

        
        return res