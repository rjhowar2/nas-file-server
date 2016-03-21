import os
import shutil
import zipfile
from io import BytesIO
from werkzeug import secure_filename
from flask import send_from_directory, send_file

from nas_server import app
from tests.test_utils import TEST_DIR, rebuild_test_tree

def api_error(message,code=None):
    response = {
        "error": {
            "message": message,
            "code": code
        }
    }
    return response

class ApiError(dict):
    def __init__(self, message, code=None):
        self["error"] = {
            "message": message,
            "code": code
        }

class ApiSuccess(dict):
    def __init__(self, action, path):
        self["action"] = action
        self["path"] = path

def api_success(action, path):
    response = {
        "action": action,
        "path": path
    }
    return response

def get_directory_contents(folder):

    dir_path = get_full_path(folder)

    all_files = {}
    for path, subdirs, files in os.walk(dir_path):
        all_files['parent'] = folder
        children = []

        def add_files(my_list, is_dir):
            for name in my_list:
                if not name.startswith("."):
                    children.append({'is_dir': is_dir, 'filename': name, 'path': os.path.join(folder, name)})

        add_files(subdirs, True)
        add_files(files, False)

        sorted_children = sorted(children, key=lambda x: x['filename'].lower())

        all_files['children'] = sorted_children

        # os.walk will traverse all sub dirs as well so break after the first pass
        break

    return all_files

def rename_resource(source, destination):
    try:
        os.rename(source, destination)
        response = api_success("update", destination)
    except:
        response = api_error("Could not update source")

    return response

def delete_resource(folder, filename):
    dir_path = get_full_path(folder)

    try:
        for f in filename:
            fullpath = os.path.join(dir_path, f)
            _delete(fullpath)
        response = ApiSuccess("Files successfully removed", folder)
    except Exception, e:
        response = ApiError(str(e))

    return response

def _delete(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    else:
        os.remove(path)

def save_file(folder, file_obj):
    filename = file_obj.filename
    file_length = file_obj.content_length

    if not _valid_file(filename):
        response = ApiError("%s is not a supported file type" % filename)

    elif not _enough_space(file_length):
        response = ApiError("Not enough storage available for file %s" % filename)

    else:
        try:
            fullpath = os.path.join(get_full_path(folder), secure_filename(filename))
            file_obj.save(fullpath, )
            response = ApiSuccess("File successfully uploaded", os.path.join(folder,filename))
        except Exception, e:
            response = ApiError(str(e))

    return response

def new_directory(folder, name):
    try:
        fullpath = os.path.join(get_full_path(folder), name)
        os.mkdir(fullpath)
        response = ApiSuccess("New folder created", os.path.join(folder,name))
    except Exception, e:
        response = ApiError(str(e))
    
    return response

def download_files(folder, files):
    base_dir = get_full_path(folder)
    if len(files) == 1 and not os.path.isdir(os.path.join(base_dir, files[0])):
        response = send_from_directory(base_dir, files[0])
    else:
        memory_file = BytesIO()
        zf = zipfile.ZipFile(memory_file, "w")

        for filename in files:
            zf.write(os.path.join(base_dir, filename), filename)
        zf.close()
        memory_file.seek(0)
        response = send_file(memory_file, attachment_filename='download.zip', as_attachment=True)

    return response


def _valid_file(filename):
    return filename.split(".")[1] in app.config["allowed_filetypes"]

def _enough_space(file_length):
    return True

def get_full_path(folder=""):
    return os.path.join(app.config['base_directory'], folder)

