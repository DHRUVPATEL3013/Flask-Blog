import secrets
import os
from PIL import Image
from flask import url_for,current_app
from flaskblog import db,bcrypt,mail
from flask_mail import Message


def save_picture(form_picture):
    random_hex=secrets.token_hex(8)
    _,f_ext=os.path.splitext(form_picture.filename)
    picture_name=random_hex + f_ext
    picture_path=os.path.join(current_app.root_path,'static/profile_pics',picture_name)
    output_size=(125,125)
    i=Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_name

SENDER=os.getenv("MAIL_USERNAME")
def send_reset_email(user):
    token=user.get_reset_token()
    reset_url = url_for('users.reset_token', token=token, _external=True)
    msg=Message('Password Reset Request',sender=SENDER,recipients=[user.email])
    msg.body=f"""
    To reset your password,visit the following link: 
{reset_url}
if you did not make this request then simply ignore this email and no change will be made.
"""
    mail.send(msg)