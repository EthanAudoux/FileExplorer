import json
import os

class Settings:
    
    def __init__(self, pathSettings):
        self.pathSettings = pathSettings
        self.settings = json.load(open(self.pathSettings))
        
        self.keyboardMapping = self.settings['keyboard']
        
        self.cursor = 0
        
    
    def display_settings(self):
        print("Current Settings:")
        i = 0
        for key, value in self.keyboardMapping.items():
            if i == self.cursor:
                print(f"> {key}: {value}")
            else:
                print(f"  {key}: {value}")
            
            i += 1
        print(f"\nUse '{self.keyboardMapping["up"]}' and '{self.keyboardMapping["down"]}' to navigate, '{self.keyboardMapping["next"]}' to select, '{self.keyboardMapping["previous"]}' to exit.")
        
    def navigate_up(self):
        if self.cursor > 0:
            self.cursor -= 1
        else:
            self.cursor = len(self.keyboardMapping) - 1
    
    def navigate_down(self):
        if self.cursor < len(self.keyboardMapping) - 1:
            self.cursor += 1
        else:
            self.cursor = 0
            
    def select(self):
        selected_key = list(self.settings.keys())[self.cursor]
        print(f"Selected: {selected_key} with value {self.settings[selected_key]}")
        # Here you can add logic to change the setting if needed
        # For now, it just prints the selected setting
    
    def previous(self):
        print("Exiting settings.")
        # Logic to exit settings can be added here
        # For now, it just prints a message
        return 1


def main_settings():
    pathSettings = os.path.join(os.path.dirname(os.path.dirname(__file__)), "settings.json")
    print(f"Loading settings from: {pathSettings}")
    settings = Settings(pathSettings)
    
    while True:
        settings.display_settings()
        command = input("Enter command: ").strip().lower()
        
        if command == settings.keyboardMapping["up"]:
            settings.navigate_up()
        elif command == settings.keyboardMapping["down"]:
            settings.navigate_down()
        elif command == settings.keyboardMapping["next"]:
            settings.select()
        elif command == settings.keyboardMapping["previous"]:
            if settings.previous() == 1:
                break
        else:
            print("Invalid command. Please try again.")