import ssl
import smtplib
from email.message import EmailMessage
import pyotp
import os
from flask import Flask, render_template, request, redirect, url_for, session
import data


app = Flask(__name__)
app.secret_key = os.urandom(24)

# Ustawienia użytkownika i poczty
EMAIL_PASSWORD = data.email_password  # Hasło aplikacji Gmail
EMAIL_SENDER = data.email_sender  # Nadawca e-maili
TOTP_SECRET_KEY = "CorrectCodeWroteBase"  # Klucz do generowania kodu TOTP
USER_CREDENTIALS = {data.email_recipient: "password"}  # Login i hasło użytkownika


def send_mail(code, recipient_email = data.email_recipient):
    """
    Wysyła e-mail z kodem 2FA na podany adres e-mail.
    """
    subject = "Your 2FA Code"
    body = f"CODE: {code}"

    em = EmailMessage()
    em['From'] = EMAIL_SENDER
    em['To'] = recipient_email
    em['Subject'] = subject
    em.set_content(body)

    context = ssl._create_unverified_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
        smtp.sendmail(EMAIL_SENDER, recipient_email, em.as_string())


@app.route('/')
def home():

    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():

    email = request.form['email']
    password = request.form['password']

    # Sprawdzanie poprawności loginu i hasła
    if email in USER_CREDENTIALS and USER_CREDENTIALS[email] == password:
        # Generowanie kodu TOTP
        totp = pyotp.TOTP(TOTP_SECRET_KEY, interval=120)#2min na wpisanie hasła
        two_fa_code = totp.now()

        # Wysyłanie kodu na e-mail
        send_mail(two_fa_code, email)

        # Zapisanie e-maila w sesji
        session['email'] = email

        return redirect(url_for('verify'))

    return 'Invalid credentials', 401


@app.route('/verify', methods=['GET', 'POST'])
def verify():

    if 'email' not in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        input_code = request.form['code']
        totp = pyotp.TOTP(TOTP_SECRET_KEY, interval=120)

        if totp.verify(input_code):
            return 'Successfully logged in!'
        else:
            return 'Incorrect 2FA code'

    return render_template('verify.html')


if __name__ == '__main__':
    app.run(debug=True)
