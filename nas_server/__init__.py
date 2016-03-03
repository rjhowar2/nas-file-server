from flask import Flask

app = Flask(__name__)

app.config['allowed_filetypes'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp3', 'mp4'])

import nas_server.views