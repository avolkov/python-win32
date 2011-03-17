import pickle, sys, os


if __name__ == "__main__":
	if len(sys.argv) < 2 or not os.path.isfile(sys.argv[1]):
		print >> sys.stderr, "Usage: "+sys.argv[0]+" <pickle_open_filename>"
		sys.exit(1)
	input = open(sys.argv[1], 'rb')
	data = pickle.load(input)
	for item in  data:
		print item
	
	input.close()
	