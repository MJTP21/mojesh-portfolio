import json
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from http.server import BaseHTTPRequestHandler


class handler(BaseHTTPRequestHandler):

  def do_POST(self):
    content_length = int(self.headers.get("Content-Length", 0))
    post_data = self.rfile.read(content_length)

    try:
      data = json.loads(post_data.decode("utf-8"))
      name = data.get("name")
      sender_email = data.get("email")
      subject = data.get("subject")
      message = data.get("message")

      if not all([name, sender_email, subject, message]):
        self._send_response(
            400, {"success": False, "message": "All fields are required."}
        )
        return

      smtp_user = os.environ.get("EMAIL_USER")
      smtp_pass = os.environ.get("EMAIL_PASS")
      receiver = os.environ.get("RECEIVER_EMAIL", smtp_user)

      if not smtp_user or not smtp_pass:
        self._send_response(
            500,
            {
                "success": False,
                "message": "Server email configuration is missing.",
            },
        )
        return

      smtp_pass = smtp_pass.replace(" ", "")

      msg = MIMEMultipart()
      msg["From"] = smtp_user
      msg["To"] = receiver
      msg["Subject"] = f"Portfolio Message: {subject}"
      msg["Reply-To"] = sender_email

      body = f"Name: {name}\nEmail: {sender_email}\nSubject: {subject}\n\nMessage:\n{message}"
      msg.attach(MIMEText(body, "plain", "utf-8"))

      with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)

      self._send_response(
          200, {"success": True, "message": "Message sent successfully!"}
      )

    except Exception as e:
      self._send_response(500, {"success": False, "message": str(e)})

  def _send_response(self, status_code, body):
    self.send_response(status_code)
    self.send_header("Content-Type", "application/json")
    self.send_header("Access-Control-Allow-Origin", "*")
    self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
    self.send_header("Access-Control-Allow-Headers", "Content-Type")
    self.end_headers()
    self.wfile.write(json.dumps(body).encode("utf-8"))

  def do_OPTIONS(self):
    self._send_response(200, {})