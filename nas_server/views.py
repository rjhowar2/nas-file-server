import json
from functools import wraps
from flask import Flask, jsonify, request, abort, make_response
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

from nas_server import app
from nas_server.api_utils import (get_directory_contents, rename_resource, delete_resource, save_file, 
	new_directory, download_files, ApiError, ApiSuccess)
from tests.test_utils import rebuild_test_tree, TEST_DIR

BASE_URI = '/nas_server/api/v1.0'

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not _check_auth(auth.username):
        	abort(401)
        return f(*args, **kwargs)
    return decorated

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
	
	if not request.json or not all ([k in request.json for k in required_args]):
		abort(400)

	source = request.json['source']
	destination = request.json['destination']
	folder = request.json.get('folder', '');

	return jsonify(rename_resource(folder, source, destination))

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

@app.route('%s/files/downloads' % BASE_URI, methods=['POST'])
def download():
	dir_path = request.form.get('folder', "")
	filename = request.form.getlist('filename', None)

	if not filename:
		abort(400)

	return download_files(dir_path, filename)

@app.route('%s/token' % BASE_URI, methods=['GET'])
def auth_token():
	auth = request.authorization

	if not auth or not (auth.username == app.config['CLIENT_ID'] and auth.password == app.config['CLIENT_SECRET']):
		abort(401)

	return jsonify({'token': _generate_auth_token(auth.username)})

def _generate_auth_token(user_id, expiration=600):
	s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
	return s.dumps(user_id)

def _check_auth(token):
	s = Serializer(app.config['SECRET_KEY'])
	try:
		data = s.loads(token)
	except SignatureExpired:
		return None    # valid token, but expired
	except BadSignature:
		return None    # invalid token
	return True

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify(ApiError("Not found", code=404)), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify(ApiError("Bad request", code=400)), 400)

@app.errorhandler(405)
def method_not_allowed(error):
    return make_response(jsonify(ApiError("Method not allowed", code=405)), 405)

