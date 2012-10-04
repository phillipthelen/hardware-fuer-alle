import settings

def stripSlash(string):
	if string[-1:] != '/':
		return string
	return string[:-1]

def getMapDepth(city=False, postcode=False, street=False):
	return 10

def get_file_name(instance, old_filename):
	extension = os.path.splitext(old_filename)[1]
	filename = str(time.time()) + extension
	return 'avatars/' + filename