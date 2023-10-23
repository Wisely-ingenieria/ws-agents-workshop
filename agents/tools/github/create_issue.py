import os
import requests
from agents.tools import Tool, Parameter

from dotenv import load_dotenv
load_dotenv()

class CreateIssue(Tool):
    def __init__(self):
        super().__init__(
            name="create_issue",
            func=self.create_issue,
            description="Create a new issue on a GitHub repository",
            arguments=[
                Parameter("repo", "The repository to create the issue on. The format should be 'owner-repoName'", str, required=True),
                Parameter("title", "The title of the issue", str, required=True),
                Parameter("body", "The content of the issue in Markdown format", str, required=False)
            ]
        )

    def create_issue(self, repo, title, body):
        github_token = os.getenv('GITHUB_PAT')
        headers = {'Authorization': f'token {github_token}'}
        issue = {'title': title,
                 'body': body}
        response = requests.post(f'https://api.github.com/repos/{repo}/issues', headers=headers, json=issue)

        if response.status_code != 201:
            return f"ERROR: Unable to create issue. Response Message: {response.text}"
        
        issue_info = response.json()
        return_string = f"Issue created successfully:\n"
        return_string += f"- Issue ID: {issue_info['id']}\n"
        return_string += f"- Title: {issue_info['title']}\n"
        return_string += f"- Body: {issue_info['body']}\n"
        return_string += f"- URL: {issue_info['html_url']}"
        
        return return_string