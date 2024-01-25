import requests
import json
import csv
import time
import streamlit as st
from datetime import datetime, timedelta
from openai import OpenAI

import os

#from dotenv import load_dotenv
#load_dotenv()
#KEY = os.environ.get("API_KEY")
#ASSISTANT = os.environ.get("ASSISTANT")

KEY = st.secrets["API_KEY"]
ASSISTANT = st.secrets["ASSISTANT"]

def tags_llm(thread, campaign_name, guess):

    message = client.beta.threads.messages.create(
        thread_id = thread.id,
        role = 'user',
        content = f'Provide a guess for the {guess} in the campaign name {campaign_name}'
    )
    
    run = client.beta.threads.runs.create(
        thread_id = thread.id,
        assistant_id = ASSISTANT
    )

    run1 = client.beta.threads.runs.retrieve(
        thread_id = thread.id,
        run_id = run.id
    )   
    
    time.sleep(5)

    messages = client.beta.threads.messages.list(
        thread_id = thread.id
    )
    
    return messages.data[0].content[0].text.value

# Function to simulate processing and updating response boxes
def process_data(thread, campaign_name, selections):
    # This is a placeholder for your actual processing logic
    tag_and_rule = tags_llm(thread, campaign_name, guess = selections)
    starts_with_brace = tag_and_rule.startswith("{")
    ends_with_brace = tag_and_rule.endswith("}")

    guess = ''
    tag = 'Not Applicable'

    if starts_with_brace and ends_with_brace:
        clean_tag_and_rule = tag_and_rule.strip('{}').split(', ')
        guess = clean_tag_and_rule[0]
        tag = clean_tag_and_rule[1]

    results = f"Tag as \n \n \n {guess}"
    return results, guess, tag

if __name__ == "__main__":
    client = OpenAI(api_key=KEY)
    thread = client.beta.threads.create()

    tag_options = [
        'Platform',
        'Country',
        'Language',
        'City',
        'Audience',
    ]

    # Set up the title of the app
    st.title('Tracer Tag LLM')

    # Text input for the campaign name
    default_campaign_name = "GO_LAL_FR_FR_Paris_Q1_2023"
    campaign_name = st.text_input('Enter campaign name here:', value=default_campaign_name)

    # Initialize a list to hold the dropdown selections
    dropdown_selections = []

    # Initialize a dictionary to hold the response placeholders
    responses = {}
    tag_rule = []

    # Initialize a list to hold the dropdown selections and response texts
    dropdown_selections = []
    response_texts = []

    # Create 4 containers for each pair of dropdown and response box
    for i in range(4):
        with st.container():
            col1, col2 = st.columns([2, 3])  # Adjust the width ratio and gap as needed
            with col1:
                # Create a dropdown for each output
                dropdown_selections.append(st.selectbox(f'Option {i+1}', tag_options, key=f'dropdown_{i}'))
            with col2:
                # Create a placeholder for the response text, align it vertically
                response_texts.append(st.empty())

    # Run button at the bottom
    if st.button('Run'):
        progress_bar = st.progress(0)
        # Iterate over the dropdown selections and update the responses
        for i, selection in enumerate(dropdown_selections):
            # Simulate processing and get result
            result, guess, tag = process_data(thread, campaign_name, selection)
            progress_bar.progress((i + 1) * 25)  # Update progress bar by 25% each iteration
            
            # Update the response text using markdown with custom styling for vertical centering
            response_texts[i].markdown(f"<div style='text-align: left; vertical-align: bottom;'>{result}</div>", unsafe_allow_html=True)
            
            if guess != '':
                tag_rule.append((guess, tag))

        # Dynamic creation of sections based on the length of the sample_list
        # Create a row of columns based on the sample_list
        st.header("How it would look in Tracer") 
        columns = st.columns(len(tag_rule))
        for i, (guess, tag) in enumerate(tag_rule, start=0):
            with columns[i]:
                #st.text_input("Field", value="campaign name", key=f'field_{i}')
                #st.text_input("Type", value="Contains", key=f'type_{i}')
                #st.text_input("Contains", value=guess, key=f'contains_{i}')
                #st.text_input("Tag As", value=guess, key=f'tag_{i}')

                st.markdown(f"""
                    <style>
                        .box{i} {{
                            border: 2px solid #ccc;
                            border-radius: 5px;
                            padding: 10px;
                            margin-bottom: 10px;
                        }}
                        .box{i} h1 {{
                            margin-top: 0;
                            font-size: 20px; /* Smaller font size for h1 */
                        }}
                    </style>
                    <div class="box{i}">
                        <h1>Tracer Rule {i+1}</h1>
                        Field: <input type="text" value="campaign name" style="width: 100%;" /><br>
                        Type: <input type="text" value="Contains" style="width: 100%;" /><br>
                        Contains: <input type="text" value="{tag}" style="width: 100%;" /><br>
                        Tag As: <input type="text" value="{guess}" style="width: 100%;" /><br>
                    </div>
                    """, unsafe_allow_html=True)

            