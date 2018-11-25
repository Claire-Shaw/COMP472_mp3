import os

def generate_model():
	### Get dictionary of all three corpora cleaned
	clean_corp = data_prep()

def predict(sentence):
	print()

def data_prep():
	### Get all corpora files
	### Clean them (stop words, white space)
	### Organize them into language groups
	### Concatenate groups
	file_names = os.listdir('./data')
	dirty_corpora = []
	lang_group = set()
	for f in file_names:
		lang_group.add(f[0:2])
	for lang in lang_group:
		for f in file_names:
			if lang in f:
				with open(f, 'r') as file:
					dirty_corpora.append( (lang, file.read()) )

	
data_prep()