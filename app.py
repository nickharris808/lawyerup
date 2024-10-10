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
- Phone Number: {form_data['phone_number']}
- Email Address: {form_data['email']}

**Incident Details:**
- Date of Incident: {form_data['incident_date']}
- Case Type: {form_data['case_type']}
- Short Description: {form_data['incident_description']}

**Losses and Damages:**
- Medical Expenses: ${form_data['medical_expenses']}
- Future Medical Expenses: ${form_data['future_medical_expenses']}
- Lost Income: ${form_data['lost_income']}
- Future Lost Income: ${form_data['future_lost_income']}
- Property Damage: ${form_data['property_damage']}
- Pain and Suffering Multiplier: {form_data['pain_suffering_multiplier']}

**Additional Information:**
- Detailed Description: {form_data['detailed_description']}
"""
    # Add dynamic questions based on case type
    if form_data['case_type'] == 'Motor Vehicle Accident':
        prompt += f"""
**Additional Questions:**
- Were you the driver or passenger?: {form_data['driver_or_passenger']}
- Was another vehicle involved?: {form_data['other_vehicle_involved']}
"""
    elif form_data['case_type'] == 'Personal Injury':
        prompt += f"""
**Additional Questions:**
- Type of injury (e.g., slip and fall, dog bite): {form_data['injury_type']}
- Was the incident on public or private property?: {form_data['property_type']}
"""
    elif form_data['case_type'] == 'Medical Malpractice':
        prompt += f"""
**Additional Questions:**
- Type of malpractice (e.g., misdiagnosis, surgical error): {form_data['malpractice_type']}
- Did you sign any consent forms?: {form_data['consent_forms']}
"""
    elif form_data['case_type'] == 'Workplace Injury':
        prompt += f"""
**Additional Questions:**
- Were you on the clock when the injury occurred?: {form_data['on_the_clock']}
- Did you report the injury to your employer?: {form_data['reported_to_employer']}
"""
    elif form_data['case_type'] == 'Product Liability':
        prompt += f"""
**Additional Questions:**
- Type of product involved: {form_data['product_type']}
- Was there a recall on the product?: {form_data['product_recall']}
"""
    elif form_data['case_type'] == 'Other':
        prompt += f"""
