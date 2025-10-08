import os
import json
from Website import Website
from page_links import get_links 
from IPython.display import Markdown, display, update_display
from dotenv import load_dotenv
from openai import OpenAI
import google.generativeai 
import gradio as gr

import sys
sys.path.append('..')
from utils import validate_api_keys 

load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')
google_api_key = os.getenv('GOOGLE_API_KEY')

validate_api_keys(api_key, google_api_key)
    
MODEL_GPT = 'gpt-4o-mini'
MODEL_GEMINI='gemini-2.5-flash-lite'

openai = OpenAI()

def get_all_details(url):
    result = "Landing page: \n"
    website = Website(url)
    result += website.get_contents()
    links = get_links(website)["links"]

    for link in links:
        result += f"\n\n{link['type']}\n"
        result += Website(link['url']).get_contents()
    
    return result

def get_brochure_system_prompt(tone):
    return f"You are an assistant that analyzes the contents of several relevant pages from a company website \
    and creates a short brochure about the company for prospective customers, investors and recruits. Respond in markdown.\
    Include details of company culture, customers and careers/jobs if you have the information. Your tone is the one of a {tone}."

def get_brochure_user_prompt(company_name, url):
    user_prompt=f"You are looking at a company called: {company_name}\n"
    user_prompt += f"Here are the contents of its landing page and other relevant pages; use this information to build a short brochure of the company in markdown.\n"
    user_prompt += get_all_details(url)
    return user_prompt

def stream_brochure(company_name, url, model, tone):
    messages=[
        {"role": "system", "content": get_brochure_system_prompt(tone) },
        {"role": "user", "content": get_brochure_user_prompt(company_name, url)}
    ]

    if (model == 'GPT'):
        stream = openai.chat.completions.create(
            model=MODEL_GPT,
            messages=messages,
            stream=True
        )

    elif(model == 'Gemini'):
        gemini_via_openai_client = OpenAI(
        api_key=google_api_key, 
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

        stream = gemini_via_openai_client.chat.completions.create(
            model=MODEL_GEMINI,
            messages=messages,
            stream=True
        )
    else:
        raise ValueError(f"Unknown model: {model}")

    result = ""
    for chunk in stream:
        result += chunk.choices[0].delta.content or ""
        yield result


view = gr.Interface(
    fn=stream_brochure,
    inputs=[gr.Textbox(label="Company name"),
            gr.Textbox(label="Company url"), 
            gr.Dropdown(["GPT", "Gemini"], label="Select model", value="GPT"), 
            gr.Dropdown(["sales person", "hiring perdon", "comedian person", "5 year old kid"], label="Select tone", value="Oriented to sales")],
    outputs=[gr.Markdown(label="Brochure")],
    flagging_mode="never"
)

view.launch()