from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired


class TicketForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired()])
	content = TextAreaField('Content', validators=[DataRequired()])
	status = SelectField('status', choices = ["Open","Waiting On Client","Waiting On Product","On Hold","Closed",])
	client_name = StringField('Client Name (optional)')
	client_num = StringField('Client Phone Number (optional)')
	client_email = StringField('Client Email (optional)')
	submit = SubmitField('Submit')