**Additional Questions:**
- Please specify the case type: {form_data['other_case_type']}
- Any additional details: {form_data['other_details']}
"""
    return prompt

# Initialize session state for multi-step form
if 'step' not in st.session_state:
    st.session_state['step'] = 1

if 'form_data' not in st.session_state:
    st.session_state['form_data'] = {}

# Helper functions to navigate between steps
def next_step():
    st.session_state['step'] += 1

def prev_step():
    if st.session_state['step'] > 1:
        st.session_state['step'] -= 1

# Define the total number of steps
TOTAL_STEPS = 5

# Main application
def main():
    st.title("Personal Injury Case Evaluation")
    st.progress((st.session_state['step'] - 1) * (100 // TOTAL_STEPS))

    if st.session_state['step'] == 1:
        personal_info()
    elif st.session_state['step'] == 2:
        incident_details()
    elif st.session_state['step'] == 3:
        losses_and_damages()
    elif st.session_state['step'] == 4:
        additional_info()
    elif st.session_state['step'] == 5:
        review_and_submit()

def personal_info():
    st.header("Step 1: Personal Information")
    with st.form(key='personal_info_form'):
        full_name = st.text_input("Full Name", value=st.session_state['form_data'].get('full_name', ''))
        phone_number = st.text_input("Phone Number", value=st.session_state['form_data'].get('phone_number', ''))
        email = st.text_input("Email Address", value=st.session_state['form_data'].get('email', ''))

        col1, col2 = st.columns(2)
        with col1:
            back = st.form_submit_button("Back", on_click=prev_step)
        with col2:
            next = st.form_submit_button("Next")

        if next:
            st.session_state['form_data']['full_name'] = full_name
            st.session_state['form_data']['phone_number'] = phone_number
            st.session_state['form_data']['email'] = email
            next_step()

def incident_details():
    st.header("Step 2: Incident Details")
    with st.form(key='incident_details_form'):
        incident_date = st.date_input("Date of Incident", value=st.session_state['form_data'].get('incident_date', None))
        case_type_options = ["Motor Vehicle Accident", "Personal Injury", "Medical Malpractice", "Workplace Injury", "Product Liability", "Other"]
        case_type = st.selectbox("Case Type", case_type_options, index=st.session_state['form_data'].get('case_type_index', 0))
        incident_description = st.text_area("Short Description", value=st.session_state['form_data'].get('incident_description', ''), max_chars=500)

        col1, col2 = st.columns(2)
        with col1:
            back = st.form_submit_button("Back", on_click=prev_step)
        with col2:
            next = st.form_submit_button("Next")

        if next:
            st.session_state['form_data']['incident_date'] = incident_date.strftime("%Y-%m-%d")
            st.session_state['form_data']['case_type'] = case_type
            st.session_state['form_data']['incident_description'] = incident_description
            st.session_state['form_data']['case_type_index'] = case_type_options.index(case_type)
            next_step()

def losses_and_damages():
    st.header("Step 3: Losses and Damages")
    with st.form(key='losses_damages_form'):
        medical_expenses = st.number_input("Medical Expenses ($)", min_value=0.0, format="%.2f", value=st.session_state['form_data'].get('medical_expenses', 0.0))
        future_medical_expenses = st.number_input("Future Medical Expenses ($)", min_value=0.0, format="%.2f", value=st.session_state['form_data'].get('future_medical_expenses', 0.0))
        lost_income = st.number_input("Lost Income ($)", min_value=0.0, format="%.2f", value=st.session_state['form_data'].get('lost_income', 0.0))
        future_lost_income = st.number_input("Future Lost Income ($)", min_value=0.0, format="%.2f", value=st.session_state['form_data'].get('future_lost_income', 0.0))
        property_damage = st.number_input("Property Damage ($)", min_value=0.0, format="%.2f", value=st.session_state['form_data'].get('property_damage', 0.0))

        pain_suffering_multiplier = st.slider("Pain and Suffering Multiplier (1-5)", min_value=1, max_value=5, value=st.session_state['form_data'].get('pain_suffering_multiplier', 1))
        st.caption("A number used to represent the value of your accumulated pain and suffering, including stress, anxiety, and physical discomfort.")

        col1, col2 = st.columns(2)
        with col1:
            back = st.form_submit_button("Back", on_click=prev_step)
        with col2:
            next = st.form_submit_button("Next")

        if next:
            st.session_state['form_data']['medical_expenses'] = medical_expenses
            st.session_state['form_data']['future_medical_expenses'] = future_medical_expenses
            st.session_state['form_data']['lost_income'] = lost_income
            st.session_state['form_data']['future_lost_income'] = future_lost_income
            st.session_state['form_data']['property_damage'] = property_damage
            st.session_state['form_data']['pain_suffering_multiplier'] = pain_suffering_multiplier
            next_step()

def additional_info():
    st.header("Step 4: Additional Information")
    with st.form(key='additional_info_form'):
        detailed_description = st.text_area("Detailed Description", value=st.session_state['form_data'].get('detailed_description', ''), max_chars=1000)

        # Dynamic Questions based on Case Type
        case_type = st.session_state['form_data']['case_type']

        if case_type == 'Motor Vehicle Accident':
            driver_or_passenger_options = ["Driver", "Passenger"]
            driver_or_passenger = st.selectbox("Were you the driver or passenger?", driver_or_passenger_options, index=st.session_state['form_data'].get('driver_or_passenger_index', 0))
            other_vehicle_involved_options = ["Yes", "No"]
            other_vehicle_involved = st.selectbox("Was another vehicle involved?", other_vehicle_involved_options, index=st.session_state['form_data'].get('other_vehicle_involved_index', 0))
            st.session_state['form_data']['driver_or_passenger'] = driver_or_passenger
            st.session_state['form_data']['driver_or_passenger_index'] = driver_or_passenger_options.index(driver_or_passenger)
            st.session_state['form_data']['other_vehicle_involved'] = other_vehicle_involved
            st.session_state['form_data']['other_vehicle_involved_index'] = other_vehicle_involved_options.index(other_vehicle_involved)
        elif case_type == 'Personal Injury':
            injury_type = st.text_input("Type of injury (e.g., slip and fall, dog bite)", value=st.session_state['form_data'].get('injury_type', ''))
            property_type_options = ["Public", "Private"]
            property_type = st.selectbox("Was the incident on public or private property?", property_type_options, index=st.session_state['form_data'].get('property_type_index', 0))
            st.session_state['form_data']['injury_type'] = injury_type
            st.session_state['form_data']['property_type'] = property_type
            st.session_state['form_data']['property_type_index'] = property_type_options.index(property_type)
        elif case_type == 'Medical Malpractice':
            malpractice_type = st.text_input("Type of malpractice (e.g., misdiagnosis, surgical error)", value=st.session_state['form_data'].get('malpractice_type', ''))
            consent_forms_options = ["Yes", "No"]
            consent_forms = st.selectbox("Did you sign any consent forms?", consent_forms_options, index=st.session_state['form_data'].get('consent_forms_index', 0))
            st.session_state['form_data']['malpractice_type'] = malpractice_type
            st.session_state['form_data']['consent_forms'] = consent_forms
            st.session_state['form_data']['consent_forms_index'] = consent_forms_options.index(consent_forms)
        elif case_type == 'Workplace Injury':
            on_the_clock_options = ["Yes", "No"]
            on_the_clock = st.selectbox("Were you on the clock when the injury occurred?", on_the_clock_options, index=st.session_state['form_data'].get('on_the_clock_index', 0))
            reported_to_employer_options = ["Yes", "No"]
            reported_to_employer = st.selectbox("Did you report the injury to your employer?", reported_to_employer_options, index=st.session_state['form_data'].get('reported_to_employer_index', 0))
            st.session_state['form_data']['on_the_clock'] = on_the_clock
            st.session_state['form_data']['on_the_clock_index'] = on_the_clock_options.index(on_the_clock)
            st.session_state['form_data']['reported_to_employer'] = reported_to_employer
            st.session_state['form_data']['reported_to_employer_index'] = reported_to_employer_options.index(reported_to_employer)
        elif case_type == 'Product Liability':
            product_type = st.text_input("Type of product involved", value=st.session_state['form_data'].get('product_type', ''))
            product_recall_options = ["Yes", "No"]
            product_recall = st.selectbox("Was there a recall on the product?", product_recall_options, index=st.session_state['form_data'].get('product_recall_index', 0))
            st.session_state['form_data']['product_type'] = product_type
            st.session_state['form_data']['product_recall'] = product_recall
            st.session_state['form_data']['product_recall_index'] = product_recall_options.index(product_recall)
        elif case_type == 'Other':
            other_case_type = st.text_input("Please specify the case type", value=st.session_state['form_data'].get('other_case_type', ''))
            other_details = st.text_area("Any additional details", value=st.session_state['form_data'].get('other_details', ''), max_chars=500)
            st.session_state['form_data']['other_case_type'] = other_case_type
            st.session_state['form_data']['other_details'] = other_details

        col1, col2 = st.columns(2)
        with col1:
            back = st.form_submit_button("Back", on_click=prev_step)
        with col2:
            next = st.form_submit_button("Next")

        if next:
            st.session_state['form_data']['detailed_description'] = detailed_description
            next_step()

def review_and_submit():
    st.header("Step 5: Review & Submit")
    form_data = st.session_state['form_data']

    st.subheader("Please review your information before submission:")

    st.write("**Full Name:**", form_data['full_name'])
    st.write("**Phone Number:**", form_data['phone_number'])
    st.write("**Email Address:**", form_data['email'])

    st.write("**Date of Incident:**", form_data['incident_date'])
    st.write("**Case Type:**", form_data['case_type'])
    st.write("**Short Description:**", form_data['incident_description'])

    st.write("**Medical Expenses:** $", form_data['medical_expenses'])
    st.write("**Future Medical Expenses:** $", form_data['future_medical_expenses'])
    st.write("**Lost Income:** $", form_data['lost_income'])
    st.write("**Future Lost Income:** $", form_data['future_lost_income'])
    st.write("**Property Damage:** $", form_data['property_damage'])
    st.write("**Pain and Suffering Multiplier:**", form_data['pain_suffering_multiplier'])

    st.write("**Detailed Description:**", form_data['detailed_description'])

    # Dynamic questions
    case_type = form_data['case_type']
    if case_type == 'Motor Vehicle Accident':
        st.write("**Were you the driver or passenger?:**", form_data['driver_or_passenger'])
        st.write("**Was another vehicle involved?:**", form_data['other_vehicle_involved'])
    elif case_type == 'Personal Injury':
        st.write("**Type of injury:**", form_data['injury_type'])
        st.write("**Was the incident on public or private property?:**", form_data['property_type'])
    elif case_type == 'Medical Malpractice':
        st.write("**Type of malpractice:**", form_data['malpractice_type'])
        st.write("**Did you sign any consent forms?:**", form_data['consent_forms'])
    elif case_type == 'Workplace Injury':
        st.write("**Were you on the clock when the injury occurred?:**", form_data['on_the_clock'])
        st.write("**Did you report the injury to your employer?:**", form_data['reported_to_employer'])
    elif case_type == 'Product Liability':
        st.write("**Type of product involved:**", form_data['product_type'])
        st.write("**Was there a recall on the product?:**", form_data['product_recall'])
    elif case_type == 'Other':
        st.write("**Specified case type:**", form_data['other_case_type'])
        st.write("**Additional details:**", form_data['other_details'])

    agree = st.checkbox('I agree to the Privacy Policy and Consent to Contact.')

    col1, col2, col3 = st.columns(3)
    with col1:
        back = st.button("Back", on_click=prev_step)
    with col2:
        submit = st.button("Submit")

    if submit and agree:
        # Generate the OpenAI prompt
        prompt = generate_prompt(form_data)

        # Call the OpenAI API
        try:
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
        except Exception as e:
            st.error(f"An error occurred: {e}")
    elif submit and not agree:
        st.warning("You must agree to the Privacy Policy and Consent to Contact before submitting.")

if __name__ == "__main__":
    main()
