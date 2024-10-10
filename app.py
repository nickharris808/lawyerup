import streamlit as st
import openai

# Set your OpenAI API key
openai.api_key = 'your-openai-api-key'

# Function to generate the OpenAI prompt
def generate_prompt(form_data):
    prompt = f"""
You are an experienced personal injury attorney. Based on the following client information, provide a case valuation and explain your reasoning.

### Client Information:

**Personal Information:**
- Full Name: {form_data['full_name']}
- Contact Information:
  - Phone Number: {form_data['phone_number']}
  - Email Address: {form_data['email']}
- Address: {form_data['address']}
- Date of Birth: {form_data['date_of_birth']}

**Incident Details:**
- Date of Incident: {form_data['incident_date']}
- Location of Incident: {form_data['incident_location']}
- Short Description: {form_data['incident_description']}

**Case Type:** {form_data['case_type']}

**Losses and Damages:**
- Current Medical Expenses: ${form_data['current_medical_expenses']}
- Future Medical Expenses: ${form_data['future_medical_expenses']}
- Current Lost Wages: ${form_data['current_lost_wages']}
- Future Lost Income: ${form_data['future_lost_income']}
- Property Damage: ${form_data['property_damage']}
- Pain and Suffering Multiplier: {form_data['pain_suffering_multiplier']}

**Additional Information:**
- Detailed Description: {form_data['detailed_description']}

"""
    # Add dynamic questions based on case type
    if form_data['case_type'] == 'Personal Injury':
        prompt += f"""
**Additional Questions:**
- Were you at fault?: {form_data['at_fault']}
- Did you receive a citation?: {form_data['citation_received']}
"""
    elif form_data['case_type'] == 'Medical Malpractice':
        prompt += f"""
**Additional Questions:**
- Nature of Malpractice: {form_data['malpractice_nature']}
- Was another provider involved?: {form_data['other_provider_involved']}
"""
    return prompt

# Initialize session state for multi-step form
if 'step' not in st.session_state:
    st.session_state.step = 1

form_data = {}

# Step 1: Personal Information
if st.session_state.step == 1:
    st.title("Personal Injury Case Evaluation")
    st.header("Step 1: Personal Information")
    st.progress(16)

    with st.form(key='personal_info_form'):
        full_name = st.text_input("Full Name")
        phone_number = st.text_input("Phone Number")
        email = st.text_input("Email Address")
        address = st.text_input("Address")
        date_of_birth = st.date_input("Date of Birth")

        submit = st.form_submit_button("Next")
        if submit:
            form_data['full_name'] = full_name
            form_data['phone_number'] = phone_number
            form_data['email'] = email
            form_data['address'] = address
            form_data['date_of_birth'] = date_of_birth.strftime("%Y-%m-%d")
            st.session_state.update(form_data)
            st.session_state.step = 2
            st.experimental_rerun()

# Step 2: Incident Details
if st.session_state.step == 2:
    st.header("Step 2: Incident Details")
    st.progress(32)

    with st.form(key='incident_details_form'):
        incident_date = st.date_input("Date of Incident")
        incident_location = st.text_input("Location of Incident")
        incident_description = st.text_area("Short Description", max_chars=500)

        submit = st.form_submit_button("Next")
        if submit:
            form_data['incident_date'] = incident_date.strftime("%Y-%m-%d")
            form_data['incident_location'] = incident_location
            form_data['incident_description'] = incident_description
            st.session_state.update(form_data)
            st.session_state.step = 3
            st.experimental_rerun()

# Step 3: Case Type Selection
if st.session_state.step == 3:
    st.header("Step 3: Case Type Selection")
    st.progress(48)

    with st.form(key='case_type_form'):
        case_type = st.selectbox("Case Type", ["Personal Injury", "Medical Malpractice", "Workplace Injury", "Product Liability", "Other"])
        submit = st.form_submit_button("Next")
        if submit:
            form_data['case_type'] = case_type
            st.session_state.update(form_data)
            st.session_state.step = 4
            st.experimental_rerun()

