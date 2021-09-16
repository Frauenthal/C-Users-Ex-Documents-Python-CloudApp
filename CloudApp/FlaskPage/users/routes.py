from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from FlaskPage import db, bcrypt
from FlaskPage.models import User, Post, Ticket
from FlaskPage.users.forms import RegistrationForm, LoginForm, UpdateAccountForm,RequestResetForm, ResetPasswordForm
from FlaskPage.users.utils import save_image, send_reset_email

users = Blueprint('users', __name__)


#functions for login.html. Recieve GET and POST requests required for login.
@users.route("/register", methods=['GET','POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))

	#recieve RegistrationForm from forms.py
	form = RegistrationForm()
    
	#if form is filled our correctly
	if form.validate_on_submit():
		#encrypt text in password filed and save as hashed_password .decode sets it as string instead of bits
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

		#create user object with supplied information from form
		user = User(username = form.username.data, email = form.email.data, password = hashed_password)

		#add user to db session
		db.session.add(user)
    	#save user to db
		db.session.commit()

    	#redirect user to home page and display account created message.
		flash(f'Account created for {form.username.data}!', 'success')
		return redirect(url_for('main.home'))

	return render_template('register.html', title='Register', form=form)

#functions for login.html. Recieve GET and POST requests required for login.
@users.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))

	#recieve LoginForm from forms.py
	form = LoginForm()
	
	#if form is filled our correctly
	if form.validate_on_submit():
		#grab info from db using email from form
		user = User.query.filter_by(email=form.email.data).first()
		
		#if username is correct and password is correct for that user
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			#login and check if they want to remember login status
			login_user(user, remember=form.remember.data)
			
			#if user send to login from other page save foward address
			forward_to = request.args.get('next')
			
			#if forward address exists, redirect to forward
			if forward_to:
				return redirect(forward_to)
			#else send home
			else:
				return redirect(url_for('main.home'))
		
		else:
			flash(f'Login Failed. Please check email and password.', 'danger')

	#display html page
	return render_template('login.html', title='Login', form = form)



#functions to log users out
@users.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('users.login'))

@users.route("/account", methods=['GET', 'POST'])
#check if user is logged in, if not redirect to login page
#login_required rerouted destination is set in __init__.py
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit() and bcrypt.check_password_hash(current_user.password, form.password.data):
		
		if form.image.data:
			picture_file = save_image(form.image.data)
			current_user.image_file = picture_file

		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('Account information updated.', 'success')
		return redirect(url_for('users.account'))

	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email

	elif bcrypt.check_password_hash(current_user.password, form.password.data) == False:
			flash('Invalid Password', 'danger')

	image_file = url_for('static', filename='profile_pictures/' + current_user.image_file)
	return render_template('account.html', title='Account', image_file= image_file, form = form)


@users.route("/user/<string:username>")
#login_required rerouted destination is set in __init__.py
@login_required
def user_posts(username):
	#set page value to use in sql query for paginate
	page = request.args.get('page', 1, type=int)
	user= User.query.filter_by(username=username).first_or_404()
	#uses paginate to set 5 posts per page
	#order_by orders posts by most recent first
	posts = Post.query.filter_by(author=user)\
	.order_by(Post.date_posted.desc())\
	.paginate(page=page, per_page=5)
	#display solutions.html page
	return render_template('user_posts.html', title='Solutions', posts=posts, user=user)

@users.route("/user/tickets/<string:username>")
#login_required rerouted destination is set in __init__.py
@login_required
def user_tickets(username):
	#set page value to use in sql query for paginate
	page = request.args.get('page', 1, type=int)
	user= User.query.filter_by(username=username).first_or_404()
	#uses paginate to set 5 posts per page
	#order_by orders posts by most recent first
	tickets = Ticket.query.filter_by(author=user)\
	.order_by(Ticket.date_posted.desc())\
	.paginate(page=page, per_page=5)
	#display solutions.html page
	return render_template('user_tickets.html', title='Tickets', tickets=tickets, user=user)

@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)