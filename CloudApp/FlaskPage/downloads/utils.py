import os
from flask import url_for, current_app
from werkzeug.utils import secure_filename


def save_custom_file(form_file):
	f= form_file.file.data
	filename = secure_filename(f.filename)
	f.save(os.path.join(current_app.root_path, 'static/file_folder', filename))
	return