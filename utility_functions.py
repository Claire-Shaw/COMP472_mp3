
def generate_bigrams(input):
    ### Returns a list of all the bigrams in the given input
    # Break sentence into tokens
    tokens = list(input)

    # Use the zip function to help us generate bigrams
    shiftToken = lambda i: (el for j, el in enumerate(tokens) if j>=i)
    shiftedTokens = (shiftToken(i) for i in range(2))
    bigrams = zip(*shiftedTokens)

    return ["".join(bigram) for bigram in bigrams]


def generate_trigrams(input):
    ### Returns a list of all the trigrams in the given input
    # Break sentence into tokens
    tokens = list(input)

    # Use the zip function to help us generate bigrams
    shiftToken = lambda i: (el for j, el in enumerate(tokens) if j>=i)
    shiftedTokens = (shiftToken(i) for i in range(3))
    trigrams = zip(*shiftedTokens)

    return ["".join(trigram) for trigram in trigrams]
