from .node import Node

from .enumeration import SortFile

class Cursor:
    """
    Class to manage the cursor in the file system.
    It allows navigation through directories, selection of files,
    copying, cutting, pasting, deleting files, and managing file permissions.
    It also provides methods to create files and directories, rename files,
    and sort files based on different criteria.
    Attributes:
        node (Node): The current node the cursor is pointing to.
        current (int): The index of the currently selected item in the node's content.
        hiddens (bool): Flag to indicate whether hidden files should be shown.
        fileToCopy (Node): The file or directory to be copied or cut.
        modeCopy (bool): Flag to indicate whether the operation is a copy (True) or cut (False).
        sortMode (SortFile): The current sorting mode for files (by name, date, or size).
    """
    
    def __init__(self, node : Node) -> None:
        """
        Initialize the Cursor with a given node.
        Parameters:
            node (Node): The Node object representing the current directory or file.
        """
        
        self.node : Node = node
        self.current = 0
                
        self.hiddens = True
        
        self.fileToCopy = None
        self.modeCopy = False
        
        self.sortMode = SortFile.NAME
         

    def get_node(self) -> Node:
        """
        Get the current node the cursor is pointing to.
        Returns:
            Node: The Node object representing the current directory or file.
        """
        return self.node
    

    def cursor_down(self, modeNew : bool = False):
        """
        Move the cursor down to the next item in the current node's content.
        If modeNew is True, it will always move down regardless of the current index.
        Parameters:
            modeNew (bool): If True, move down without checking the current index.
        """
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
        """
        Move the cursor up to the previous item in the current node's content.
        If modeNew is True, it will always move up regardless of the current index.
        Parameters:
            modeNew (bool): If True, move up without checking the current index.
        """
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
        """
        Select the current item in the node's content.
        """
        self.node = self.get_current_selected()
        self.current = 0
    

    def get_content(self, filter : str = '') -> list:
        """
        Get the content of the current node.
        If the node is a directory, it returns its children sorted by the current sort mode.
        If the node is a file, it returns the content of the file.
        Parameters:
            filter (str): A string to filter the content by name.
        Returns:
            list: A list of objects representing the content of the node. Strings for files, Node objects for directories.
        """
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
        """
        Get the index of the currently selected item in the node's content.
        Returns:
            int: The index of the currently selected item.
        """
        return self.current
    

    def get_parent(self):
        """
        Move the cursor to the parent directory of the current node.
        If the current node is the root directory, it does nothing.
        """
        previous = self.node.get_name()
        self.node = self.node.get_parent()
        self.current = next((i for i, obj in enumerate(self.get_content()) if obj.get_name() == previous), 0)



    def get_toggle_hidden(self):
        """
        Toggle the visibility of hidden files in the current node's content.
        If hidden files are currently shown, it hides them, and vice versa.
        """
        self.hiddens = not self.hiddens
        self.current = 0


    def get_current_selected(self) -> Node:
        """
        Get the currently selected item in the node's content.
        Returns:
            Node: The currently selected Node object.
        """
        return self.get_content()[self.current]
    
    
    def copySet(self):
        """
        Set the file or directory to be copied.
        It stores the currently selected item in the fileToCopy attribute
        and sets the modeCopy flag to True.
        """
        self.fileToCopy = self.get_current_selected()
        self.modeCopy = True
    
    def cutSet(self):
        """
        Set the file or directory to be cut.
        It stores the currently selected item in the fileToCopy attribute
        and sets the modeCopy flag to False.
        """
        self.fileToCopy = self.get_current_selected()
        self.modeCopy = False
        
    def paste(self):
        """
        Paste the copied or cut file or directory to the current node.
        If modeCopy is True, it copies the file; otherwise, it moves the file.
        It uses the copy or move method of the Node class.
        """
        if self.modeCopy:
            self.fileToCopy.copy(self.node)
        else:
            self.fileToCopy.move(self.node)
        
    def delete(self):
        """
        Delete the currently selected file or directory.
        It calls the delete method of the Node class for the currently selected item.
        If the current index is out of bounds after deletion, it adjusts the current index.
        """
        self.get_current_selected().delete()
        
        if self.current > len(self.get_content()) - 1:
            self.current = len(self.get_content()) - 1
            
    def get_permissions(self)-> str:
        """
        Get the permissions of the currently selected file or directory.
        It calls the get_permissions method of the Node class for the currently selected item.
        Returns:
            str: A string representing the permissions of the currently selected item.
        """
        return self.get_current_selected().get_permissions()
    
    def create_file(self, name):
        """
        Create a new file with the specified name in the current node.
        If the name is not an empty string, it calls the create_file method of the Node class.
        Parameters:
            name (str): The name of the file to be created.
        """
        if name != "":
            self.node.create_file(name)
    
    def create_dir(self, name):
        """
        Create a new directory with the specified name in the current node.
        If the name is not an empty string, it calls the create_dir method of the Node class.
        Parameters:
            name (str): The name of the directory to be created.
        """
        if name != "":
            self.node.create_dir(name)
        
    def rename(self, name):
        """
        Rename the currently selected file or directory to the specified name.
        If the name is not an empty string, it calls the rename method of the Node class.
        Parameters:
            name (str): The new name for the file or directory.
        """
        if name != "":
            self.get_current_selected().rename(name)
        
        
    def sortNode(self, child):
        """
        Sort the child node based on the current sort mode.
        It returns a value based on the sort mode:
        - If sort mode is NAME, it returns the name of the child in lowercase.
        - If sort mode is DATE, it returns the date of the child.
        - If sort mode is SIZE, it returns the size of the child.
        Parameters:
            child (Node): The child node to be sorted.
        Returns:
            sstr or int: A value used for sorting the child node.
        """
        if self.sortMode == SortFile.NAME:
            return child.get_name().lower()
        elif self.sortMode == SortFile.DATE:
            return child.get_date()
        elif self.sortMode == SortFile.SIZE:
            return child.get_size()
    
    def changeSort(self):
        """
        Change the current sort mode of the cursor.
        It cycles through the sort modes: NAME -> DATE -> SIZE -> NAME.
        """
        if self.sortMode == SortFile.NAME:
            self.sortMode = SortFile.DATE
        elif self.sortMode == SortFile.DATE:
            self.sortMode = SortFile.SIZE
        elif self.sortMode == SortFile.SIZE:
            self.sortMode = SortFile.NAME
        self.current = 0