import nlp_for_dummies
import language_model
import math
import utility_functions

def main():
	# Dict for storing and returning language models
	models = {}
	while(True):
		input_op = input("\nDo you want to:\n"
						"1. Train model?\n"
						"2. Read from file? (check '.txt' files in '/sentences')\n"
						"3. Read from console?\n"
						)
		
		if input_op == '1':
			models = generate_models() 
		elif input_op == '2':
			if not models:
				print("You must train the models first!")
			else:
				fp = "./sentences/"\
					+ input("Enter filename (no extension):\n")\
					+ ".txt"

				with open(fp, 'r') as file:
					sentence_buffer = [line.strip() for line in file]

				for index, sentence in enumerate(sentence_buffer):
					predict(sentence, index+1, models)

		elif input_op == '3':
			if not models:
				print("You must train the models first!")
			else:
				predict( input("Enter sentence:\n"), 'MANUAL', models)
		else:
			print("Invalid option entered.\n")


def generate_models():
	# Dictionary for storing and returning our language models
	models = {}

	data = nlp_for_dummies.data_prep()

	models['fr'] = language_model.LanguageModel('French')
	models['en'] = language_model.LanguageModel('English')
	models['es'] = language_model.LanguageModel('Spanish')
	
	models['fr'].generate_model(data['fr'])
	models['en'].generate_model(data['en'])
	models['es'].generate_model(data['es'])
	
	return models


def predict(sentence, index, models):
	out_file = "./output/out{}.txt".format(index)

	### Cumulative sum of log of probabilities
	probability_uni_fr = 0.0
	probability_uni_en = 0.0
	probability_uni_ot = 0.0
	probability_bi_fr = 0.0
	probability_bi_en = 0.0
	probability_bi_ot = 0.0

	with open(out_file, 'w') as file:
		file.write(sentence)
		print('"' + sentence + '"')

		clean_sentence = nlp_for_dummies.clean_sentence(sentence)
		
		file.write("\n\n")
		file.write("UNIGRAM MODEL:\n")
		for unigram in list(clean_sentence):
			file.write("\nUNIGRAM: " + unigram +"\n")
			
			### Single unigram probabilities
			prob_fr = models['fr'].predict_unigram(unigram)
			prob_en = models['en'].predict_unigram(unigram)
			prob_ot = models['es'].predict_unigram(unigram)
			### Cumulative sum of log probablities
			probability_uni_fr += math.log10(prob_fr)
			probability_uni_en += math.log10(prob_en)
			probability_uni_ot += math.log10(prob_ot)

			file.write("FRENCH: P({}) = {} ==> log prob of sentence so far: {}\n".format(unigram, prob_fr, probability_uni_fr))
			file.write("ENGLISH: P({}) = {} ==> log prob of sentence so far: {}\n".format(unigram, prob_en, probability_uni_en))
			file.write("OTHER: P({}) = {} ==> log prob of sentence so far: {}\n".format(unigram, prob_ot, probability_uni_ot))

		file.write("\n")	

		if probability_uni_fr >= probability_uni_en and probability_uni_fr >= probability_uni_ot:
			winning_language = models['fr'].get_language_name()
		elif probability_uni_en >= probability_uni_ot:
			winning_language = models['en'].get_language_name()
		else:
			winning_language = models['es'].get_language_name()

		file.write("According to the unigram model, the sentence is in " + winning_language + "\n")
		print("According to the unigram model, the sentence is in " + winning_language)
		
		file.write("----------------\n")

		file.write("BIGRAM MODEL:\n")
		for bigram in utility_functions.generate_bigrams(clean_sentence):
			file.write("\nBIGRAM: " + bigram + "\n")
			
			### Single bigram probabilities
			prob_fr = models['fr'].predict_bigram(bigram)
			prob_en = models['en'].predict_bigram(bigram)
			prob_ot = models['es'].predict_bigram(bigram)
			### Cumulative probablities
			probability_bi_fr += math.log10(prob_fr)
			probability_bi_en += math.log10(prob_en)
			probability_bi_ot += math.log10(prob_ot)

			file.write("FRENCH: P({}|{}) = {} ==> log prob of sentence so far: {}\n".format(bigram[1], bigram[0], prob_fr, probability_bi_fr))
			file.write("ENGLISH: P({}|{}) = {} ==> log prob of sentence so far: {}\n".format(bigram[1], bigram[0], prob_en, probability_bi_en))
			file.write("OTHER: P({}|{}) = {} ==> log prob of sentence so far: {}\n".format(bigram[1], bigram[0], prob_ot, probability_bi_fr))

		file.write("\n")

		if probability_bi_fr >= probability_bi_en and probability_bi_fr >= probability_bi_ot:
			winning_language = models['fr'].get_language_name()
		elif probability_bi_en >= probability_bi_ot:
			winning_language = models['en'].get_language_name()
		else:
			winning_language = models['es'].get_language_name()

		file.write("According to the bigram model, the sentence is in " + winning_language)
		print("According to the bigram model, the sentence is in " + winning_language)

		predict_trigram(models, clean_sentence)

def predict_trigram(models, clean_sentence):
	
	probability_tri_fr = 0
	probability_tri_en = 0
	probability_tri_ot = 0

	for trigram in utility_functions.generate_trigrams(clean_sentence):
				
		### Single trigram probabilities
		prob_fr = models['fr'].predict_trigram(trigram)
		prob_en = models['en'].predict_trigram(trigram)
		prob_ot = models['es'].predict_trigram(trigram)
		
		### Cumulative probablities
		probability_tri_fr += math.log10(prob_fr)
		probability_tri_en += math.log10(prob_en)
		probability_tri_ot += math.log10(prob_ot)
	

		if probability_tri_fr >= probability_tri_en and probability_tri_fr >= probability_tri_ot:
			winning_language = models['fr'].get_language_name()
		elif probability_tri_en >= probability_tri_ot:
			winning_language = models['en'].get_language_name()
		else:
			winning_language = models['es'].get_language_name()

	print("According to the trigram model, the sentence is in " + winning_language + "\n")



if __name__ == "__main__":
    main()