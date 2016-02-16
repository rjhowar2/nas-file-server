import os
import shutil

TEST_DIR = "%s/test_files_dir" % os.path.dirname(os.path.relpath(__file__))

def rebuild_test_tree():
	def _build_tree(file_tree, path):
		for node in file_tree:
			if node["is_dir"]:
				if path:
					new_path = "%s/%s" % (path, node["name"])
				else:
					new_path = node["name"]

				os.mkdir(new_path)
				_build_tree(node["children"], new_path)
			else:
				filepath = "%s/%s" % (path, node["name"])
				os.system('touch "%s"' % filepath)

	if os.path.exists(TEST_DIR):
		shutil.rmtree(TEST_DIR)
	os.mkdir(TEST_DIR)

	_build_tree(FILE_TREE_FULL, TEST_DIR)

def remove_test_tree():
	shutil.rmtree(TEST_DIR)

FILE_TREE_FULL = [	
	{
		"name": "folder 1",
		"is_dir": True,
		"children": [
			{
				"name": "folder1_file1.txt",
				"is_dir": False,
				"children": []
			},
			{
				"name": "folder1_file2.txt",
				"is_dir": False,
				"children": []
			},
			{
				"name": "folder1_file3.txt",
				"is_dir": False,
				"children": []
			}
		]
	},
	{
		"name": "folder 2",
		"is_dir": True,
		"children": [
			{
				"name": "folder2_sub1",
				"is_dir": True,
				"children": [
					{
						"name": "sub1_file1.txt",
						"is_dir": False,
						"children": []
					},
					{
						"name": "sub1_file2.txt",
						"is_dir": False,
						"children": []
					},
					{
						"name": "sub1_file3.txt",
						"is_dir": False,
						"children": []
					}
				]
			},
			{
				"name": "folder2_sub2",
				"is_dir": True,
				"children": [
					{
						"name": "folder2_sub2_sub1",
						"is_dir": True,
						"children": []
					}
				]
			},
		]
	},
	{
		"name": "folder 3",
		"is_dir": True,
		"children": []
	},
	{
		"name": "file1.txt",
		"is_dir": False,
		"children": []
	},
	{
		"name": "file2.txt",
		"is_dir": False,
		"children": []
	},
	{
		"name": "file3.txt",
		"is_dir": False,
		"children": []
	}
]