from flask import Flask, render_template, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
app = Flask(__name__)

# ✅ SMTP configuration (use your Gmail + app password)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = os.getenv("SMTP_USER")       # <-- your Gmail (sender)
SMTP_PASS = os.getenv("SMTP_PASS")     # <-- your Gmail App Password
TO_EMAIL   = "goguldev28@gmail.com"      # <-- the recipient email

# ✅ Route to serve your HTML
@app.route("/")
def home():
    return render_template("index.html")

# ✅ Route to handle form submission
@app.route("/send-inquiry", methods=["POST"])
def send_inquiry():
    try:
        name = request.form.get("name")
        sender_email = request.form.get("email")
        phone = request.form.get("phone")
        product = request.form.get("product")
        quantity = request.form.get("quantity")

        # Create the email
        msg = MIMEMultipart()
        msg["From"] = SMTP_USER
        msg["To"] = TO_EMAIL
        msg["Subject"] = f"New Inquiry from {name}"
        msg.add_header('Reply-To', sender_email)

        # Email body
        body = f"""
        New Inquiry received from your website:

        Name: {name}
        Email: {sender_email}
        Phone: {phone}
        Product: {product}
        Quantity: {quantity}
        """

        msg.attach(MIMEText(body, "plain"))

        # Send email using Gmail SMTP
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)

        return jsonify({"success": True, "message": "✅ Inquiry sent successfully!"})
    except Exception as e:
        print("Error:", e)
        return jsonify({"success": False, "message": "❌ Failed to send inquiry."}), 500


if __name__ == "__main__":
    app.run(debug=True)
