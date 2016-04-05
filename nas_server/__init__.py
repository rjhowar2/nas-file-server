from flask import Flask
from config import *

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.debug=TEST_MODE

app.config['allowed_filetypes'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp3', 'mp4', 'py', 'html'])
app.config['SECRET_KEY'] = "No one ever really dies"
app.config['CLIENT_ID'] = CLIENT_ID
app.config['CLIENT_SECRET'] = CLIENT_SECRET

try:
	app.config['FILES_DIRECTORY'] = FILES_DIRECTORY
except NameError:
	app.config['FILES_DIRECTORY'] = os.path.join(BASE_DIR, "tests/test_files_dir")

import nas_server.views