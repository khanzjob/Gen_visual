import requests
import os
from dotenv import find_dotenv ,load_dotenv
dotenv_path= find_dotenv()
load_dotenv(dotenv_path)
username = os.getenv("SunbirdUsername")
password = os.getenv("SunbirdPassword")
AccesToken = os.getenv("SunbirdAccessToken")

url = 'https://sunbird-ai-api-5bq6okiwgq-ew.a.run.app'
creds = {
    'username': '{username}',
    'password': '{password}'
}
response = requests.post(f'{url}/auth/token', data=creds)
token = response.json()['access_token']
print(token)