import smtplib
from email.mime.text import MIMEText

sender = 'freelancey64@gmail.com'
receiver = 'storydemoi1@gmail.com'
app_password = 'jcut rimn bcjy yimn'  # Not your Gmail password!

msg = MIMEText("This is the body of the email")
msg['Subject'] = 'Test Email'
msg['From'] = sender
msg['To'] = receiver

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
    server.login(sender, app_password)
    server.send_message(msg)
