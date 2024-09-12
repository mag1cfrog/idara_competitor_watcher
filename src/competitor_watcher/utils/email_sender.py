import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

def send_email(subject, body, to_addr, from_addr, attachment=None):
    load_dotenv()
    password = os.getenv('gmail_sender_password')
    if not password:
        raise ValueError("EMAIL_PASSWORD environment variable is not set.")
    
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = subject

    # Add the email body to the message
    msg.attach(MIMEText(body, 'plain'))

    # Add an attachment to the email
    if attachment:
        from email.mime.base import MIMEBase
        from email import encoders

        part = MIMEBase('application', 'octet-stream')
        with open(attachment, 'rb') as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment)}')
        msg.attach(part)

    # Connect to the Gmail server
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()  # Initiate TLS encryption
        server.login(from_addr, password)  # Log in to the Gmail server
        server.send_message(msg)  # Send the email



if __name__ == '__main__':
    subject = 'Test Email'
    body = 'This is a test email sent by the email_sender module.'
    to_addr = 'mag1cfrogginger@gmail.com'  
    from_addr = 'harrywong2017@gmail.com'

    send_email(subject, body, to_addr, from_addr)
    print('Test email sent successfully!')