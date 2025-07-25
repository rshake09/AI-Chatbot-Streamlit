import streamlit as st
import json
import os
from client import BotpressClient, CONVERSATION_ID

st.title("MedViz AI Assistant")

client = BotpressClient()

user = client.get_user()
user_id = user["user"]["id"]

# storing messages
if "messages" not in st.session_state:
    st.session_state.messages = []

    messages = client.list_messages(conversation_id = CONVERSATION_ID) 

    for message in messages["messages"][::-1]:  # reverse the order of list
        
        role = "user" if message["userId"] == user_id else "assistant"
        text = message["payload"]["text"]
        st.session_state.messages.append({"role": role, "content": text})

def save_messages_to_file():
    os.makedirs("outputs", exist_ok = True)
    with open("outputs/messages.json", "w") as f:
        json.dump(st.session_state.messages, f, indent = 2)

# Displaying messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    save_messages_to_file()

    with st.chat_message("user"):
        st.markdown(prompt)

    # Sending message to Botpress
    client.create_message(CONVERSATION_ID, prompt)

    with st.chat_message("assistant"):

        response_box = st.empty()
        last_rendered_id = ""

        for message in client.listen_conversation(CONVERSATION_ID):
            if message["id"] != last_rendered_id:
                last_rendered_id = message["id"]
                response_box.markdown(message["text"])

                st.session_state.messages.append({"role": "assistant", "content": message["text"]})
                save_messages_to_file()