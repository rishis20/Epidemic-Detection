from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import base64

scopes = ['https://www.googleapis.com/auth/gmail.compose', "https://www.googleapis.com/auth/gmail.readonly"]


def get_token():
    creds = None

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', scopes)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', scopes)
            creds = flow.run_local_server(port=8080)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds


def create_message(recipient: str):
    mail = MIMEMultipart()

    with (
        open("./templates/email.html", "r", encoding="utf-8") as f,
        # open("./templates/emailplain.html", "r", encoding="utf-8") as f,
        # open("./static/ConTag Logo Black and Green lowlowres.png", "rb") as g,
        # open("./static/contag logo.gif", "rb") as g
        open("./static/contag logo with bg.png", "rb") as g,
    ):
        mail.attach(MIMEText(f.read(), _subtype="html"))
        image = MIMEImage(g.read())

    image.add_header("Content-ID", "<logo>")
    mail.attach(image)

    mail["from"] = "vinkami.krip@gmail.com"
    mail["to"] = recipient
    mail["subject"] = "ConTag 🦠 Outbreak Alert!"

    message = {
        'raw': base64.urlsafe_b64encode(mail.as_bytes()).decode()
    }
    return message


if __name__ == '__main__':
    # ---- CREDENTIALS ---- #
    print("Getting credentials")
    creds = get_token()
    service = build('gmail', 'v1', credentials=creds)
    print("Got credentials")

    # ---- MAILING LIST ---- #
    print("Getting mailing list")
    if os.path.exists("list.txt"):
        with open("list.txt", "r") as f:
            mailing_list = f.read().splitlines()
    else:
        print("Mailing list not found. Quitting")
        quit()
    print("Got mailing list")

    # ---- SENDING ---- #
    print(f"Emails will be sent now. Total: {len(mailing_list)} emails")
    for i, mail_addr in enumerate(mailing_list):
        print(f"Sent email to {mail_addr} ({i + 1}/{len(mailing_list)})")
        try:
            message = create_message(mail_addr)
            service.users().messages().send(userId="me", body=message).execute()
        except HttpError as error:
            print(f'An error occurred: {error}')
