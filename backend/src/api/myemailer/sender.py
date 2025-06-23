from email.message import EmailMessage
import os
import smtplib
from dotenv import load_dotenv
load_dotenv() 

EMAIL_HOST=os.getenv("EMAIL_HOST")
EMAIL_ADDRESS=os.getenv("EMAIL_ADDRESS")

print(EMAIL_HOST,EMAIL_ADDRESS)

EMAIL_PASSWORD=os.getenv("EMAIL_PASSWORD")
EMAIL_PORT = int(os.getenv("EMAIL_PORT"))

def send_email(subject:str="No subject provided",content:str="No content provided",to_email:str=EMAIL_ADDRESS,from_email:str=EMAIL_ADDRESS):
    msg=EmailMessage()
    msg["Subject"]=subject
    msg["From"]=from_email
    msg["To"]=to_email
    msg.set_content(content)
    with smtplib.SMTP_SSL(EMAIL_HOST,EMAIL_PORT) as server:
        server.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
        server.send_message(msg)
    