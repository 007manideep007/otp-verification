# Project - OTP Verification App

import streamlit as st          # for frontend development
import smtplib                  # to send emails using SMTP
import random                   # for OTP generation
import os                       # accessing environment variables
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
                


# Accessing environment over here inside the code
load_dotenv()
EMAIL = os.getenv("EMAIL_USER")
PASSWORD = os.getenv("EMAIL_PASS")


st.title("Email OTP Verification  App")
# Intialize the OTP
if "otp" not in st.session_state:
    st.session_state.otp = None


with st.form("otp_form"):
    user_email = st.text_input("Enter your email address")
    send_clicked = st.form_submit_button("Send OTP")


    if send_clicked:
        if EMAIL is None or PASSWORD is None:
            st.error("Email OR Password is missing in ENV file")
        elif user_email == "":
            st.warning("Please enter some email ID")
        else:
            st.session_state.otp = random.randint(1000,9999)

            body = f"OTP for verification: {st.session_state.otp}"
            msg = MIMEMultipart()
            msg["form"] = EMAIL
            msg["to"] = user_email
            msg["Subject"] = "OTP to steal all your money"
            msg.attach(MIMEText(body,"plain"))

            try:
                server = smtplib.SMTP("Smtp.gmail.com",587)
                server.starttls()
                server.login(EMAIL,PASSWORD)
                server.send_message(msg)
                server.quit()

                st.success("OTP fired successfully")

            except:
                st.error("Authentication Fails OR Internet Issue")
if st.session_state.otp:
    entered_otp = st.text_input("Enter OTP you received in Gmail")
    if st.button("Verify OTP"):
        if int(entered_otp) == st.session_state.otp:
            st.success("OTP Match")
        else:
            st.error("Wrong OTP")