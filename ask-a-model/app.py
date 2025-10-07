# imports
import os
import requests
from dotenv import load_dotenv
from openai import OpenAI
from IPython.display import Markdown, display, update_display
import google.generativeai 

import gradio as gr
# from utils import validate_api_keys 

# constants
MODEL_GPT = 'gpt-4o-mini'
MODEL_GEMINI='gemini-2.5-flash-lite'

load_dotenv(override=True)

openai_api_key = os.getenv('OPENAI_API_KEY')
google_api_key = os.getenv('GOOGLE_API_KEY')

# validate_api_keys(openai_api_key, google_api_key)

openai=OpenAI()


system_message = "You are a helpful assistant"

def stream_gpt(prompt):
    messages = [
        {
            "role":"system", "content": system_message
        }, 
        {
            "role":"user", "content": prompt
        }
    ]

    stream = openai.chat.completions.create(model=MODEL_GPT, messages=messages, stream=True)
    result = ""
    for chunk in stream:
        result += chunk.choices[0].delta.content or ""
        yield result

def stream_gemini(prompt):
    gemini_via_openai_client = OpenAI(
    api_key=google_api_key, 
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
    stream = gemini_via_openai_client.chat.completions.create(
        model=MODEL_GEMINI,
        messages=[
            {
                "role":"system", "content": system_message
            }, 
            {
                "role":"user", "content": prompt
            }
        ],
        stream=True
    )
    result = ""
    for chunk in stream:
        result += chunk.choices[0].delta.content or ""
        yield result

def stream_model(prompt, model):
    if model=="GPT":
        result = stream_gpt(prompt)
    elif model=="Gemini":
        result = stream_gemini(prompt)
    else:
        raise ValueError("Unknown model")
    yield from result


view = gr.Interface(
    fn=stream_model,
    inputs=[gr.Textbox(label="Your message:", lines=6), gr.Dropdown(["GPT", "Gemini"], label="Select model", value="GPT")],
    outputs=[gr.Markdown(label="Response:")],
    flagging_mode="never"
)
view.launch()

