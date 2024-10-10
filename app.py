import streamlit as st
import urllib.parse
import openai

# Define default session values
session_defaults = {
    'q1': 'Unknown Case Type',
    'q2': '0',
    'q3': '0',
    'q4': 'No incident description',
    'q5': '0',
    'q6': '0',
    'q7': '0',
    'q8': '1.0',
    'q9': 'No detailed description',
    'name': 'Unknown'
}

# Initialize session state with defaults if they don't exist
for key, default_value in session_defaults.items():
    if key not in st.session_state:
        st.session_state[key] = default_value

# Retrieve and decode query parameters
query_params = st.experimental_get_query_params()

# Update session state with query parameters if they exist
for key in session_defaults.keys():
    if key in query_params:
        st.session_state[key] = urllib.parse.unquote(query_params.get(key, [session_defaults[key]])[0])

# Build the prompt using session state values
prompt = f"""
Give me an accurate estimation, the best argument, and the best next steps for my personal injury case with these relevant details:

- Case Type: {st.session_state['q1']}
- Medical Expenses ($): {st.session_state['q2']}
- Future Medical Expenses ($): {st.session_state['q3']}
- Short Description of Incident: {st.session_state['q4']}
- Lost Income ($): {st.session_state['q5']}
- Property Damage ($): {st.session_state['q6']}
- Future Lost Income ($): {st.session_state['q7']}
- Pain and Suffering Multiplier: {st.session_state['q8']}
- Detailed Description: {st.session_state['q9']}
- Full Name: {st.session_state['name']}
"""

# Display a loading spinner while the API call is made
with st.spinner('Processing your request...'):
    try:
        # Make the API call using the correct format
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert providing legal advice for personal injury cases."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        # Extract and display the response
        response_text = response['choices'][0]['message']['content'].strip()

        # Display a success message
        st.success('Request processed successfully!')
        st.header('Estimated Case Evaluation')
        st.write(response_text)

    except Exception as e:
        st.error(f"An error occurred: {e}")
