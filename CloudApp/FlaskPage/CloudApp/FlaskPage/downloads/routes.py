from flask import render_template, Blueprint, redirect, flash, url_for, current_app,send_file
from FlaskPage.downloads.forms import UploadForm
from flask_login import login_required
from FlaskPage.downloads.utils import save_custom_file
import os


downloads = Blueprint('downloads', __name__)



@downloads.route("/upload", methods=['GET', 'POST'])
#login_required rerouted destination is set in __init__.py
@login_required
def upload():
	form = UploadForm()
	if form.validate_on_submit():
		save_custom_file(form)
		flash(f'File successfully uploaded!', 'success')
		return redirect(url_for('main.downloads'))


	#display about.html page
	return render_template('upload.html', title ='Upload A File', form = form)

#download_file
@downloads.route("/download/<path:filename>", methods=['GET', 'POST'])
@login_required
def download_file(filename):
	file_path='static/file_folder/' + filename
	return send_file(file_path, as_attachment=True)


@downloads.route("/delete")
#login_required rerouted destination is set in __init__.py
@login_required
def delete():
	#get list of files in directory
	files=(os.listdir(os.path.join(current_app.root_path, 'static/file_folder')))
	#display delete_file.html page
	return render_template('delete.html', title ='Downloads', files=files)

#delete selected file
@downloads.route("/delete_file/<path:filename>", methods=['GET', 'POST'])
@login_required
def delete_file(filename):
	file_path=os.path.join(current_app.root_path, 'static/file_folder', filename)
	flashmesage = "File Deleted : " + filename
	flash(flashmesage, 'danger')

	os.remove(file_path)
	return redirect(url_for('main.downloads'))

#files=(os.listdir(os.path.join(current_app.root_path, 'static/file_folder')))