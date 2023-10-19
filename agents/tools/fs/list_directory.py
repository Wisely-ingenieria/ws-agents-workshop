import os
from agents.tools import Tool, Parameter
from llm import count_tokens

MAX_TOKENS = 1000

class ListDirectory(Tool):
    def __init__(self):
        super().__init__(
            name="list_directory",
            func=self.list_directory,
            description="List the contents of the specified directory and its subdirectories. Default = './'",
            arguments=[
                Parameter("path", "The path of the directory to list. Must start with './'", str, required=False),
                Parameter("depth", "The depth of subdirectories to list.", int, required=False)        
            ]
        )

    def list_directory(self, path="./", depth=1):
        try:
            if not path.startswith("./"):
                return "Invalid path. Path must start with './'"

            if not os.path.exists(path):
                return "Path does not exist"

            if not os.path.isdir(path):
                return "Path is not a directory"

            def get_tree(path, depth):
                tree = {}
                if depth < 0: return tree
                for name in os.listdir(path):
                    sub_path = os.path.join(path, name)
                    if os.path.isdir(sub_path):
                        tree[name + "/"] = get_tree(sub_path, depth - 1)
                    else:
                        tree[name] = None
                return tree

            tree = get_tree(path, depth)
            tree_string = f"Here is the directory:\n{print_tree(tree)}"

            tokens_count = count_tokens(tree)
            if tokens_count > MAX_TOKENS:
                return "The string containing the list of files and directories is too large, try different depth or another path."

            return tree_string

        except Exception as e:
            return f"ERROR: {str(e)}"
            
def print_tree(tree, indent='', is_last=False):
    tree_string = ''
    keys = list(tree.keys())
    for i, key in enumerate(keys):
        value = tree[key]
        if is_last:
            prefix = '    ' # four spaces
        else:
            prefix = '│   ' # vertical line followed by three spaces
        if i == len(keys) - 1: # if it's the last item
            tree_string += f'{indent}└── {key}\n'
            next_indent = indent + prefix
            tree_string += print_tree(value, next_indent, is_last=True) if isinstance(value, dict) else ''
        else:
            tree_string += f'{indent}├── {key}\n'
            next_indent = indent + prefix
            tree_string += print_tree(value, next_indent, is_last=False) if isinstance(value, dict) else ''
    return tree_string