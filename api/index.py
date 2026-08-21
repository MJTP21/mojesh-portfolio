import os
import smtplib
from email.message import EmailMessage

from flask import Flask, request, jsonify
from flask_cors import CORS


app = Flask(__name__)

# Allow requests from your portfolio website
CORS(app)


@app.route("/", methods=["POST"])
def contact():

    try:
        # Get JSON data from frontend
        data = request.get_json(silent=True)

        if not data:
            return jsonify({
                "success": False,
                "message": "No data received."
            }), 400

        # Get form values
        name = str(data.get("name", "")).strip()
        email = str(data.get("email", "")).strip()
        subject = str(data.get("subject", "")).strip()
        message = str(data.get("message", "")).strip()

        # Validate form
        if not name or not email or not subject or not message:
            return jsonify({
                "success": False,
                "message": "Please fill in all fields."
            }), 400

        # Get Gmail credentials from Vercel Environment Variables
        gmail_user = os.environ.get("GMAIL_USER")
        gmail_password = os.environ.get("GMAIL_APP_PASSWORD")

        if not gmail_user or not gmail_password:
            print("ERROR: Gmail environment variables are missing.")

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

            server.ehlo()

            server.starttls()

            server.ehlo()

            server.login(
                gmail_user,
                gmail_password
            )

            server.send_message(email_message)

        print("Email sent successfully.")

        return jsonify({
            "success": True,
            "message": "Message sent successfully!"
        }), 200

    except smtplib.SMTPAuthenticationError:

        print("ERROR: Gmail authentication failed.")

        return jsonify({
            "success": False,
            "message": "Gmail authentication failed. Check your App Password."
        }), 500

    except Exception as error:

        print("EMAIL ERROR:", str(error))

        return jsonify({
            "success": False,
            "message": "Unable to send message."
        }), 500


# Optional GET route for testing
@app.route("/", methods=["GET"])
def test():

    return jsonify({
        "success": True,
        "message": "Portfolio contact API is working."
    }), 200
