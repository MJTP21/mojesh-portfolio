import os
import smtplib
from email.message import EmailMessage

from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/api/contact", methods=["POST"])
def contact():

    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "message": "No data received."
            }), 400

        name = data.get("name", "").strip()
        email = data.get("email", "").strip()
        subject = data.get("subject", "").strip()
        message = data.get("message", "").strip()

        if not name or not email or not subject or not message:
            return jsonify({
                "success": False,
                "message": "Please fill in all fields."
            }), 400

        # Get Gmail details from Vercel Environment Variables
        gmail_user = os.environ.get("GMAIL_USER")
        gmail_password = os.environ.get("GMAIL_APP_PASSWORD")

        if not gmail_user or not gmail_password:

            print("Gmail environment variables are missing.")

            return jsonify({
                "success": False,
                "message": "Email configuration is missing."
            }), 500

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

        print("Email sent successfully.")

        return jsonify({
            "success": True,
            "message": "Message sent successfully!"
        }), 200

except Exception as error:

    error_message = str(error)

    print("Email error:", error_message)

    return jsonify({
        "success": False,
        "message": f"Email error: {error_message}"
    }), 500