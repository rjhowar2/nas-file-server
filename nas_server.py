from flask import Flask, jsonify, request, abort
import os

app = Flask(__name__)

def get_files_from_root(root):
	all_files = {}
	for path, subdirs, files in os.walk(root):
		all_files['path'] = path
		children = []

		def add_files(my_list, is_dir):
			for name in my_list:
				if not name.startswith("."):
					children.append({'is_dir': is_dir, 'filename': name})

		add_files(subdirs, True)
		add_files(files, False)

		sorted_children = sorted(children, key=lambda x: x['filename'].lower())

		all_files['children'] = sorted_children

		break

	return all_files

@app.route('/nas_server/api/v1.0/files', methods=['POST'])
def get_files():
	if not request.json or not 'root' in request.json:
		abort(400)

	root = request.json['root']

	return jsonify({'files': get_files_from_root(root)})

if __name__ == '__main__':
    app.run(debug=True, host="localhost")