# Step 4: Losses and Damages
if st.session_state.step == 4:
    st.header("Step 4: Losses and Damages")
    st.progress(64)

    with st.form(key='losses_damages_form'):
        current_medical_expenses = st.number_input("Current Medical Expenses", min_value=0.0, format="%.2f")
        future_medical_expenses = st.number_input("Future Medical Expenses", min_value=0.0, format="%.2f")
        current_lost_wages = st.number_input("Current Lost Wages", min_value=0.0, format="%.2f")
        future_lost_income = st.number_input("Future Lost Income", min_value=0.0, format="%.2f")
        property_damage = st.number_input("Property Damage", min_value=0.0, format="%.2f")
        pain_suffering_multiplier = st.selectbox("Pain and Suffering Multiplier", [1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5])

        submit = st.form_submit_button("Next")
        if submit:
            form_data['current_medical_expenses'] = current_medical_expenses
            form_data['future_medical_expenses'] = future_medical_expenses
            form_data['current_lost_wages'] = current_lost_wages
            form_data['future_lost_income'] = future_lost_income
            form_data['property_damage'] = property_damage
            form_data['pain_suffering_multiplier'] = pain_suffering_multiplier
            st.session_state.update(form_data)
            st.session_state.step = 5
            st.experimental_rerun()

# Step 5: Additional Information
if st.session_state.step == 5:
    st.header("Step 5: Additional Information")
    st.progress(80)

    with st.form(key='additional_info_form'):
        detailed_description = st.text_area("Detailed Description", max_chars=1000)

        # Dynamic Questions
        if st.session_state.case_type == 'Personal Injury':
            at_fault = st.selectbox("Were you at fault?", ["Yes", "No"])
            citation_received = st.selectbox("Did you receive a citation?", ["Yes", "No"])
            form_data['at_fault'] = at_fault
            form_data['citation_received'] = citation_received

        elif st.session_state.case_type == 'Medical Malpractice':
            malpractice_nature = st.selectbox("Nature of Malpractice", ["Misdiagnosis", "Surgical Error", "Medication Error", "Other"])
            other_provider_involved = st.selectbox("Was another provider involved?", ["Yes", "No"])
            form_data['malpractice_nature'] = malpractice_nature
            form_data['other_provider_involved'] = other_provider_involved

        submit = st.form_submit_button("Next")
        if submit:
            form_data['detailed_description'] = detailed_description
            st.session_state.update(form_data)
            st.session_state.step = 6
            st.experimental_rerun()

# Step 6: Review & Submission
if st.session_state.step == 6:
    st.header("Step 6: Review & Submit")
    st.progress(100)

    st.subheader("Please review your information before submission:")
    st.write("**Full Name:**", st.session_state.full_name)
    st.write("**Phone Number:**", st.session_state.phone_number)
    st.write("**Email Address:**", st.session_state.email)
    st.write("**Address:**", st.session_state.address)
    st.write("**Date of Birth:**", st.session_state.date_of_birth)

    st.write("**Date of Incident:**", st.session_state.incident_date)
    st.write("**Location of Incident:**", st.session_state.incident_location)
    st.write("**Short Description:**", st.session_state.incident_description)

    st.write("**Case Type:**", st.session_state.case_type)

    st.write("**Current Medical Expenses:** $", st.session_state.current_medical_expenses)
    st.write("**Future Medical Expenses:** $", st.session_state.future_medical_expenses)
    st.write("**Current Lost Wages:** $", st.session_state.current_lost_wages)
    st.write("**Future Lost Income:** $", st.session_state.future_lost_income)
    st.write("**Property Damage:** $", st.session_state.property_damage)
    st.write("**Pain and Suffering Multiplier:**", st.session_state.pain_suffering_multiplier)

    st.write("**Detailed Description:**", st.session_state.detailed_description)

    if st.session_state.case_type == 'Personal Injury':
        st.write("**Were you at fault?:**", st.session_state.at_fault)
        st.write("**Did you receive a citation?:**", st.session_state.citation_received)
    elif st.session_state.case_type == 'Medical Malpractice':
        st.write("**Nature of Malpractice:**", st.session_state.malpractice_nature)
        st.write("**Was another provider involved?:**", st.session_state.other_provider_involved)

    agree = st.checkbox('I agree to the Privacy Policy and Consent to Contact.')

    if st.button("Submit") and agree:
        # Generate the OpenAI prompt
        prompt = generate_prompt(st.session_state)

        # Call the OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=1,
            max_tokens=1500,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        # Display the results
        st.success("Your case valuation is ready!")
        st.header("Case Valuation")
        st.write(response['choices'][0]['message']['content'])
    elif not agree:
        st.warning("You must agree to the Privacy Policy and Consent to Contact before submitting.")

