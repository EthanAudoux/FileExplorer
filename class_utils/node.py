import time
import os
from .enumeration import SortFile


class Node:
    
    def __init__(self, path : str):
        self.path = path
    
    
    def get_path(self):
        return self.path
    
    def get_name(self):
        return os.path.basename(self.path)
    
    def is_dir(self):
        return os.path.isdir(self.path)
    
    def get_brother(self):
        try:
            parent = self.get_parent()
            return parent.get_children(True)
        except:
            return ["Impossible to read the folder"]
    
    def get_children(self, hidden : bool, sort : SortFile = SortFile.NAME):
        try:
            if hidden:
                if os.path.isdir(self.path):
                    return [Node(os.path.join(self.path, child)) for child in os.listdir(self.path) if not child.startswith('.')]
                else:
                    return None
            else:
                if os.path.isdir(self.path):
                    return [Node(os.path.join(self.path, child)) for child in os.listdir(self.path)]
                else:
                    return None
        except:
            return self.get_brother()
        
    def get_permissions(self):
        return oct(os.stat(self.path).st_mode)[-3:]
    

    def get_content(self):
        try:            
            with open(self.path, 'r') as f:
                return f.readlines()
        except:
            return ["Impossible to read the file"]
    
    def get_parent(self):
        return Node(os.path.dirname(self.path))


    def copy(self, node):
        os.system(f'cp -r {self.get_path()} {node.get_path()}')

    def move(self, node):
        os.system(f'mv {self.get_path()} {node.get_path()}')
        
    def delete(self):
        #os.system(f'rm -r {self.get_path()}')

            os.system(f'gio trash {self.get_path()}')
        
    def create_file(self, name):
        os.system(f'touch {os.path.join(self.get_path(), name)}')
        
    def create_dir(self, name):
        os.system(f'mkdir {os.path.join(self.get_path(), name)}')
        
    def rename(self, name):
        os.system(f'mv {self.get_path()} {os.path.join(self.get_parent().get_path(), name)}')
    
    
    def get_size(self):
        return os.path.getsize(self.path)
    
    def get_date(self):
        return os.path.getmtime(self.path)
