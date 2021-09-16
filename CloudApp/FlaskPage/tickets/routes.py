from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from FlaskPage import db
from FlaskPage.models import Post, Ticket
from FlaskPage.tickets.forms import TicketForm

tickets = Blueprint('tickets', __name__)


#functions for creating a post
@tickets.route("/ticket/new", methods=['GET', 'POST'])
@login_required
def new_ticket():
	form = TicketForm()
	
	if form.validate_on_submit():
		#create ticket object
		ticket = Ticket(title = form.title.data, content = form.content.data, author = current_user, status= form.status.data)
		#add object to session
		if form.client_name.data != '':
			ticket.client_name = form.client_name.data

		if form.client_num.data != '':
			ticket.client_num = form.client_num.data

		if form.client_email.data != '':
			ticket.client_email = form.client_email.data

		db.session.add(ticket)
		#commit session changes to db [saves post to database]
		db.session.commit()
		flash('Ticket has been created.','success')
		return redirect(url_for('main.tickets'))

	return render_template('create_ticket.html', title='New Ticket', form = form, legend = 'Create New Ticket')


@tickets.route("/ticket/<int:ticket_id>")
def ticket(ticket_id):
	#query SQL database for post by ID
	#get post if it exists, or return 404
	ticket = Ticket.query.get_or_404(ticket_id)
	return render_template('ticket.html', title=ticket.title, ticket=ticket)

@tickets.route("/ticket/<int:ticket_id>/update", methods=['GET', 'POST'])
@login_required
def update_ticket(ticket_id):
	#find post
	ticket = Ticket.query.get_or_404(ticket_id)
	
	#check if the author of the post is the current user
	if ticket.author != current_user:
		#if they are not the author abort
		abort(403)

	#Set form type as Post Form from forms.py [imported at top]
	form = TicketForm()
	
	#if form is filled in correctly
	if form.validate_on_submit():
		#set title and content to form data
		ticket.title = form.title.data
		ticket.content = form.content.data
		ticket.status = form.status.data
		#commit change | don't need to add to session because values already exist and are just being modified
		if form.client_name.data != '':
			ticket.client_name = form.client_name.data

		if form.client_num.data != '':
			ticket.client_num = form.client_num.data

		if form.client_email.data != '':
			ticket.client_email = form.client_email.data

		db.session.commit()
		flash('ticket has been updated','success')
		return redirect(url_for('tickets.ticket', ticket_id=ticket.id))
	
	#get data to prefil forms with current post information
	elif request.method =='GET':
		form.title.data = ticket.title
		form.content.data = ticket.content

	return render_template('create_ticket.html', title='Update ticket', form = form, legend = 'Update ticket')

@tickets.route("/ticket/<int:ticket_id>/delete", methods=['POST'])
@login_required
def delete_ticket(ticket_id):
	#find post
	ticket = Ticket.query.get_or_404(ticket_id)
	
	#check if the author of the post is the current user
	if ticket.author != current_user:
		#if they are not the author abort
		abort(403)

	db.session.delete(ticket)
	db.session.commit()
	flash('Ticket has been deleted!','success')
	return redirect(url_for('main.tickets'))
