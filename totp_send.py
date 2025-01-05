import ssl
import smtplib
from email.message import EmailMessage
import pyotp
import dane

def send_mail(code):
    email_sender = dane.email_sender
    email_password = dane.email_password
    email_recipient = dane.email_recipient

    subject = "Your 2FA Code"
    body = "CODE: "+ str(code)

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_recipient
    em['Subject'] = subject
    em.set_content(body)

    context = ssl._create_unverified_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_recipient, em.as_string())

interval = 60 #Co ile zmienia sie kod (default = 30sek)
key = "CorrectCodeWroteBase"
totp = pyotp.TOTP(key, interval=interval)

two_fa_code = totp.now()

send_mail(two_fa_code)

input_code = input("Podaj kod 2FA: ")
if totp.verify(input_code):
    print("Right code", totp.now())
else:
    print("False", totp.now())
