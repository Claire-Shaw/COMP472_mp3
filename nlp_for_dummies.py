import os
import string
import re
import pandas as pd
import math
import language_model
import utility_functions

def data_prep():
	### Get all corpora files
	### Clean them (stop words, white space)
	### Organize them into language groups
	### Concatenate groups
	file_names = os.listdir('./data')
	raw_corpora = get_raw_corpora(file_names)
	clean_corpora = clean_text(raw_corpora)

	return clean_corpora

def get_raw_corpora(file_names):
	dirty_corpora = []
	lang_group = set()
	for f in file_names:
		lang_group.add(f[0:2])
	for lang in lang_group:
		for f in file_names:
			if lang == f[0:2]:
				with open('./data/' + f, 'r') as file:
					dirty_corpora.append( (lang, file.read()) )
	dirty_df = pd.DataFrame(dirty_corpora, columns=['lang', 'text'])

	return dirty_df

def clean_text(raw):
	### Set to lowercase
	df = raw
	df['text'] = df['text'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
	df['text'] = df['text'].apply(lambda x: x.lower())
	df['text'] = df['text'].apply(lambda x: re.sub(r"\W", "", x))
	df['text'] = df['text'].apply(lambda x: re.sub(r"\d", "", x))
	clean_df = df.groupby('lang').agg(lambda x: x.sum())
	clean_dict = dict([(x,y) for x, y in zip(df.lang, df.text)])

	return clean_dict


data = data_prep()
french_model = language_model.LanguageModel('FRENCH')
french_model.generate_model(data['fr'])
english_model = language_model.LanguageModel('ENGLISH')
english_model.generate_model(data['en'])
probability_en = 0
probability_fr = 0
for bigram in utility_functions.generate_bigrams("loiseauvole"):
	print("BIGRAM : " + bigram)
	probability_en += math.log(english_model.predict_bigram(bigram), 10)
	probability_fr += math.log(french_model.predict_bigram(bigram), 10)
	print("French: {} English: {}".format(probability_fr,probability_en))
