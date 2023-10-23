import os
import requests
from agents.tools import Tool, Parameter

from dotenv import load_dotenv
load_dotenv()

class GetIssues(Tool):
    def __init__(self):
        super().__init__(
            name="get_issues",
            func=self.get_repo_issues,
            description="Get issues from a Github repository",
            arguments=[
                Parameter("repo", "The repository to get the issues from. The format should be 'owner/repoName'", str, required=True),
                Parameter("state", "Indicates the state of the issues to return. Either open, closed, or all. Default='open'", str, required=False),
                Parameter("page_size", "The size of each page. Default=25.", int, required=False),
                Parameter("page_number", "The page number to return. Default=1.", int, required=False)
            ]
        )

    def get_repo_issues(self, repo, state='open', page_size=25, page_number=1):
        github_token = os.getenv('GITHUB_PAT')
        headers = {'Authorization': f'token {github_token}'}
        response = requests.get(f'https://api.github.com/repos/{repo}/issues?state={state}', headers=headers)

        if response.status_code != 200:
            return f"ERROR: Unable to retrieve repository's issues. Response Message: {response.text}"

        issues = response.json()
        
        # Use pagination
        start = (page_number - 1) * page_size
        end = start + page_size
        page_issues = issues[start:end]

        total_pages = len(issues) // page_size + (len(issues) % page_size > 0)
        return_string = f"Issues for repository {repo} (Page {page_number} of {total_pages}):\n"
        for issue in page_issues:
            return_string += f"Issue # {issue['id']}: {issue['title']} ({issue['state']}) URL: {issue['html_url']}\n"

        return return_string