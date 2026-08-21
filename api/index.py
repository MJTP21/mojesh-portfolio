import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/api/contact", methods=["POST"])
def contact():
  try:
    data = request.get_json()
    if not data:
      return jsonify({"success": False, "message": "No data received."}), 400

    name = data.get("name")
    sender_email = data.get("email")
    subject = data.get("subject")
    message = data.get("message")

    if not all([name, sender_email, subject, message]):
      return (
          jsonify({"success": False, "message": "All fields are required."}),
          400,
      )

    # Server SMTP credentials from environment variables
    smtp_user = os.environ.get("EMAIL_USER")
    smtp_password = os.environ.get("EMAIL_PASS")
    smtp_receiver = os.environ.get("RECEIVER_EMAIL", smtp_user)

    if not smtp_user or not smtp_password:
      return (
          jsonify({
              "success": False,
              "message": "SMTP credentials are not configured.",
          }),
          500,
      )

    # Email message construction
    msg = MIMEMultipart()
    msg["From"] = smtp_user
    msg["To"] = smtp_receiver
    msg["Subject"] = f"Portfolio Message: {subject}"
    msg["Reply-To"] = sender_email

    email_body = f"""New Message from Portfolio Website:

Name: {name}
Email: {sender_email}
Subject: {subject}

Message:
{message}
"""
    msg.attach(MIMEText(email_body, "plain", "utf-8"))

    # Direct SMTP connection (Gmail)
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
      server.starttls()
      server.login(smtp_user, smtp_password)
      server.send_message(msg)

    return (
        jsonify({"success": True, "message": "Message sent successfully!"}),
        200,
    )

  except Exception as e:
    return (
        jsonify({
            "success": False,
            "message": f"SMTP delivery failed: {str(e)}",
        }),
        500,
    )


# For local testing
if __name__ == "__main__":
  app.run(port=5000, debug=True)