from flask import Flask
from config import CLIENT_ID, CLIENT_SECRET

app = Flask(__name__)

app.config['allowed_filetypes'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp3', 'mp4', 'py', 'html'])
app.config['SECRET_KEY'] = "No one ever really dies"
app.config['CLIENT_ID'] = CLIENT_ID
app.config['CLIENT_SECRET'] = CLIENT_SECRET

import nas_server.views