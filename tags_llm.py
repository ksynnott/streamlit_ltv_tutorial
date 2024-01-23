import requests
import json
import csv
import boto3
import time
import streamlit as st
from datetime import datetime, timedelta
from openai import OpenAI

import os
KEY = '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'
ass_id = 'asst_06yKMUj9FAyN4cAxP513ppO7'

def tags_llm(thread, campaign_name, guess):

    message = client.beta.threads.messages.create(
        thread_id = thread.id,
        role = 'user',
        content = f'Provide a guess for the {guess} in the campaign name {campaign_name}'
    )
    
    run = client.beta.threads.runs.create(
        thread_id = thread.id,
        assistant_id = ass_id
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
    guess = tags_llm(thread, campaign_name, guess = selections)
    results = f"Tag as \n \n \n {guess}"
    return results

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

    # Initialize a list to hold the dropdown selections and response texts
    dropdown_selections = []
    response_texts = []

    # Create 4 containers for each pair of dropdown and response box
    for i in range(4):
        with st.container():
            col1, col2 = st.columns([2, 3], gap="small")  # Adjust the width ratio and gap as needed
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
            result = process_data(thread, campaign_name, selection)
            progress_bar.progress((i + 1) * 25)  # Update progress bar by 25% each iteration
            
            # Update the response text using markdown with custom styling for vertical centering
            response_texts[i].markdown(f"<div style='text-align: left; vertical-align: bottom;'>{result}</div>", unsafe_allow_html=True)