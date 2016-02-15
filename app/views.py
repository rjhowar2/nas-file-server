from flask import Flask, jsonify, request, abort
from utils import get_directory_contents

app = Flask(__name__)

BASE_URI = '/nas_server/api/v1.0'

@app.route('%s/directory' % BASE_URI, methods=['GET'])
def directory_contents():

	path = request.args.get('path', None)

	if not path:
		abort(400)

	return jsonify({'files': get_directory_contents(path)})

@app.route('%s/files' % BASE_URI, methods=['GET'])
def download_file():
	path = request.args.get('path', None)

	if not path:
		abort(400)

	return "Requested to download the following: %s" % path

@app.route('%s/files' % BASE_URI, methods=['POST'])
def upload_file():
	required_args = ['filename','directory_path']
	
	if not request.json or not  all ([k in request.json for k in required_args]):
		abort(400)

	filename = request.json['filename']
	dir_path = request.json['directory_path']

	return "Request to upload %s to %s" % (filename, dir_path)

@app.route('%s/files' % BASE_URI, methods=['PUT'])
def update_file():
	required_args = ['source', 'destination']
	
	if not request.json or not  all ([k in request.json for k in required_args]):
		abort(400)

	source = request.json['source']
	destination = request.json['destination']

	return "Request to rename %s to %s" % (source, destination)

@app.route('%s/files' % BASE_URI, methods=['DELETE'])
def delete_file():
	path = request.args.get('path', None)

	if not path:
		abort(400)

	return "Requested to delete the following: %s" % path


if __name__ == '__main__':
    app.run(debug=True, host="localhost")