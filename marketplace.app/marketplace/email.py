from itsdangerous import URLSafeSerializer, BadSignature
from marketplace import app, mail
from flask import url_for, render_template
from flask_mail import Message


def generate_confirmation_token(user_email):
    serializer = URLSafeSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(user_email, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token):
    serializer = URLSafeSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT']
        )
    except BadSignature:
        return None
    return email


def _send_email(to, template, subject):
    msg = Message(
        subject=subject,
        recepient=[to],
        html=template
    )
    mail.send(msg)


def send_confirmation_email(user_email):
    token = generate_confirmation_token(user_email)
    subject = 'MARKETPLACE. Подтверждение электронной почты'
    confirm_url = url_for('.email_confirm', token=token, _external=True)
    html = render_template('email_confirm.html', confirm_url=confirm_url)
    print(confirm_url)
    # _send_email(user_email, html, subject)
