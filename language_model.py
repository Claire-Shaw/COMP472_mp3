import string 
import itertools

import utility_functions

class LanguageModel:
    def __init__(self, language_name):
		### Delta for smoothing
	    self.delta = 0.5

	    if(language_name == "ENGLISH"):
		    self.language_code = "EN"
	    elif(language_name == "FRENCH"):
		    self.language_code = "FR"
	    else:
		    self.language_code = "OT"
		
		### Output files for language model dump 
        self.unigram_model_dump = "output/unigram" + language_code + ".txt"
        self.bigram_model_dump = "output/bigram" + language_code + ".txt"

        ### Dictionaries for storing our unigram and bigram models
        all_lowercase_letters = string.ascii_lowercase
        two_letter_combos = list(intertools.product(all_lowercase_letters, all_lowercase_letters))
        # The unigram model will have 1 entry for each letter of the alphabet
        self.unigram_model = dict.fromkeys(all_lowercase_letters, 0)
        # The bigram model will have 1 entry for each set of two letters in the alphabet
        # P(x|y) will be stored in the dict with key yx
        self.bigram_model = dict.fromkeys(two_letter_combos, 0)


    def generate_model(self, training_data):
		### Get dictionary of all three corpora cleaned
		clean_corp = data_prep()
        processed_data = utility_functions.input_processor(clean_corp)

		### Generate both unigram and bigram models
		self.generate_unigram_model(processed_data)
		self.generate_bigram_model(processed_data)

		### Dump trained models to output file
		self.unigram_model_dump()
		self.bigram_model_dump()


    def generate_unigram_model(self, processed_data):
        print("Generating unigram model")

		### Build our dict of letter counts
		### At first, our model will contain the raw counts of letters seen in the training data
		### This will be converted to log of probabilities later
		for token in list(processed_data):
			self.unigram_model[token] += 1
			
		total_letters = len(processed_data)
        total_bins = len(self.unigram_model)

		### Convert our raw counts to log of probabilities (base 10) after performing add-delta smoothing
		for key, value in self.unigram_model:
			self.unigram_model[key] = math.log((value + self.delta) / (total_letters + self.delta * total_bins), 10)
		
	
    def generate_bigram_model(self, processed_data):
		print("Generating bigram model")

		### Build our dict of bigram counts
		### At first, our model will contain the raw counts of letters seen in the training data
		### This will be converted to log of probabilities later
        bigrams = utility_functions.generate_bigrams(processed_data)
		for bigram in bigrams:
			self.bigram_model[bigram] += 1
			
		total_bigrams = len(bigrams)
        total_bins = len(self.bigram_model)

		### Convert our raw counts to log of probabilities (base 10) after performing add-delta smoothing
		for key, value in self.bigram_model:
			self.bigram_model[key] = math.log((value + self.delta) / (total_bigrams + self.delta * total_bins), 10)
	

    def unigram_model_dump(self):
		with open(self.unigram_model_dump, 'w') as file:
			for key, value in self.unigram_model:
				file.write("P({}} = {}".format(key, value))
		print("{} unigram model has been dumped to {}".format(self.language_code, self.unigram_model_dump))


    def bigram_model_dump(self):
	    with open(self.bigram_model_dump, 'w') as file:
		    for key, value in self.bigram_model:
			    file.write("P({}|{}} = {}".format(key[1], key[0], value))
	    print("{} bigram model has been dumped to {}".format(self.language_code, self.bigram_model_dump))
    
    
    def predict_unigram(self, letter):
        probability = self.unigram_model[letter]
        return probability


	def predict_bigram(self, bigram):
        probability = self.bigram_model[bigram]
        return probability
