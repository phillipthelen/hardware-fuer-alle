def stripSlash(string):
	if string[-1:] != '/':
		return string
	return string[:-1]