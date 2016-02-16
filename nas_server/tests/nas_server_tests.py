import unittest
from test_utils import make_test_tree, rebuild_test_tree, TEST_DIR
from nas_server.api_utils import get_directory_contents

class TestSysFunctions(unittest.TestCase):

	def setUp(self):
		rebuild_test_tree()

	def tearDown(self):
		remove_test_tree()

	def test_directory_contents(self):
		expected_dict = {
			'path': TEST_DIR, 
			'children': [
				{'is_dir': False, 'filename': 'file1.txt'}, 
				{'is_dir': False, 'filename': 'file2.txt'}, 
				{'is_dir': False, 'filename': 'file3.txt'}, 
				{'is_dir': True, 'filename': 'folder 1'}, 
				{'is_dir': True, 'filename': 'folder 2'}, 
				{'is_dir': True, 'filename': 'folder 3'}
			]
		}
		dir_contents = get_directory_contents(TEST_DIR)
		self.assertEqual(expected_dict, dir_contents)

if __name__ == '__main__':
    unittest.main()