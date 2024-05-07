"""
issues
- boxes.json, your-image.jpg, and fabric.min.js are created in the wrong directory
"""

import os
import re

class FileSystemManager:
    """Handles file and directory operations."""

    @staticmethod
    def create_directory(path):
        """Creates a directory if it doesn't already exist."""
        os.makedirs(path, exist_ok=True)

    @staticmethod
    def create_file(path):
        """Creates an empty file."""
        with open(path, 'w') as f:
            f.close()

class TreeParser:
    """Parses a tree structure string and creates the corresponding file system structure."""

    def __init__(self, tree_str):
        self.tree_str = tree_str
        self.path_stack = []

    def parse_and_create(self):
        """Parses the tree string and creates the directories and files accordingly."""
        lines = self.tree_str.strip().split('\n')

        for line in lines:
            self._process_line(line)

    def _process_line(self, line):
        depth = self._calculate_depth(line)
        self.path_stack = self.path_stack[:depth]

        name = self._extract_name(line)
        if name:
            if name.endswith('/'):
                self._create_directory(name[:-1])
            else:
                self._create_file(name)

    # def _calculate_depth(self, line):
    #     """Calculates the depth of the current line based on its indentation."""
    #     indent_match = re.match(r"(\|\s*|--\s*)*", line)
    #     if indent_match:
    #         indent = indent_match.group()
    #         return indent.count('|') + indent.count('--') // 2
    #     return 0

    def _calculate_depth(self, line):
        """Calculates the depth of the current line based on its indentation, assuming 4 spaces per indentation level."""
        # Calculate leading spaces and divide by 4 (or the number of spaces per level in your specific tree output)
        leading_spaces = len(line) - len(line.lstrip(' '))
        depth = leading_spaces // 4  # Adjust this value if your indentation uses a different number of spaces per level
        return depth


    def _extract_name(self, line):
        """Extracts the name of the file or directory from the line."""
        name_match = re.search(r"[A-Za-z].*", line)
        return name_match.group() if name_match else None

    def _create_directory(self, name):
        """Creates a directory at the current path stack level."""
        dir_path = os.path.join(*self.path_stack, name) if self.path_stack else name
        FileSystemManager.create_directory(dir_path)
        self.path_stack.append(name)

    def _create_file(self, name):
        """Creates a file at the current path stack level."""
        file_path = os.path.join(*self.path_stack, name) if self.path_stack else name
        if os.path.dirname(file_path):
            FileSystemManager.create_directory(os.path.dirname(file_path))
        FileSystemManager.create_file(file_path)

tree_output = """
site/
├── backend/
│   ├── app/
│   │   └── main.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   ├── Dockerfile
│   └── package.json
├── nginx/
│   ├── Dockerfile
│   └── nginx.conf
└── docker-compose.yml
"""

if __name__ == "__main__":
    parser = TreeParser(tree_output)
    parser.parse_and_create()
