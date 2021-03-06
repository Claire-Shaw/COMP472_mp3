import string 
import itertools
import math
import operator

import utility_functions

class LanguageModel:
	def __init__(self, language_name):
		### Delta for smoothing
		self.delta = 0.000001

		if(language_name == "English"):
			self.language_name = language_name
			self.language_code = "EN"
		elif(language_name == "French"):
			self.language_name = language_name
			self.language_code = "FR"
		else:
			self.language_name = language_name
			self.language_code = "OT"
		
		### Output files for language model dump 
		self.unigram_model_dump = "output/unigram" + self.language_code + ".txt"
		self.bigram_model_dump = "output/bigram" + self.language_code + ".txt"
		self.trigram_model_dump = "output/trigram" + self.language_code + ".txt"

		### Output files for sorted langauage model dump
		self.sorted_unigram_dump = "test_output/sortedUnigram" + self.language_code + ".txt"
		self.sorted_bigram_dump = "test_output/sortedBigram" + self.language_code + ".txt"
		self.sorted_trigram_dump = "test_output/sortedTrigram" + self.language_code + ".txt"

        ### Dictionaries for storing our unigram and bigram models ++++ TRIGRAMS
		all_lowercase_letters = string.ascii_lowercase
		two_letter_combos = []
		three_letter_combos = []
		for combo in list(itertools.product(all_lowercase_letters, all_lowercase_letters)):
			two_letter_combos.append(''.join(combo))
		
		for combo in list(itertools.product(all_lowercase_letters, two_letter_combos)):
			three_letter_combos.append(''.join(combo))


        # The unigram model will have 1 entry for each letter of the alphabet
		self.unigram_model = dict.fromkeys(all_lowercase_letters, 0)
        # The bigram model will have 1 entry for each set of two letters in the alphabet
        # P(x|y) will be stored in the dict with key yx
		self.bigram_model = dict.fromkeys(two_letter_combos, 0)

		# The trigram model will have 1 entry for each set of three letters on the alphabet
		self.trigram_model = dict.fromkeys(three_letter_combos, 0)


	def generate_model(self, training_data):
		### Generate both unigram and bigram models
		self.generate_unigram_model(training_data)
		self.generate_bigram_model(training_data)
		self.generate_trigram_model(training_data)

		### Dump trained models to output file
		self.dump_unigram_model()
		self.dump_bigram_model()


	def generate_unigram_model(self, training_data):
		print("Generating unigram model")

		### Build our dict of letter counts
		### At first, our model will contain the raw counts of letters seen in the training data
		### This will be converted to probabilities later
		for token in list(training_data):
			self.unigram_model[token] += 1

			
		total_letters = len(training_data)
		total_bins = len(self.unigram_model)

		### Convert our raw counts to probabilities after performing add-delta smoothing
		for key, value in self.unigram_model.items():
			self.unigram_model[key] = (value + self.delta) / (total_letters + self.delta * total_bins)
		
	
	def generate_bigram_model(self, training_data):
		print("Generating bigram model")

        ### Convert our training data to bigrams
		bigrams = utility_functions.generate_bigrams(training_data)

		### Build our dict of bigram counts
		### At first, our model will contain the raw counts of bigrams seen in the training data
		### This will be converted to probabilities later
		for bigram in bigrams:
			self.bigram_model[bigram] += 1
			
		total_bigrams = len(bigrams)
		total_bins = len(self.bigram_model)

		### Convert our raw counts to probabilities  after performing add-delta smoothing
		for key, value in self.bigram_model.items():
			self.bigram_model[key] = (value + self.delta) / (total_bigrams + self.delta * total_bins)
	
	
	def generate_trigram_model(self, training_data):
		print("Generating trigram model")

        ### Convert our training data to bigrams
		trigrams = utility_functions.generate_trigrams(training_data)

		### Build our dict of trigram counts
		### At first, our model will contain the raw counts of trigrams seen in the training data
		### This will be converted to probabilities later
		for trigram in trigrams:
			self.trigram_model[trigram] += 1
			
		total_trigrams = len(trigrams)
		total_bins = len(self.trigram_model)

		### Convert our raw counts to probabilities  after performing add-delta smoothing
		for key, value in self.trigram_model.items():
			self.trigram_model[key] = (value + self.delta) / (total_trigrams + self.delta * total_bins)


	def dump_unigram_model(self):
		with open(self.unigram_model_dump, 'w') as file:
			for key, value in self.unigram_model.items():
				file.write("P({}) = {}\n".format(key, value))
		print("{} unigram model has been dumped to {}".format(self.language_code, self.unigram_model_dump))

		### Sort our unigram model and dump it to the test_output folder
		with open(self.sorted_unigram_dump, 'w') as file:
			sorted_unigram_model = sorted(self.unigram_model.items(), key=operator.itemgetter(1))
			for x in sorted_unigram_model:
				file.write("{} = {}\n".format(x[0], x[1]))
		print("SORTED {} unigram model has been dumped to {}".format(self.language_code, self.sorted_unigram_dump))



	def dump_bigram_model(self):
		with open(self.bigram_model_dump, 'w') as file:
		    for key, value in self.bigram_model.items():
			    file.write("P({}|{}) = {}\n".format(key[1], key[0], value))
		print("{} bigram model has been dumped to {}".format(self.language_code, self.bigram_model_dump))
		
		### Sort our bigram model and dump it to the test_output folder
		with open(self.sorted_bigram_dump, 'w') as file:
			sorted_bigram_model = sorted(self.bigram_model.items(), key=operator.itemgetter(1))
			for x in sorted_bigram_model:
				file.write("{} = {}\n".format(x[0], x[1]))
		print("SORTED {} bigram model has been dumped to {}".format(self.language_code, self.sorted_bigram_dump))
	
    
    
	def predict_unigram(self, letter):
		probability = self.unigram_model[letter]
		return probability


	def predict_bigram(self, bigram):
		probability = self.bigram_model[bigram]
		return probability


	def predict_trigram(self, trigram):
		probability = self.trigram_model[trigram]
		return probability


	def get_language_name(self):
		return self.language_name
