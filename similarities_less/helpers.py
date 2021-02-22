from nltk.tokenize import sent_tokenize
import re


def lines(a, b):
    """Return lines in both a and b"""

    # define list to store all unique matching lines in
    lines_in_both = []

    # split strings into separate lines
    lines_in_a = a.split('\n')
    lines_in_b = b.split('\n')

    # iterate over each line in string b
    for line_b in lines_in_b:
        # iterate over each line in string a
        for line_a in lines_in_a:
            if line_a == line_b:
                # check whether line has already been printed
                if line_a in lines_in_both:
                    break
                else:
                    # add unique matching line to final list
                    lines_in_both.append(line_a)
            else:
                pass
    return lines_in_both


def sentences(a, b):
    """Return sentences in both a and b"""

    # define final list to store all matching sentences
    sentences_in_both = []

    # use natural language tool kit to split the two strings a and b into sentences
    sentences_in_a = sent_tokenize(a)
    sentences_in_b = sent_tokenize(b)

    # iterate over all sentences in string b
    for sentence_b in sentences_in_b:
        # iterate over all sentences in string a
        for sentence_a in sentences_in_a:
            if sentence_a == sentence_b:
                # check whether matching string has already been printed
                if sentence_a in sentences_in_both:
                    break
                else:
                    # add unique string to final list
                    sentences_in_both.append(sentence_a)
            else:
                pass
    return sentences_in_both


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    # function to create list with all unique substrings in a string
    def extract(x, n):
        list_extract = []
        # replace line breaks with spaces
        x = re.sub(r"\n", r" ", x)
        # check whether n is greater than string length
        if n > len(x):
            pass
        # iterate over string and append all unique substrings
        else:
            for i in range(len(x)):
                if len(x) >= (i + n):
                    j = (i + n)
                    if x[i:j] in list_extract:
                        pass
                    else:
                        list_extract.append(x[i:j])
                else:
                    break
        return list_extract

    # define list that wll be returned with all substrings in both a and b of length n
    substrings_in_both = []

    # unique substrings in from string a
    substrings_in_a = extract(a, n)
    # unique substrings from string b
    substrings_in_b = extract(b, n)

    # iterate over string b
    for substring_b in substrings_in_b:
        # iterate over string a
        for substring_a in substrings_in_a:
            if substring_a == substring_b:
                # check whether substring has already been printed to list
                if substring_a in substrings_in_both:
                    break
                else:
                    # add unique substring to list
                    substrings_in_both.append(substring_a)
            else:
                pass

    return substrings_in_both