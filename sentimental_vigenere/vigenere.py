import sys
from cs50 import get_float, get_string, get_int

# get keyword
if len(sys.argv) == 2:
    l = sys.argv[1]
else:
    print("Usage: python vigenere.py keyword")
    sys.exit("1")

# if keyword contains a non-alphabetical character
for m in range(len(l)):
    if str.isalpha(l[m]) is False:
        print("Please enter a keyword with letters and no numbers")
        sys.exit("1")

# request plaintext
s = get_string("plaintext: ")

# declaring j to ensure that enciphering is only done is character in l isalpha
j = 0

# encipher the plaintext using the keyword
print("ciphertext: ", end="")
for i in range(len(s)):
    # keeping j independent of i and only moving forward if char in l isalpha
    j = j % len(l)

    # for all alphabetic values
    if str.isalpha(s[i]):
        # preserve case
        if str.isupper(s[i]):
            # shift upper case plaintext character by key
            if str.isupper(l[j]):
                # ensure that characters in l will be treated irrespective of case
                o = (((ord(s[i])) - 65) + (ord(l[j]) - 65)) % 26
                print(f"{chr(o + 65)}", end="")
            else:
                o = (((ord(s[i])) - 65) + (ord(l[j]) - 97)) % 26
                print(f"{chr(o + 65)}", end="")
        else:
            # shift lower case plaintext character by key
            if str.isupper(l[j]):
                # ensure that characters in l will be treated irrespective of case
                o = (((ord(s[i])) - 97) + (ord(l[j]) - 65)) % 26
                print(f"{chr(o + 97)}", end="")
            else:
                o = (((ord(s[i])) - 97) + (ord(l[j]) - 97)) % 26
                print(f"{chr(o + 97)}", end="")
        # increasing j if ith character in l islpha is True
        j += 1
    else:
        # anything non-alphabetic will be printed without changes
        print(f"{s[i]}", end="")

# skip to next row at the end
print("")