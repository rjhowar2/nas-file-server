from flask import Flask

app = Flask(__name__)

app.config['allowed_filetypes'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp3', 'mp4', 'py', 'html'])
app.config['SECRET_KEY'] = "No one ever really dies"
app.config['CLIENT_ID'] = "5bbdf80b-97b6-4f13-adeb-666f1643679e"
app.config['CLIENT_SECRET'] = "a?6Znfk~u5J]wkS!"

import nas_server.views