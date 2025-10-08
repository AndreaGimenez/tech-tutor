import os
import json
from week1.brochure import Website
from week1.page_links import get_links
from IPython.display import Markdown, display, update_display
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')

if api_key and api_key.startswith('sk-proj-') and len(api_key)>10:
    print("API key looks good so far")
else:
    print("There might be a problem with your API key? Please visit the troubleshooting notebook!")
    
MODEL = 'gpt-4o-mini'
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

system_prompt = "You are an assistant that analyzes the contents of several relevant pages from a company website \
and creates a short brochure about the company for prospective customers, investors and recruits. Respond in markdown.\
Include details of company culture, customers and careers/jobs if you have the information."

def get_brochure_user_prompt(company_name, url):
    user_prompt=f"You are looking at a company called: {company_name}\n"
    user_prompt += f"Here are the contents of its landing page and other relevant pages; use this information to build a short brochure of the company in markdown.\n"
    user_prompt += get_all_details(url)
    user_prompt = user_prompt[:5_000] # Truncate if more than 5,000 characters
    return user_prompt

def create_brochure(company_name, url):
    response = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt },
            {"role": "user", "content": get_brochure_user_prompt(company_name, url)}
        ]
    )

    result = response.choices[0].message.content
    display(Markdown(result))