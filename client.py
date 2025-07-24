import os
import requests
from dotenv import load_dotenv
import json
import sseclient

load_dotenv()

BASE_URI = f"https://chat.botpress.cloud/{os.getenv('CHAT_API_ID')}"
CONVERSATION_ID = "conv_01K0FVZZ2MAM8AR50919S4HZ7K"

#res = requests.get(BASE_URI)
#print(res.content)

class BotpressClient:
    def __init__(self):
        self.headers = {
            "accept": "application/json",
            "Content-type": "application/json",
            "x-user-key": os.getenv("USER_KEY"),
        }
        self.base_url = BASE_URI

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

    def create_convo(self):
        return self._request("POST", "/conversations", json = {"body": {}})
    
    def create_message(self, conversation_id, message):
        body = {
            "payload": {
                "type": "text",
                "text": message
            },
            "conversationID": conversation_id,
        }
        return self._request("POST", "/messages", json = body)
    
    def list_messages(self, conversation_id):
        return self._request("GET", "/messages")

    def listen_to_stream(self, conversation_id):
        url = f"{self.base_url}/conversations/{conversation_id}/listen"
        
        for event in sseclient.SSEClient(url, headers = self.headers):
            print(event.data)




if __name__ == "__main__":
    client = BotpressClient()
    
    #print(client.create_user("Rizma", "1234"))
    #print(client.create_convo())
    client.listen_to_stream(CONVERSATION_ID)