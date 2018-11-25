
def generate_bigrams(input):
    ### Returns a list of all the bigrams in the given input
    # Break sentence into tokens
    tokens = list(input)

    # Use the zip function to help us generate bigrams
    shiftToken = lambda i: (el for j, el in enumerate(tokens) if j>=i)
    shiftedTokens = (shiftToken(i) for i in range(2))
    bigrams = zip(*shiftedTokens)

    return ["".join(bigram) for bigram in bigrams]
