from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from FlaskPage.models import User

class RegistrationForm(FlaskForm):
	#email section requires data, validates is an email
	email = StringField('Email:',
                        validators=[DataRequired(), Email()])
	
	#username section requires date, must be between 5 and 20 characters
	username = StringField('Username:', validators=[DataRequired(),
		Length(min = 5,max = 20)])

	#password section requires date, must be between 5 and 20 characters
	password = PasswordField('Password:', validators=[DataRequired(),
		Length(min = 5,max = 20)])

	#username section requires date, must match input in password field
	confirm_password = PasswordField('Confirm Password:',
		validators=[DataRequired(), EqualTo('password')])

	#submit button
	submit = SubmitField('Register New User')

	#def validate_filed(self, field):
	#	if True:
	#		raise ValidationError('Validation Message')

	def validate_username(self, username):
		user = User.query.filter_by(username = username.data).first()

		if user:
			raise ValidationError('Username is already in use.')

	def validate_email(self, email):
		email = User.query.filter_by(email = email.data).first()

		if email:
			raise ValidationError('Email is already in use.')



class LoginForm(FlaskForm):
	
	#validate input is an email
	email = StringField('Email', validators=[DataRequired(),
		Email()])

	#password must be between 5 and 20 characters
	password = PasswordField('Password', validators=[DataRequired(),
		Length(min = 5,max = 20)])

	#remember me radial button
	remember = BooleanField('Stay Signed In')

	#submit button
	submit = SubmitField('Log in')


class UpdateAccountForm(FlaskForm):
	#email section requires data, validates is an email
	email = StringField('Email:',
                        validators=[DataRequired(), Email()])
	
	#username section requires date, must be between 5 and 20 characters
	username = StringField('Username:', validators=[DataRequired(),
		Length(min = 5,max = 20)])

	image = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])

	#password must be between 5 and 20 characters
	password = PasswordField('Confirm Current Password:', validators=[DataRequired(),
		Length(min = 5,max = 20)])


	#submit button
	submit = SubmitField('Update')

	#example to add differnet validation fields
	#def validate_filed(self, field):
	#	if True:
	#		raise ValidationError('Validation Message')

	def validate_username(self, username):
		if username.data != current_user.username:
			user = User.query.filter_by(username = username.data).first()

			if user:
				raise ValidationError('Username is already in use.')

	def validate_email(self, email):
		if email.data != current_user.email:
			email = User.query.filter_by(email = email.data).first()

			if email:
				raise ValidationError('Email is already in use.')

class RequestResetForm(FlaskForm):
	email = StringField('Email:',
                        validators=[DataRequired(), Email()])
	submit = SubmitField('Request Password Reset')

	def validate_email(self, email):
		email = User.query.filter_by(email = email.data).first()

		if email is None:
			raise ValidationError('Email is not associated with an account.')

class ResetPasswordForm(FlaskForm):
	#password section requires date, must be between 5 and 20 characters
	password = PasswordField('Password:', validators=[DataRequired(),
		Length(min = 5,max = 20)])

	#username section requires date, must match input in password field
	confirm_password = PasswordField('Confirm Password:',
		validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Set Password')