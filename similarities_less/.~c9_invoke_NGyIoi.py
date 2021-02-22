from nltk.tokenize import sent_tokenize

def lines(a, b):
    """Return lines in both a and b"""

    # TODO
    len(a)
    len(b)
    if len(a) >= len(b):
        x = a
    else:
        x = b
    # until the end of the file
    for line in x:
        # split file1 into separate strings (sentences)
        a = a.splitlines()
        print(a)
        # split file2 into separate strings (sentences)
        b = b.splitlines()
        print(b)
        # iterate over characters in both sentences and check whether they are the same
        for i in a:
        # if they are the same
            for j in b:
                if i == j:
            # if line has already been printed
                # do not print line
                    break
            # if not
                else:
                # print line
                    print(i)
        # else
            # do not print and read the next string
    return []


def sentences(a, b):
    """Return sentences in both a and b"""

    # TODO
    return []


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    # TODO
    return []
