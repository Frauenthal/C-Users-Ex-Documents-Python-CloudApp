from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from FlaskPage import db
from FlaskPage.models import Post, Ticket
from FlaskPage.posts.forms import PostForm

posts = Blueprint('posts', __name__)


#functions for creating a post
@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
	form = PostForm()
	
	if form.validate_on_submit():
		#create post object
		post = Post(title = form.title.data, content = form.content.data, author = current_user)
		
		#temp line to add ticket
		#post = Ticket(title = form.title.data, content = form.content.data, author = current_user)
		#add object to session

		db.session.add(post)
		#commit session changes to db [saves post to database]
		db.session.commit()
		flash('Post has been created.','success')
		return redirect(url_for('main.solutions'))

	return render_template('create_post.html', title='New Post', form = form, legend = 'Create New Post')


@posts.route("/post/<int:post_id>")
def post(post_id):
	#query SQL database for post by ID
	#get post if it exists, or return 404
	post = Post.query.get_or_404(post_id)
	return render_template('post.html', title=post.title, post=post)

@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
	#find post
	post = Post.query.get_or_404(post_id)
	
	#check if the author of the post is the current user
	if post.author != current_user:
		#if they are not the author abort
		abort(403)

	#Set form type as Post Form from forms.py [imported at top]
	form = PostForm()
	
	#if form is filled in correctly
	if form.validate_on_submit():
		#set title and content to form data
		post.title = form.title.data
		post.content = form.content.data
		#commit change | don't need to add to session because values already exist and are just being modified
		db.session.commit()
		flash('Post has been updated','success')
		return redirect(url_for('posts.post', post_id=post.id))
	
	#get data to prefil forms with current post information
	elif request.method =='GET':
		form.title.data = post.title
		form.content.data = post.content

	return render_template('create_post.html', title='Update Post', form = form, legend = 'Update Post')

@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
	#find post
	post = Post.query.get_or_404(post_id)
	
	#check if the author of the post is the current user
	if post.author != current_user:
		#if they are not the author abort
		abort(403)

	db.session.delete(post)
	db.session.commit()
	flash('Post has been deleted!','success')
	return redirect(url_for('main.solutions'))
