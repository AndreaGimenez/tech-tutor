import sys
sys.path.append('..')
from utils import validate_api_keys 
from tools import flight_price_function, hotel_price_function, handle_tool_call
import os
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr

load_dotenv(override=True)

openai_api_key = os.getenv('OPENAI_API_KEY')
validate_api_keys(openai_api_key, False)

MODEL = "gpt-4o-mini"
openai = OpenAI()

system_message = "You are a helpful assistant for an Airline called FlightAI. "
system_message += "Give short, courteous answers, no more than 1 sentence. "
system_message += "Always be accurate. If you don't know the answer, say so."

tools = [
    {"type": "function", "function": flight_price_function}, 
    {"type": "function", "function": hotel_price_function}
] 


def chat(message, history):
    messages = [{"role": "system", "content": system_message }] + history + [{"role": "user", "content": message }]
    response = openai.chat.completions.create(model=MODEL, messages=messages, tools=tools)

    if response.choices[0].finish_reason == "tool_calls":
        message = response.choices[0].message
        print(f"message: {message}")
        tool_responses = handle_tool_call(message)
        print(f"tool_responses: ", tool_responses)
        messages.append(message)
        messages.extend(tool_responses)
        response = openai.chat.completions.create(model=MODEL, messages=messages)
    
    return response.choices[0].message.content

view = gr.ChatInterface(fn=chat, type="messages")
view.launch()