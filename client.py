import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URI = f"https://chat.botpress.cloud/{os.getenv('CHAT_API_ID')}/hello"

res = requests.get(BASE_URI)
print(res.content)

class BotpressClient:
    def __init__(self):
        self.headers = {
            "accept": "application/json",
            "Content-type": "application/json",
        }

    def _request(self, method, path, json = None):
        url = f"{BASE_URI}{path}"

        try:
            response = requests.request(method, url, headers = self.headers, json = json)
            response.raise_for_status()  
            return response.json()
        
        except requests.HTTPError:
            return response.status_code, response.text

    def create_user(self, name, id):
        user_data = {"name": name, "id": id}
        return self._request("POST", "/users", json = user_data)


if __name__ == "__main__":
    client = BotpressClient()
    
    print(client.create_user("Rizma", "12345"))