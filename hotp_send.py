import time
import pyotp
import ssl
import smtplib
from email.message import EmailMessage
import dane

def send_mail(code, numer):
    email_sender = dane.email_sender
    email_password = dane.email_password
    email_recipient = dane.email_recipient

    subject = "Your 2FA Code " + str(numer+1)
    body = "CODE:"+str(code)

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_recipient
    em['Subject'] = subject
    em.set_content(body)

    context = ssl._create_unverified_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_recipient, em.as_string())


counter = 0
key = "CorrectCodeWroteBase"

hotp = pyotp.HOTP(key)


for i in range (5):
    print (f"wysyłanie {i+1} maila")
    send_mail(hotp.at(i), i)
for i in range (5):
    email_code = input(f"Jaki jest {i+1} wyslany kod: ")
    #print(hotp.at(i))

hotp.verify()
    


