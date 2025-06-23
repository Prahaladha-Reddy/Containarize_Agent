import os
from gmail_imap_parser import GmailImapParser
from dotenv import load_dotenv
load_dotenv()

def read_inbox(hours_ago=24,unread_only=True):
    parser = GmailImapParser(
    email_address=os.environ["EMAIL_ADDRESS"],
    app_password=os.environ["EMAIL_PASSWORD"]
    )
    emails = parser.fetch_emails(hours=hours_ago, unread_only=unread_only)
    for email in emails:
        print(f"From: {email['from']}")
        print(f"Subject: {email['subject']}")
        print(f"Date: {email['timestamp']}")
        print("---")
    return emails