import streamlit as st 
from chatbot_backend import chatbot
from langchain_core.messages import HumanMessage

# st.session_state -> dict -> 
CONFIG = {'configurable': {'thread_id': 'thread-1'}}


# everytime when we press enter after typing our message the whole program is run again and prev msg will be lost

# so in order to overcome this issue we will be using a dictionary to store the messages and load the contents everytime we re-run

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

# loading the conversation history
for messages in st.session_state['message_history']:
    role = messages.get('role', 'assistant')
    text = messages.get('msg', messages.get('content', ''))
    with st.chat_message(role):
        st.text(text)

user_input = st.chat_input("type here")

if user_input:
    st.session_state['message_history'].append({'role': 'user', 'msg': user_input})
    with st.chat_message('user'):
        st.text(user_input)

    streamed_chunks = []
    with st.chat_message('assistant'):
        for message_chunk, _ in chatbot.stream(
            {'messages': [HumanMessage(content=user_input)]},
            config=CONFIG,
            stream_mode='messages'
        ):
            chunk_content = message_chunk.content
            if isinstance(chunk_content, list):
                text = ''.join(
                    part.get('text', '') if isinstance(part, dict) else str(part)
                    for part in chunk_content
                )
            else:
                text = str(chunk_content)

            if text:
                streamed_chunks.append(text)
                st.write(text)

    ai_message = ''.join(streamed_chunks)
    st.session_state['message_history'].append({'role': 'assistant', 'msg': ai_message})