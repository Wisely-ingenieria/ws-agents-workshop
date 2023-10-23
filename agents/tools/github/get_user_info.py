import os
import requests
from agents.tools import Tool

from dotenv import load_dotenv
load_dotenv()

class GetUserInfo(Tool):
    def __init__(self):
        super().__init__(
            name="get_user",
            func=self.get_user_profile,
            description="Get user's Github profile information",
            arguments=[]
        )

    def get_user_profile(self):
        github_token = os.getenv('GITHUB_PAT')
        headers = {'Authorization': f'token {github_token}'}
        response = requests.get('https://api.github.com/user', headers=headers)

        if response.status_code != 200:
            return f"ERROR: Unable to retrieve user's profile information. Response Message: {response.text}"
        
        user_info = response.json()
        return_string = f"Retrieved user's profile information:\n"
        return_string += f"- Username: {user_info['login']}\n"
        return_string += f"- ID: {user_info['id']}\n"
        return_string += f"- URL: {user_info['html_url']}\n"
        return_string += f"- Avatar: {user_info['avatar_url']}\n"
        return_string += f"- Created At: {user_info['created_at']}\n"
        return_string += f"- Updated At: {user_info['updated_at']}"
        
        return return_string
