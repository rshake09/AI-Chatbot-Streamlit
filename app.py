import streamlit as st
from client import BotpressClient, CONVERSATION_ID

st.title("MedViz AI Assistant")

client = BotpressClient()

# storing messages
if "messages" not in st.session_state:
    messages = client.list_messages(conversation_id = CONVERSATION_ID) [::-1]  # reverse the order
    st.session_state.messages = []

# Displaying messages
for message in st.session_state.messages:
    #with st.chat_message(message["role"]):
    st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Sending message to Botpress
    client.create_message(CONVERSATION_ID, prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})