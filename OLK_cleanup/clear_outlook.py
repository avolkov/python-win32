#!C:\Python27\Python.exe -u
import os, re


def rm_rf(directory):
	if os.path.isdir(directory):
		for filepath in os.listdir(directory):
			full_path = os.path.join(directory, filepath)
			if os.path.isfile(full_path):
				os.remove(full_path)

				
if __name__ == "__main__":
	"""
	Cleanup temporary outlook files
	"""
        #print("running main")
	olk_search = re.compile("^OLK.+$")
	final_path = os.environ['USERPROFILE']
	for path_element in ['Local Settings', 'Temporary Internet Files']:
		final_path = os.path.join(final_path, path_element);
	if not os.path.isdir(final_path):
		print("Temporary files dir doesn't exists")
	else:
		for subdir in os.listdir(final_path):
			if olk_search.match(subdir):
				print("Found match %s" % os.path.join(final_path,subdir))
				rm_rf(os.path.join(final_path,subdir));
