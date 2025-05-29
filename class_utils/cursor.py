from .node import Node

from .enumeration import SortFile

class Cursor:
    
    def __init__(self, node : Node) -> None:
        self.node : Node = node
        self.current = 0
                
        self.hiddens = True
        
        self.fileToCopy = None
        self.modeCopy = False
        
        self.sortMode = SortFile.NAME
         

    def get_node(self) -> Node:
        return self.node
    

    def cursor_down(self, modeNew : bool = False):
        if modeNew:
            self.current += 1
        else:
            if len(self.get_content()) != 0:
                self.current += 1
                if self.current > len(self.get_content()) - 1:
                    self.current = 0
            else:
                self.current = 0


    def cursor_up(self, modeNew : bool = False):
        if modeNew:
            self.current -= 1
        else:
            if len(self.get_content()) != 0:
                self.current -= 1
                if self.current < 0:
                    self.current = len(self.get_content()) - 1
            else:
                self.current = 0
        

    def select(self):
        self.node = self.get_current_selected()
        self.current = 0
    

    def get_content(self, filter : str = '') -> list:
        res = []
        if self.node.is_dir():
            res = self.node.get_children(self.hiddens)
            res.sort(key=lambda x: self.sortNode(x))
            # Filter the content
            return [obj for obj in res if obj.get_name().startswith(filter)]
        else:
            res = self.node.get_content()
            return res
        
        
        
    

    def get_current_index(self) -> int:
        return self.current
    

    def get_parent(self):
        previous = self.node.get_name()
        self.node = self.node.get_parent()
        self.current = next((i for i, obj in enumerate(self.get_content()) if obj.get_name() == previous), 0)



    def get_toggle_hidden(self):
        self.hiddens = not self.hiddens
        self.current = 0


    def get_current_selected(self) -> Node:
        return self.get_content()[self.current]
    
    
    def copySet(self):
        self.fileToCopy = self.get_current_selected()
        self.modeCopy = True
    
    def cutSet(self):
        self.fileToCopy = self.get_current_selected()
        self.modeCopy = False
        
    def paste(self):
        if self.modeCopy:
            self.fileToCopy.copy(self.node)
        else:
            self.fileToCopy.move(self.node)
        
    def delete(self):
        self.get_current_selected().delete()
        
        if self.current > len(self.get_content()) - 1:
            self.current = len(self.get_content()) - 1
            
    def get_permissions(self):
        return self.get_current_selected().get_permissions()
    
    def create_file(self, name):
        if name != "":
            self.node.create_file(name)
    
    def create_dir(self, name):
        if name != "":
            self.node.create_dir(name)
        
    def rename(self, name):
        if name != "":
            self.get_current_selected().rename(name)
        
        
    def sortNode(self, child):
        if self.sortMode == SortFile.NAME:
            return child.get_name().lower()
        elif self.sortMode == SortFile.DATE:
            return child.get_date()
        elif self.sortMode == SortFile.SIZE:
            return child.get_size()
    
    def changeSort(self):
        if self.sortMode == SortFile.NAME:
            self.sortMode = SortFile.DATE
        elif self.sortMode == SortFile.DATE:
            self.sortMode = SortFile.SIZE
        elif self.sortMode == SortFile.SIZE:
            self.sortMode = SortFile.NAME
        self.current = 0