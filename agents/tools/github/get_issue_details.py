import os
import requests
from agents.tools import Tool, Parameter
from dotenv import load_dotenv

load_dotenv()

class GetIssueDetails(Tool):
    def __init__(self):
        super().__init__(
            name="get_issue_details",
            func=self.get_issue_details,
            description="Get details of a specific issue from a Github repository",
            arguments=[
                Parameter("repo", "The repository to get the issue from. The format should be 'owner/repoName'", str, required=True),
                Parameter("issue_number", "The number of the issue", int, required=True),
            ]
        )

    def get_issue_details(self, repo, issue_number):
        github_token = os.getenv('GITHUB_PAT')
        headers = {'Authorization': f'token {github_token}'}
        response = requests.get(f'https://api.github.com/repos/{repo}/issues/{issue_number}', headers=headers)

        if response.status_code != 200:
            return f"ERROR: Unable to retrieve issue details. Response Message: {response.text}"

        issue = response.json()
        return_string = f"Details for issue {issue_number} in repository {repo}:\n"
        return_string += f"- Issue ID: {issue['id']}\n"
        return_string += f"- Title: {issue['title']}\n"
        return_string += f"- State: {issue['state']}\n"
        return_string += f"- URL: {issue['html_url']}\n"
        return_string += f"- Created At: {issue['created_at']}\n"
        return_string += f"- Updated At: {issue['updated_at']}\n"
        return_string += f"- Body: {issue['body']}\n"

        return return_string