#!/usr/bin/python3.11
# -*- coding: utf-8 -*-
# -*- mode: python; python-indent-offset: 4 -*-
# use the Google AI API to look up CEFR levels
#
import time

word_list=[
    'Glass­box-metoden',
    'Layer­2­teknologier',
    'Linköping',
    'anpassnings',
    'enstegs-',
    'interaktions-',
    'irakisk-',
    'isär-',
    'klock-',
    'klockfas-',
    'konstruktions-',
    'langsammare',
    'levande-',
    'lokala-',
    'lång-',
    'långsamt',
    'mitt-',
    'modellanpassnings',
    'modellerings-',
    'människa-',
    'pension-',
    'produktionskallor',
    'regel-',
    'sopor',
    'state-action-par',
    'täcknings',
    'underskattades',
    'uppdrags-',
    'upptäckt-',
    'varnings-',
    'verktygs-',
    'yrkesliv-',
    'ångström',
    'öppen-',
    'öppet-',
]


from dotenv import load_dotenv
load_dotenv()

import os
import google.generativeai as genai
import re

os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(prompt):
    model = genai.GenerativeModel('gemini-pro')
    try:
        response = model.generate_content(prompt)
    except ValueError as e:
        print(e)
        print(f'{response.prompt_feedback=}')
    return response

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

def clean_text(text):
    # Remove extra whitespaces and newlines
    cleaned_text = re.sub('\s+', ' ', text).strip()

    # Remove markdown-style bullet points, asterisks, and numeric bullet points
    cleaned_text = re.sub(r'[*-]\s*|\d+\.\s*', '', cleaned_text)

    # Remove extra spaces before and after colons
    cleaned_text = re.sub(r'\s*:\s*', ': ', cleaned_text)

    # Remove extra spaces before and after hyphens
    cleaned_text = re.sub(r'\s*-\s*', ' - ', cleaned_text)
    
    return cleaned_text


def download_button(file_path,topic):
    # Read the content of the PPT file
    with open(file_path, "rb") as file:
        ppt_content = file.read()

#model = genai.GenerativeModel('gemini-pro')

def divide_chunks(l, n): 
      
    # looping till length l 
    for i in range(0, len(l), n):  
        yield l[i:i + n] 
  
 

def main():
    global content
    content = []

    batches = list(divide_chunks(word_list, 40)) 
    final_content=content_generation(batches)
    print(final_content)
    
if __name__ == "__main__": main()

