from agents.tools import Tool, Parameter
from llm import count_tokens, generate_text, gpt35_model, gpt35_16k_model, gpt4_model

MAX_TOKENS = 8000

class QueryFile(Tool):
    def __init__(self):
        super().__init__(
            name="query_file",
            func=self.query_file,
            description="Useful for when you need to ask questions about a file in the ./data directory and extract information from it using a Large Language Model.",
            arguments=[
                Parameter("filepath", "The path to the text based file you want to query. Must start with './data'", str, required=True),
                Parameter("questions", "An array of fully formed queries that you want to execute on the file.", list, item_type=str, required=True)
            ]
        )

    def query_file(self, filepath, questions):
        if filepath is None or questions is None:
            return "ERROR: Missing arguments. Both filepath and questions are required."
        
        if not filepath.startswith("./data"):
            return "ERROR: Invalid path. Path must start with './data'"

        allowed_extensions = ['.txt', '.md', '.yaml', '.yml', '.conf', '.ini', '.html', '.css', '.js', '.py', '.java', '.c', '.cpp', '.js', '.ts', '.php', '.rb', '.go', '.rs', '.h', '.hpp', '.cs', '.swift', '.kt', '.scala', '.m', '.pl', '.bash', '.sh', '.r', '.groovy', '.clj', '.sql', '.properties', '.bat', '.ps1', '.vbs', '.lua', '.rst', '.markdown', '.tex', '.asm', '.mat', '.f', '.pas', '.vb', '.dart', '.sass', '.less', '.scss', '.erl', '.hs', '.aspx', '.jsp', '.phtml', '.twig', '.mustache', '.haml', '.jl', '.cshtml', '.vbhtml', '.fs', '.fsx', '.ml', '.tcl', '.zsh', '.csh', '.jsx', '.tsx']

        # Check if file extension is allowed
        if not any(filepath.endswith(extension) for extension in allowed_extensions):
            return f"ERROR: Invalid file extension. Allowed extensions are {allowed_extensions}"

        query = "\n".join(questions)

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
        
        if tokens_count > 2000:
            model = gpt35_16k_model
        else:
            model = gpt35_model

        system_message = {"role": "system", "content": "Review the [FILE_CONTENT] and answer the [QUERY]. Include as much details as possible in your answer."}
        prompt = f"[QUERY]\n{query}\n[FILE_CONTENT]\n\'\'\'\n{file_content}\n'\'\'\n[ANSWER]"
        answer = generate_text(prompt, model=model, messages=[system_message])
        return answer