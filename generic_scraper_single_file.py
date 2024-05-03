from openai import OpenAI
from schemafile2 import schema
from bs4 import BeautifulSoup
import requests
import re 
import json 
from prompt_details import prompt_function_call, get_prompt_functions, get_prompt_messages, prompt_model
import os
import pandas as pd
import logging
import argparse
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
driver = webdriver.Chrome(options=options)
def extract_info(URL,ApiKey):
    try:
        driver.get(URL)
        driver.implicitly_wait(10)
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, "html.parser")
        website_text = soup.get_text(separator=" ")
        website_text_stripped = re.sub(r'\n+', ' ', website_text)
        # print(website_text_stripped)
    except:
        return ['Forbidden', {}]

    if(len(html_content) < 100):
        return ['Forbidden', {}]

 

    client = OpenAI(api_key =ApiKey)
    
    try:
        chat_completion = client.chat.completions.create(
        messages=get_prompt_messages(website_text_stripped),#prompt_messages,
        functions = get_prompt_functions(schema),
        model=prompt_model,
        function_call = prompt_function_call
        )
    except:
        return 'Forbidden', {}

    json_extracted_details = chat_completion.choices[0].message.function_call.arguments
    return 'Permitted', json_extracted_details



def call_llm(URL,ApiKey):
    status, details = extract_info(URL,ApiKey)
    required_keys = list(schema.keys())
    
    ret_json = {}
    ret_json["url"] = URL
    if status == 'Forbidden':
        for key in required_keys:
            ret_json[key] = ""
        return ret_json
    else:
        json_val = json.loads(details)

        for key in required_keys:
            if key not in json_val.keys():
                ret_json[key]=""
            else:
                ret_json[key]=json_val[key]
        return ret_json


