from itsdangerous import URLSafeSerializer, BadSignature
from marketplace import app, mail, celery
from flask import url_for, render_template
from flask_mail import Message
from datetime import datetime, timedelta


def generate_confirmation_token(payload):
    serializer = URLSafeSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(payload, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token):
    serializer = URLSafeSerializer(app.config['SECRET_KEY'])
    try:
        payload = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT']
        )
    except BadSignature:
        return None
    return payload


@celery.task()
def _send_email(to, template, subject):
    msg = Message(
        subject=subject,
        recipients=[to],
        html=template,
        sender='customers@xtramarket.ru'
    )
    mail.connect()
    mail.send(msg)


def send_confirmation_email(user_email, contact):
    token = generate_confirmation_token(user_email)
    subject = 'MARKETPLACE. Подтверждение электронной почты'
    confirm_url = url_for('.email_confirm', token=token, _external=True)
    data = datetime.now().strftime("%d.%m.%y")
    html = render_template('email_confirm.html', confirm_url=confirm_url, contact=contact, data=data)
    _send_email.delay(user_email, html, subject)


def send_password_recovery_email(user_email):
    expires_on = datetime.utcnow()+timedelta(seconds=app.config['RECOVERY_PASSWORD_URL_EXPIRES'])
    payload = {'email': user_email, 'expires': expires_on.timestamp()}
    token = generate_confirmation_token(payload)
    subject = 'MARKETPLACE. Восстановление пароля'
    confirm_url = url_for('.password_recovery', token=token, _external=True)
    html = render_template('email_recovery_password.html', confirm_url=confirm_url)
    # _send_email.delay(user_email, html, subject)
