from openai import OpenAI
from Home import chat_window
import streamlit as st

import openai

openai.api_key = st.secrets["api_keys"]["openai_api_key"]


def create_assistant(file_path, new_message, thread_id=None):
    client = OpenAI(api_key=openai.api_key)

    assistant_id = "asst_VRAa7H9EuS6dZB4x8gJvj3sw"
    
    if thread_id is None:
        file = client.files.create(
            file=open(file_path, "rb"),
            purpose='assistants',
        )

        thread = client.beta.threads.create(
            messages=[
                {
                    "role": "user",
                    "content": new_message,
                    "attachments": [
                        { "file_id": file.id, "tools": [{"type": "code_interpreter"}]}
                    ]
                }
            ]
        )
        thread_id = thread.id

    else:
        message = client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=new_message
        )

    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread_id,
        assistant_id=assistant_id,
    )

    if run.status == 'completed':
        messages = client.beta.threads.messages.list(
            thread_id=thread_id
        )

    response = messages.data[0].content[0].text.value

    return response, thread_id
