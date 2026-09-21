import streamlit as st 
from chatbot_backend import chatbot
from langchain_core.messages import HumanMessage

# st.session_state -> dict -> 
CONFIG = {'configurable': {'thread_id': 'thread-1'}}


# everytime when we press enter after typing our message the whole program is run again and prev msg will be lost

# so in order to overcome this issue we will be using a dictionary to store the messages and load the contents everytime we re-run

if 'message_history' not in st.session_state: 
    st.session_state['message_history']=[] #yaha par session_state ek dictionary ki tarah act kar rha hai jisme message_history se ek key hai jo ki apne aap mein ek dictionary hai jo ki actually mein conversations ko store kar rha hai


# loading the conversation history
for messages in st.session_state['message_history']:
    with st.chat_message(messages['role']):
        st.text(messages['msg'])


user_input=st.chat_input("type here")

if user_input:

    # storing the user message in dictionary
    st.session_state['message_history'].append({'role':'user','msg':user_input})
    with st.chat_message('user'):
        st.text(user_input)


    response = chatbot.invoke(
        {'messages': [HumanMessage(content=user_input)]},
        config=CONFIG
    )

    message = response['messages'][-1]
    content = message.content

    if isinstance(content, list):
        ai_message = "".join(
            part.get("text", "") if isinstance(part, dict) else str(part)
            for part in content
        )
    else:
        ai_message = str(content)

    st.session_state['message_history'].append({'role': 'assistant', 'msg': ai_message})
    with st.chat_message('assistant'):
        st.text(ai_message)