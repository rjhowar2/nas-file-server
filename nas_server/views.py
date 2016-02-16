from flask import Flask, jsonify, request, abort
import os

from nas_server import app
from nas_server.api_utils import get_directory_contents, rename_resource, delete_resource
from tests.test_utils import rebuild_test_tree, TEST_DIR

BASE_URI = '/nas_server/api/v1.0'

@app.route('%s/test_app' % BASE_URI, methods=['GET'])
def reset_test_files():
	rebuild_test_tree()
	return jsonify({'files': get_directory_contents(TEST_DIR)})

@app.route('%s/directory' % BASE_URI, methods=['GET'])
def directory_contents():

	path = request.args.get('path', None)

	if not path:
		abort(400)

	return jsonify({'files': get_directory_contents(path)})

@app.route('%s/files' % BASE_URI, methods=['PUT'])
def update_file():
	required_args = ['source', 'destination']
	
	if not request.json or not  all ([k in request.json for k in required_args]):
		abort(400)

	source = request.json['source']
	destination = request.json['destination']

	return jsonify(rename_resource(source, destination))

@app.route('%s/files' % BASE_URI, methods=['DELETE'])
def delete_file():
	path = request.args.get('path', None)

	if not path:
		abort(400)

	return jsonify(delete_resource(path))

"""
**************************** STILL NEED TO IMPLEMENT  ********************************
"""

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
