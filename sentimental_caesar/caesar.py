import sys
from cs50 import get_int, get_string

# get k value
if len(sys.argv) == 2:
    k = int(sys.argv[1])
else:
    print("Usage: python caesar.py k")
    k = 0
    sys.exit("1")

# advising user what to enter
if len(sys.argv) == 2 and k != 0:
    s = get_string("plaintext: ")

    # print ciphertext
    print("ciphertext: ", end="")
    for i in range(len(s)):
        # check whether character is an alphabetic character
        if str.isalpha(s[i]):
            if str.isupper(s[i]):
                # if it is uppercase, convert
                t = (((ord(s[i]) - 65) + k) % 26)
                print(f"{chr(t + 65)}", end="")
            else:
                # if it is lowercase, convert
                t = (((ord(s[i]) - 97) + k) % 26)
                print(f"{chr(t + 97)}", end="")
        else:
            # anything non-alphabetic will be printed without enciperhing
            print(f"{s[i]}", end="")
    print("")

# instructions on how to use this programme
else:
    print("Usage: python caesar.py k")