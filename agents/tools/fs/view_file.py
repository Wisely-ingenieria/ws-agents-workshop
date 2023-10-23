from agents.tools import Tool, Parameter
from llm import count_tokens

MAX_TOKENS = 2000

class ViewFile(Tool):
    def __init__(self):
        super().__init__(
            name="view_file",
            func=self.view_file,
            description="Useful for viewing the content of a text file, considering a max tokens limit.",
            arguments=[
                Parameter("filepath", "The path to the text file you want to view. Must start with './data'", str, required=True),
            ]
        )

    def view_file(self, filepath):
        if filepath is None:
            return "ERROR: Missing argument. Filepath is required."
        
        if not filepath.startswith("./data"):
            return "ERROR: Invalid path. Path must start with './data'"

        allowed_extensions = ['.txt', '.md', '.yaml', '.yml', '.conf', '.ini', '.html', '.css', '.js', '.py', '.java', '.c', '.cpp', '.js', '.ts', '.php', '.rb', '.go', '.rs', '.h', '.hpp', '.cs', '.swift', '.kt', '.scala', '.m', '.pl', '.bash', '.sh', '.r', '.groovy', '.clj', '.sql', '.properties', '.bat', '.ps1', '.vbs', '.lua', '.rst', '.markdown', '.tex', '.asm', '.mat', '.f', '.pas', '.vb', '.dart', '.sass', '.less', '.scss', '.erl', '.hs', '.aspx', '.jsp', '.phtml', '.twig', '.mustache', '.haml', '.jl', '.cshtml', '.vbhtml', '.fs', '.fsx', '.ml', '.tcl', '.zsh', '.csh', '.jsx', '.tsx']

        # Check if file extension is allowed
        if not any(filepath.endswith(extension) for extension in allowed_extensions):
            return f"ERROR: Invalid file extension. Allowed extensions are {allowed_extensions}"

        try:
            with open(filepath, 'r', encoding="utf-8") as infile:
                file_content = infile.read()
        except FileNotFoundError:
            return "ERROR: File not found"
        except IOError as e:
            return f"ERROR: I/O error({e.errno}): {e.strerror}"
        except Exception as e:
            return f"ERROR: {e}"

        # Count tokens in file_content
        tokens_count = count_tokens(file_content)
        
        if tokens_count > MAX_TOKENS:
            return "ERROR: The string containing the file content is too large, try a different file or a different tool."
        
        return file_content