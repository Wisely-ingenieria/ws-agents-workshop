import os
import re
from agents.tools import Tool, Parameter
from llm import count_tokens

MAX_TOKENS = 1500

class SearchDirectory(Tool):
    def __init__(self):
        super().__init__(
            name="search_directory",
            func=self.search_directory,
            description="Search for files and folders in the specified directory and its subdirectories using a regular expression.",
            arguments=[
                Parameter("regex", "Regular expression to filter the search. Default=None.", str, required=True),
                Parameter("page_size", "The size of each page. Default=25.", int, required=False),
                Parameter("page_number", "The page number to return. Default=1.", int, required=False)
            ]
        )

    def search_directory(self, regex=None, page_size=25, page_number=1):
        # If regex is provided, check if it is valid
        if regex:
            try:
                re.compile(regex)
            except re.error:
                return "ERROR: Invalid regular expression"
            
        # Create a list of all the filepaths inside the ./data directory
        matches = []
        for root, dirnames, filenames in os.walk("./data"):
            for filename in filenames:
                # Append the filepath to the list of matches. Change \ for /
                matches.append(os.path.join(root, filename).replace("\\", "/"))
            
        # If regex is provided, filter the matches
        if regex:
            pattern = re.compile(regex)
            matches = [match for match in matches if pattern.search(match)]
        
        # Use pagination
        start = (page_number - 1) * page_size
        end = start + page_size

        # Return the matches in the requested page
        page_matches = matches[start:end]

        # Error handling for no matches
        if len(page_matches) == 0:
            return f"No matches found for the given regex {regex}."

        return_string = f"Search results (page {page_number} of {len(matches) // page_size + 1}):\n"
        for file in page_matches:
            return_string += f"- {file}\n"

        # Check for token count limit
        token_count = count_tokens(return_string)
        if token_count > MAX_TOKENS:
            return "ERROR: The return string is too long. Please try again with a smaller page size."

        return f"Search results: {len(page_matches)} matches:\n{return_string}"