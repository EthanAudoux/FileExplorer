from .display import Display
from .enumeration import *

import os
import json
import pyperclip

class Keys:
    
    def __init__(self, display : Display) -> None:
        self.display = display
        
        self.setting = display.settings
        self.keyboardMapping = display.keyboardMapping
    
    
    def resolve_keys(self, command : str) -> int:
        if self.display.showSettings == ModeOnOff.ON:
            res = self.resolve_keys_settings(command)
        elif self.display.mode == ModeCreationFile.NONE:
            res = self.resolve_keys_normal(command)
        else:
            res = self.resolve_keys_new(command)
        return res
    

    def resolve_keys_normal(self, command : str):

        self.display.display()
        if command == self.keyboardMapping['quit']:
            return 1
        elif command == self.keyboardMapping['down']:
            self.display.cursor.cursor_down()
        elif command == self.keyboardMapping['up']:
            self.display.cursor.cursor_up()
        elif command == self.keyboardMapping['next']:
            self.display.cursor.select()
        elif command == self.keyboardMapping['previous']:
            self.display.cursor.get_parent()
            
            
        elif command == self.keyboardMapping['showHidden']:
            self.display.cursor.get_toggle_hidden()
        elif command == self.keyboardMapping['showPermissions']:
            self.display.showPermission = not self.display.showPermission
        elif command == self.keyboardMapping['showSettings']:
            self.display.showSettings = ModeOnOff.ON
        
        
        elif command == self.keyboardMapping['copy']:
            self.display.cursor.copySet()
        elif command == self.keyboardMapping['cut']:
            self.display.cursor.cutSet()
        elif command == self.keyboardMapping['paste']:
            self.display.cursor.paste()
        elif command == self.keyboardMapping['delete']:
            self.display.cursor.delete()
            
        elif command == self.keyboardMapping['rename']:
            self.display.renameMode = ModeOnOff.ON
        
        
        elif command == self.keyboardMapping['new']:
            self.display.mode = ModeCreationFile.UNKNOWN

            
        
        elif command == self.keyboardMapping['filter']:
            self.display.filterMode = ModeOnOff.ON
        elif command == self.keyboardMapping['changeSort']:
            self.display.cursor.changeSort()
            
        
        elif command == self.keyboardMapping['openInTerminal']:
            new_dr = self.display.cursor.node.path
            pyperclip.copy("cd " + new_dr)
            return 1
        
        
        else:
            print('Unknown command')
        
        return 0
        

    def resolve_keys_new(self, command : str):
        if command == self.keyboardMapping['down']:
            self.display.cursor.cursor_down(True)
        elif command == self.keyboardMapping['up']:
            self.display.cursor.cursor_up(True)
        elif command == self.keyboardMapping['next']:
            self.display.select_new()
        elif command == self.keyboardMapping['previous']:
            self.display.mode = ModeCreationFile.NONE
        return 0


    def resolve_keys_settings(self, command : str):
        if command == self.keyboardMapping['quit']:
            return 1
        elif command == self.keyboardMapping['previous']:
            self.display.showSettings = ModeOnOff.OFF          
        return 0

