import os
import subprocess
from agents.tools import Tool, Parameter

from dotenv import load_dotenv
load_dotenv()

class CloneRepo(Tool):
    def __init__(self):
        super().__init__(
            name="clone_repo",
            func=self.clone_repo,
            description="Clone a repository",
            arguments=[
                Parameter("repo_url", "The URL of the repository to clone.", str, required=True)
            ]
        )

    def clone_repo(self, repo_url):
        # Get the PAT from environment variables
        github_token = os.getenv('GITHUB_PAT')

        # Modify the repo_url to include the PAT
        repo_url_parts = repo_url.split('://')  # separate the protocol from the rest of the URL
        repo_url = f'{repo_url_parts[0]}://{github_token}@{repo_url_parts[1]}'

        # Get the repo name from the URL
        repo_name = repo_url.split('/')[-1]
        if '.git' in repo_name:
            repo_name = repo_name[:-4]  # Remove the .git extension if present

        # Create destination directory with the repo name
        destination = './data/git/' + repo_name + '/'
        if os.path.exists(destination):
            return f"ERROR: Destination directory already exists. {destination}"
        os.makedirs(destination, exist_ok=True)

        console_output = None  # Initialize console_output
        try:
            # Clone the repository
            result = subprocess.run(['git', 'clone', repo_url, destination], check=True, capture_output=True, text=True)
            console_output = result.stdout
        except subprocess.CalledProcessError as e:
            return f"ERROR: Unable to clone repository. Error message: {e}. Console output: {console_output}"
        
        except OSError as e:
            return f"ERROR: Unable to create destination directory. Error message: {e}"

        return f"Repository cloned successfully to {destination}"