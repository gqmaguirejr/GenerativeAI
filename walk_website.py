#!/usr/bin/python3.11
# -*- coding: utf-8 -*-
# -*- mode: python; python-indent-offset: 4 -*-
# use the Google AI API to look up CEFR levels
#
import time

from dotenv import load_dotenv
load_dotenv()

import sys
import os
import google.generativeai as genai
import re

os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


from bs4 import BeautifulSoup 
import requests 

# the following defaults and functions are from https://medium.com/@shubhamshah30/grammatical-error-correction-using-googles-gemini-ai-634eb009a441
from IPython.display import display
from IPython.display import Markdown


def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

for m in genai.list_models():
  if 'generateContent' in m.supported_generation_methods:
    print(m.name)
    
defaults = {
    'model': 'models/text-bison-001',
    'temperature': 0.7,
    'candidate_count': 1,
    'top_k': 40,
    'top_p': 0.95,
    'max_output_tokens': 1024,
}
def correct_sentence(text):
    # Prompt for correcting the grammar
    prompt_correction = f"Correct the grammar of the following sentence:\nOriginal: {text}\nFixed Grammar:"

    # Assuming the API call returns the corrected text
    response_correction = genai.generate_text(**defaults, prompt=prompt_correction)
    corrected_text = response_correction.result.strip()  # Extract the corrected sentence from the response

    print(f"Corrected Sentence: {corrected_text}")

# ----------------------------------------------------------------------

# lists 
urls=[] 
def content_generation(batches):
    content = []
    for i in batches:
        prompt = '''Create a python dict with value for each of the words a dict with the CEFR level as a key and the value being the part of speech.  Do not forgetting to put in the correct quotation marks when you generate the python dict. Please do not include images. Use the following template for each entry:
  "{word}": {"{CEFR level}": "{Part of Speech}"},
For the word "ecliptiska" this would yield a response of the form.
  "ecliptiska": {"B2": "Adjective"},
Do this for the following Swedish words: '''+f'{i}'
        model = genai.GenerativeModel('gemini-pro')
        try:
            response = model.generate_content(prompt,
                                              safety_settings={
                                                  'HATE': 'BLOCK_NONE',
                                                  'HARASSMENT': 'BLOCK_NONE',
                                                  'SEXUAL' : 'BLOCK_NONE',
                                                  'DANGEROUS' : 'BLOCK_NONE'
                                              }
                                              )
        except ValueError as e:
            print(e)
            print(f'{response.prompt_feedback=}')
            print(f'{reponse.candidate.safety_ratings=}')
            print(f'{response.prompt_feedback.block_reason=}')
            continue
        print(f'{i}: {response.text}')
        if len(response.candidates) > 0:
            candidate = response.candidates[0]
            if candidate.finish_reason  == "STOP":
                content.append(response.text)
            elif candidate.finish_reason  == "SAFETY":
                print('finised due to safety issue')
                content.append(response.text)
            else:
                print(f'finised due to other reason: {candidate.finish_reason=}')
                content.append(response.text)

        else:
            print('no candidates in response')
        time.sleep(1)
    return content
   
# function created 
def scrape(site): 
       
    # getting the request from url 
    r = requests.get(site) 
       
    # converting the text 
    s = BeautifulSoup(r.text,"html.parser") 
       
    for i in s.find_all("a"): 
          
        href = i.attrs['href'] 
           
        if href.startswith("/"): 
            site = site+href 
               
            if site not in  urls: 
                urls.append(site)  
                print(site) 
                # calling it self 
                scrape(site) 
   
# main function 
if __name__ =="__main__": 
   
    # website to be scrape 
    site="http://example.webscraping.com//"
   
    # calling function 
    scrape(site) 
