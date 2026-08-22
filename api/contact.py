import json
import os
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from http.server import BaseHTTPRequestHandler


class handler(BaseHTTPRequestHandler):

  def do_POST(self):
    content_length = int(self.headers.get("Content-Length", 0))
    post_data = self.rfile.read(content_length)

    try:
      if not post_data:
        self._send_response(
            400, {"success": False, "message": "No data received."}
        )
        return

      data = json.loads(post_data.decode("utf-8"))
      name = data.get("name", "").strip()
      sender_email = data.get("email", "").strip()
      subject = data.get("subject", "").strip()
      message = data.get("message", "").strip()

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
                "message": "Missing EMAIL_USER or EMAIL_PASS in Vercel settings.",
            },
        )
        return

      smtp_pass = smtp_pass.replace(" ", "")

      # Create MIME email message
      msg = MIMEMultipart()
      msg["From"] = smtp_user
      msg["To"] = receiver
      msg["Subject"] = f"Portfolio Message: {subject}"
      msg["Reply-To"] = sender_email

      body = f"Name: {name}\nEmail: {sender_email}\nSubject: {subject}\n\nMessage:\n{message}"
      msg.attach(MIMEText(body, "plain", "utf-8"))

      # Send via Gmail SMTP SSL port 465
      context = ssl.create_default_context()
      with smtplib.SMTP_SSL(
          "smtp.gmail.com", 465, context=context, timeout=10
      ) as server:
        server.login(smtp_user, smtp_pass)
        server.sendmail(smtp_user, receiver, msg.as_string())

      self._send_response(
          200, {"success": True, "message": "Message sent successfully!"}
      )

    except smtplib.SMTPAuthenticationError:
      self._send_response(
          500,
          {
              "success": False,
              "message": (
                  "SMTP Authentication failed. Verify your 16-character Google"
                  " App Password."
              ),
          },
      )
    except Exception as e:
      self._send_response(
          500, {"success": False, "message": f"Server Error: {str(e)}"}
      )

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