import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from FlaskPage import mail

def save_image(form_image):
	secret_hex = secrets.token_hex(8)
	#gives back two variables, file name and file extension.
	#only want extension
	_, file_ext = os.path.splitext(form_image.filename)
	image_name = secret_hex + file_ext
	image_path = os.path.join(current_app.root_path,'static/profile_pictures', image_name)
	
	#scale down image with Pillow's Image
	#set size to 125 by 125, then save image
	output_size = (125,125)
	i=Image.open(form_image)
	i.thumbnail(output_size)
	i.save(image_path)
	
	return image_name
	
def send_reset_email(user):
	token = user.get_reset_token()
	msg = Message('Password Reset Request', sender='TicketManagerPlusNU@gmail.com', recipients=[user.email])

	msg.body = f'''Click the following link within the next 30 minutes to reset your password.
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request, please ignore this email.'''
	mail.send(msg)