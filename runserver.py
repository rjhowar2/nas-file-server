import sys, getopt
from nas_server import app


def main(argv):
	host = "0.0.0.0"

	try:
		opts, args = getopt.getopt(argv,"lp:")
   	except getopt.GetoptError:
   		print 'runserver.py -l -p <port>'
   		sys.exit(2)

   	for opt, arg in opts:
   		if opt == "-l":
   			host = "localhost"

	app.run(debug=True, host=host)


if __name__ == "__main__":
   main(sys.argv[1:])