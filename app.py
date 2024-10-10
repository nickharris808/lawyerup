import openai

# Set your OpenAI API key securely
openai.api_key = st.secrets["openai"]["api_key"]

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
    try:
        # Make the API call using the correct format
        response = openai.ChatCompletion.create(
            model="gpt-4",  # or "gpt-3.5-turbo" depending on your access
            messages=[
                {"role": "system", "content": "You are an expert providing legal advice for personal injury cases."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000,  # Adjust as needed
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
