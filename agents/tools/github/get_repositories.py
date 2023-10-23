import os
import requests
from agents.tools import Tool, Parameter

from dotenv import load_dotenv
load_dotenv()

class GetRepositories(Tool):
    def __init__(self):
        super().__init__(
            name="get_repositories",
            func=self.get_user_repos,
            description="Get user's Github repositories",
            arguments=[
                Parameter("page_size", "The size of each page. Default=10.", int, required=False),
                Parameter("page_number", "The page number to return. Default=1.", int, required=False)
            ]
        )

    def get_user_repos(self, page_size=10, page_number=1):
        github_token = os.getenv('GITHUB_PAT')
        headers = {'Authorization': f'token {github_token}'}
        response = requests.get(f'https://api.github.com/user/repos', headers=headers)

        if response.status_code != 200:
            return f"ERROR: Unable to retrieve user's repositories. Response Message: {response.text}"
        
        repos = response.json()
        filtered_repos = []
        for repo in repos:
            filtered_repos.append({
                "id": repo["id"],
                "name": repo["name"],
                "html_url": repo["html_url"],
                "description": repo["description"],
                "language": repo["language"],
                "created_at": repo["created_at"],
                "updated_at": repo["updated_at"]
            })
        
        # Use pagination
        start = (page_number - 1) * page_size
        end = start + page_size
        
        # Apply pagination to return string
        total_pages = len(filtered_repos) // page_size + (len(filtered_repos) % page_size > 0)
        return_string = f"User Repositories (Page {page_number} of {total_pages}):\n\n"
        for repo in filtered_repos[start:end]:
            return_string += f"- ID: {repo['id']}\n"
            return_string += f"- Name: {repo['name']}\n"
            return_string += f"- URL: {repo['html_url']}\n"
            return_string += f"- Description: {repo['description']}\n"
            return_string += f"- Language: {repo['language']}\n"
            return_string += f"- Created At: {repo['created_at']}\n"
            return_string += f"- Updated At: {repo['updated_at']}\n"   

        return return_string.encode('utf-8')