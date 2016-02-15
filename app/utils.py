import os

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