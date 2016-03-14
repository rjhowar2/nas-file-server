from flask import Flask, jsonify, request, abort, send_from_directory, make_response
import os
import json

from nas_server import app
from nas_server.api_utils import get_directory_contents, rename_resource, delete_resource, save_file, new_directory, ApiError, ApiSuccess
from tests.test_utils import rebuild_test_tree, TEST_DIR

BASE_URI = '/nas_server/api/v1.0'

@app.route('%s/test_app' % BASE_URI, methods=['GET'])
def reset_test_files():
	rebuild_test_tree()
	return jsonify({'files': get_directory_contents(TEST_DIR)})

@app.route('%s/directory/root' % BASE_URI, methods=['GET'])
def get_base_directory():
	return jsonify({'base_directory': app.config['base_directory']})

@app.route('%s/directory' % BASE_URI, methods=['GET'])
def directory_contents():

	path = request.args.get('path', "")

	return jsonify({'files': get_directory_contents(path)})

@app.route('%s/directory/create' % BASE_URI, methods=['POST'])
def create():
	folder = request.form.get('folder', "")
	name = request.form.get('name', None)

	if not name:
		abort(400)

	response = new_directory(folder, name)

	return jsonify(response)

@app.route('%s/files' % BASE_URI, methods=['PUT'])
def update():
	required_args = ['source', 'destination']
	
	if not request.json or not  all ([k in request.json for k in required_args]):
		abort(400)

	source = request.json['source']
	destination = request.json['destination']

	return jsonify(rename_resource(source, destination))

@app.route('%s/files/deletes' % BASE_URI, methods=['POST'])
def delete():
	folder = request.form.get('folder', "")
	filename = request.form.getlist('filename', None)

	if not all (filename):
		abort(400)

	response = delete_resource(folder, filename)

	return jsonify(response)

@app.route('%s/files' % BASE_URI, methods=['POST'])
def upload():
	folder = request.form.get("folder", "")
	file_body = request.files['file']
	
	if not file_body:
		return abort(400)

	response = save_file(folder, file_body)

	return jsonify(response)

@app.route('%s/files' % BASE_URI, methods=['GET'])
def download():
	dir_path = request.args.get('path', None)
	filename = request.args.get('filename', None)

	if not dir_path:
		abort(400)

	return send_from_directory(dir_path, filename)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify(ApiError("Not found")), 404)

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify(ApiError("Bad request")), 400)

@app.errorhandler(405)
def not_found(error):
    return make_response(jsonify(ApiError("Method not allowed")), 405)

