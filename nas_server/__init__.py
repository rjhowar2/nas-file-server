from flask import Flask
import os

app = Flask(__name__)

app.config['allowed_filetypes'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp3', 'mp4'])
app.config['base_directory'] = "%s/%s" % (os.path.dirname(os.path.realpath("nas_server/")), "nas_server/tests/test_files_dir")

import nas_server.views