import re

def generate_bigrams(input):
    ### Returns a list of all the bigrams in the given input
    # Break sentence into tokens
    tokens = list(input)

    # Use the zip function to help us generate bigrams
    shiftToken = lambda i: (el for j, el in enumerate(tokens) if j>=i)
    shiftedTokens = (shiftToken(i) for i in range(2))
    bigrams = zip(*shiftedTokens)

    return ["".join(bigram) for bigram in bigrams]


def input_processor(raw_input):
    # Convert to lowercase
    clean_input = raw_input.lower()
    # Remove all punctuation, numbers and whitespace
    clean_input = re.sub(r'[^a-z]', '', clean_input)

    return clean_input