import os
from .enumeration import SortFile


class Node:
    """
    Class representing a file or directory in the filesystem.
    Provides methods to interact with the filesystem, such as getting children,
    copying, moving, deleting, and retrieving metadata.
    """
    
    def __init__(self, path : str):
        """
        Initialize the Node with a given path.
        @param path: The path to the file or directory.
        """
        self.path = os.path.abspath(path)
    
    def get_path(self):
        """
        Get the absolute path of the node.
        @return: The absolute path as a string.
        """
        return os.path.abspath(self.path)
    
    def get_name(self):
        """
        Get the name of the node (file or directory).
        @return: The name of the node as a string.
        """
        if self.path == '/':
            return 'Root'
        else:
            return os.path.basename(self.path)
    
    def is_dir(self):
        """
        Check if the node is a directory.
        @return: True if the node is a directory, False otherwise.
        """
        return os.path.isdir(self.path)
    
    def get_brother(self):
        """
        Get the siblings of the node (children of the parent directory).
        @return: A list of Node objects representing the siblings, or an error message if the operation fails.
        """
        try:
            parent = self.get_parent()
            return parent.get_children(True)
        except:
            return ["Impossible to read the folder"]
    
    def get_children(self, hidden : bool, sort : SortFile = SortFile.NAME):
        """
        Get the children of the node (files and directories within it).
        @param hidden: If True, include hidden files (those starting with a dot).
        @param sort: The sorting method to apply to the children (default is by name).
        @return: A list of Node objects representing the children, or None if the node is not a directory.
        """
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
        """
        Get the permissions of the node in octal format.
        @return: A string representing the permissions in octal format (e.g., '755').
        """
        return oct(os.stat(self.path).st_mode)[-3:]
    

    def get_content(self):
        """
        Get the content of the node if it is a file.
        @return: A list of lines in the file, or an error message if the operation fails.
        """
        try:            
            with open(self.path, 'r') as f:
                return f.readlines()
        except:
            return ["Impossible to read the file"]
    
    def get_parent(self):
        """
        Get the parent directory of the node.
        @return: A Node object representing the parent directory.
        """
        if self.path == '/':
            return Node('/')
        return Node(os.path.dirname(self.path))


    def copy(self, node):
        """
        Copy the node to another node's path.
        @param node: The destination Node object where the current node will be copied.
        """
        os.system(f'cp -r {self.get_path()} {node.get_path()}')

    def move(self, node):
        """
        Move the node to another node's path.
        @param node: The destination Node object where the current node will be moved.
        """
        os.system(f'mv {self.get_path()} {node.get_path()}')
        
    def delete(self):
        """
        Delete the node by moving it to the trash.
        Note: This uses the 'gio trash' command to move the node to the trash instead of permanently deleting it.
        """
        # Uncomment the next line to permanently delete the node
        #os.system(f'rm -r {self.get_path()}')
        os.system(f'gio trash {self.get_path()}')
        
    def create_file(self, name):
        """
        Create a new file with the specified name in the node's directory.
        @param name: The name of the file to be created.
        """
        os.system(f'touch {os.path.join(self.get_path(), name)}')
        
    def create_dir(self, name):
        """
        Create a new directory with the specified name in the node's directory.
        @param name: The name of the directory to be created.
        """
        os.system(f'mkdir {os.path.join(self.get_path(), name)}')
        
    def rename(self, name):
        """
        Rename the node to the specified name.
        @param name: The new name for the node.
        """
        os.system(f'mv {self.get_path()} {os.path.join(self.get_parent().get_path(), name)}')
    
    
    def get_size(self):
        """
        Get the size of the node (file or directory).
        @return: The size of the node in bytes, or 0 if the node does not exist.
        """
        return os.path.getsize(self.path)
    
    def get_date(self):
        """
        Get the last modification time of the node.
        @return: The last modification time as a timestamp (seconds since epoch).
        """
        return os.path.getmtime(self.path)
