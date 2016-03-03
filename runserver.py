import sys, getopt, os
from nas_server import app


def main(argv):
	host = "0.0.0.0"
	test_mode = False
	base_dir = "%s/%s" % (os.path.dirname(os.path.realpath("nas_server/")), "nas_server/tests/test_files_dir")

	try:
		opts, args = getopt.getopt(argv,"tlp:d:")
	except getopt.GetoptError:
		print 'runserver.py -t -l -p <port> -d <base_directory>'
		sys.exit(2)

	for opt, arg in opts:
		if opt == "-l":
			host = "127.0.0.1"
		if opt == "-t":
			test_mode = True
		if opt == "-d":
			base_dir = arg

	app.config['test_mode'] = test_mode
	app.config['base_directory'] = base_dir
	
	app.run(debug=test_mode, host=host)


if __name__ == "__main__":
	main(sys.argv[1:])