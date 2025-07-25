import os
from dotenv import load_dotenv
import json
import sseclient
import requests


load_dotenv()

BASE_URI = f"https://chat.botpress.cloud/{os.getenv('CHAT_API_ID')}"
CONVERSATION_ID = "conv_01K0FVZZ2MAM8AR50919S4HZ7K"

#res = requests.get(BASE_URI)
#print(res.content)

class BotpressClient:
    def __init__(self):
        self.headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
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

    def get_user(self):
        return self._request("GET", "/users/me")

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
            "conversationId": conversation_id,
        }
        return self._request("POST", "/messages", json = body)
    

    def listen_conversation(self, conversation_id):
        url = f"{self.base_url}/conversations/{conversation_id}/listen"
        
        for event in sseclient.SSEClient(url, headers = self.headers):
            print(event.data)
            if event.data == "ping":
                continue
            data = json.loads(event.data)["data"]
            yield {
                "id": data["id"],
                "text": data["payload"]["text"]
            }

    def list_messages(self, conversation_id):
        return self._request("GET", f"/conversations/{conversation_id}/messages")




if __name__ == "__main__":

    client = BotpressClient()
    response = client.create_message(CONVERSATION_ID, "Hi from Rizma's script!")
    print("Message sent:", response)

    print("Listening for bot reply...")
    client.listen_conversation(CONVERSATION_ID)
