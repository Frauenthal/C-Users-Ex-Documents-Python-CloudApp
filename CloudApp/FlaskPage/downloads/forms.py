from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_wtf.file import FileField, FileRequired


class UploadForm(FlaskForm):
	file = FileField('Choose file to upload',validators=[FileRequired()])

	#submit button
	submit = SubmitField('Upload' )