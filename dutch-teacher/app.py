import os
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr

import sys
sys.path.append('..')
from utils import validate_api_keys 

load_dotenv(override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')
validate_api_keys(openai_api_key, False)

openai = OpenAI()
MODEL_GPT = 'gpt-4o-mini'

system_message = """ You are a helpful and friendly dutch teacher (NT2).
User come to you because they want to practise their dutch skills.
You have to carry on the conversation with the user and correct the user's grammar mistakes.
Also pay attention to outdated vocabulary or very formal ways of speaking.
When the user makes a mistakes, correct them heartlightly and ask if they want to go deeper into that 
specific topic.
If they do, always offer a couple of examples of how to do it correctly.
Make the user suggest an specific topic or situation to talk about. If the user cannot choose,
you should suggest a situation and start a conversation.
"""

def chat(message, history):
    """
        message is the latest messge sent by the user.
        history is the whole previous conversation user/assistant without the latest user message
    """
    messages = [{"role": "system", "content": system_message}] + history + [{"role":"user", "content": message}]

    stream = openai.chat.completions.create(
        model=MODEL_GPT,
        messages=messages,
        stream=True
    )

    response = ""
    for chunk in stream:
        response += chunk.choices[0].delta.content or ""
        yield response


view = gr.ChatInterface(title="Dutch teacher AI assistant", fn=chat, type="messages" )
view.launch()