# imports
import os
import requests
from dotenv import load_dotenv
from openai import OpenAI

# constants
MODEL_GPT = 'gpt-4o-mini'

# set up environment
load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')

if api_key and api_key.startswith('sk-proj-') and len(api_key)>10:
    print("API key looks good so far")
else:
    print("There might be a problem with your API key? Please visit the troubleshooting notebook!")

openai = OpenAI()

def get_system_prompt():
    system_prompt="You are an expert in software development.\n"
    system_prompt+="You will receive fragments of code from other developers and will explain in detail what it does."
    return system_prompt

def get_user_prompt(code):
    return f"Please explain what this code does and why: \n {code}"


# Get gpt-4o-mini to answer, with streaming
def ask_tutor(code):
    stream = openai.chat.completions.create(
        model=MODEL_GPT,
         messages=[
            {"role": "system", "content": get_system_prompt()},
            {"role": "user", "content": get_user_prompt(code)},
        ],
        stream=True
    )
    return stream
