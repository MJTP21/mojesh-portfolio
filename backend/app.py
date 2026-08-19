from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import smtplib
import os
from email.message import EmailMessage


# =====================================================
# LOAD ENVIRONMENT VARIABLES
# =====================================================

load_dotenv()


# =====================================================
# FLASK APP
# =====================================================

app = Flask(__name__)

CORS(app)


# =====================================================
# GMAIL SETTINGS
# =====================================================

GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")

GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")


# =====================================================
# HOME / TEST ROUTE
# =====================================================

@app.route("/")
def home():

    return jsonify({
        "status": "success",
        "message": "Mojesh Tripura Portfolio Backend is running!"
    })


# =====================================================
# CONTACT FORM
# =====================================================

@app.route("/send-message", methods=["POST"])
def send_message():

    try:

        # -------------------------------------------------
        # GET DATA FROM FORM
        # -------------------------------------------------

        data = request.get_json()

        if not data:

            return jsonify({
                "status": "error",
                "message": "No data received."
            }), 400


        name = data.get("name", "").strip()

        email = data.get("email", "").strip()

        subject = data.get("subject", "").strip()

        message = data.get("message", "").strip()


        # -------------------------------------------------
        # VALIDATION
        # -------------------------------------------------

        if not name:

            return jsonify({
                "status": "error",
                "message": "Please enter your name."
            }), 400


        if not email:

            return jsonify({
                "status": "error",
                "message": "Please enter your email."
            }), 400


        if not subject:

            return jsonify({
                "status": "error",
                "message": "Please enter a subject."
            }), 400


        if not message:

            return jsonify({
                "status": "error",
                "message": "Please enter your message."
            }), 400


        # -------------------------------------------------
        # CREATE EMAIL
        # -------------------------------------------------

        email_message = EmailMessage()


        email_message["Subject"] = (
            f"Portfolio Contact: {subject}"
        )


        email_message["From"] = GMAIL_ADDRESS


        email_message["To"] = GMAIL_ADDRESS


        email_message["Reply-To"] = email


        email_message.set_content(

            f"""
You have received a new message from your portfolio website.

----------------------------------------

Name:
{name}

Email:
{email}

Subject:
{subject}

Message:
{message}

----------------------------------------

This message was sent from your portfolio contact form.
"""
        )


        # -------------------------------------------------
        # CONNECT TO GMAIL SMTP
        # -------------------------------------------------

        with smtplib.SMTP(
            "smtp.gmail.com",
            587
        ) as smtp:


            smtp.ehlo()


            smtp.starttls()


            smtp.ehlo()


            smtp.login(
                GMAIL_ADDRESS,
                GMAIL_APP_PASSWORD
            )


            smtp.send_message(
                email_message
            )


        # -------------------------------------------------
        # SUCCESS RESPONSE
        # -------------------------------------------------

        return jsonify({

            "status": "success",

            "message":
                "Your message has been sent successfully!"

        }), 200


    except Exception as error:

        print(
            "EMAIL ERROR:",
            error
        )


        return jsonify({

            "status": "error",

            "message":
                "Unable to send message. Please try again later."

        }), 500


# =====================================================
# RUN SERVER
# =====================================================

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )


    app.run(

        host="0.0.0.0",

        port=port,

        debug=True

    )