from flask import url_for
from flask_mail import Message
from Login import mail
def send_reset_email(user2):
    token=user2.get_reset_token()
    msg=Message('Password Reset Request',sender='norepy_bs@demo.com',recipients=[user2.email])
    msg.body=f'''To reset your password, visit the following link:
{url_for('users.reset_token',token=token,_external=True)}

If you did not make this request then simply ignore and no changes will be made
'''

    mail.send(msg)