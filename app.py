import streamlit as st
import urllib.parse
import openai

# Set your OpenAI API key securely
openai.api_key = st.secrets["openai"]["api_key"]

# Retrieve and decode query parameters
query_params = st.experimental_get_query_params()
q1 = urllib.parse.unquote(query_params.get('q1', [''])[0])
q2 = urllib.parse.unquote(query_params.get('q2', [''])[0])
q3 = urllib.parse.unquote(query_params.get('q3', [''])[0])
q4 = urllib.parse.unquote(query_params.get('q4', [''])[0])
q5 = urllib.parse.unquote(query_params.get('q5', [''])[0])
q6 = urllib.parse.unquote(query_params.get('q6', [''])[0])
q7 = urllib.parse.unquote(query_params.get('q7', [''])[0])
q8 = urllib.parse.unquote(query_params.get('q8', [''])[0])
q9 = urllib.parse.unquote(query_params.get('q9', [''])[0])
name = urllib.parse.unquote(query_params.get('name', [''])[0])

# Build the prompt
prompt = f"""
Give me an accurate estimation, the best argument, and the best next steps for my personal injury case with these relevant details:

- Case Type: {q1}
- Medical Expenses ($): {q2}
- Future Medical Expenses ($): {q3}
- Short Description of Incident: {q4}
- Lost Income ($): {q5}
- Property Damage ($): {q6}
- Future Lost Income ($): {q7}
- Pain and Suffering Multiplier: {q8}
- Detailed Description: {q9}
- Full Name: {name}
"""

# Display a loading spinner while the API call is made
with st.spinner('Processing your request...'):
    # Make the API call
    response = openai.ChatCompletion.create(
        model="gpt-4-32k",  # Use "gpt-4" or "gpt-4-32k" depending on your access
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=1,
        max_tokens=2000,  # Adjust as needed
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    
    # Extract the response text
    response_text = response['choices'][0]['message']['content'].strip()

# Display a success message
st.success('Request processed successfully!')

# Display the results
st.header('Estimated Case Evaluation')
st.write(response_text)
