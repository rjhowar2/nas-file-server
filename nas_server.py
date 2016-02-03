from flask import Flask, jsonify, request, abort
import os

app = Flask(__name__)

def get_files_as_dict(root):
	all_files = []
	for path, subdirs, files in os.walk(root):
		for name in files:
			all_files.append(os.path.join(path, name))

	return all_files

@app.route('/nas_server/api/v1.0/files', methods=['POST'])
def get_files():
	if not request.json or not 'root' in request.json:
		abort(400)

	root = request.json['root']

	return jsonify({'files': get_files_as_dict(root)})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")