import os
import json
import smtplib
from email.message import EmailMessage


def handler(request):
    # Only allow POST requests
    if request.method != "POST":
        return {
            "statusCode": 405,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "success": False,
                "message": "Method not allowed"
            })
        }

    try:
        # Get JSON data from frontend
        data = request.get_json()

        name = data.get("name", "").strip()
        email = data.get("email", "").strip()
        subject = data.get("subject", "").strip()
        message = data.get("message", "").strip()

        # Check required fields
        if not name or not email or not subject or not message:
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({
                    "success": False,
                    "message": "Please fill in all fields."
                })
            }

        # Get Gmail credentials from Vercel Environment Variables
        gmail_user = os.environ.get("GMAIL_USER")
        gmail_password = os.environ.get("GMAIL_APP_PASSWORD")

        if not gmail_user or not gmail_password:
            return {
                "statusCode": 500,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({
                    "success": False,
                    "message": "Email configuration is missing."
                })
            }

        # Create email
        email_message = EmailMessage()

        email_message["From"] = gmail_user
        email_message["To"] = gmail_user
        email_message["Reply-To"] = email
        email_message["Subject"] = f"Portfolio Contact: {subject}"

        email_message.set_content(
            f"""
New message from your portfolio website.

Name:
{name}

Email:
{email}

Subject:
{subject}

Message:
{message}
"""
        )

        # Connect to Gmail SMTP
        with smtplib.SMTP("smtp.gmail.com", 587) as server:

            server.starttls()

            server.login(
                gmail_user,
                gmail_password
            )

            server.send_message(
                email_message
            )

        # Successful response
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "success": True,
                "message": "Message sent successfully!"
            })
        }

    except Exception as error:

        print("Email error:", str(error))

        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "success": False,
                "message": "Unable to send message."
            })
        }