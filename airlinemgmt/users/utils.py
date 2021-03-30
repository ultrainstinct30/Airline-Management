from flask import url_for, current_app
from flask_mail import Message
from airlinemgmt import mail

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
        sender='noreply@demo.com',
        recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not request this, ignore.
'''
    mail.send(msg)