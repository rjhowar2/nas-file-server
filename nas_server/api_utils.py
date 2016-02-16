import os
import shutil

from tests.test_utils import TEST_DIR, rebuild_test_tree

def api_error(message,code=None):
	response = {
		"error": {
			"messgae": message,
			"code": code
		}
	}
	return response

def api_success(action, path):
	response = {
		"action": action,
		"path": path
	}
	return response

def get_directory_contents(dir_path):

	all_files = {}
	for path, subdirs, files in os.walk(dir_path):
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

def delete_resource(path):
	try:
		if os.path.isdir(path):
			shutil.rmtree(path)
		else:
			os.remove(path)

		response = api_success("delete", path)

	except Exception, e:
		response = api_error(str(e))

	return response

