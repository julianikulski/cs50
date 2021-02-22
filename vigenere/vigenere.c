#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, string argv[])
{
    // if less than or more than one keyword given, stop program
    string l;
    char c;
    if (argc != 2)
    {
        printf("Usage: ./vigenere keyword\n");
        return 1;
    }

    l = argv[1];
    for (int i = 0, n = strlen(l); i < n; i++)
    {
        // if keyword contains a non-alphabetical character
        c = l[i];
        if (isalpha(c) == false)
        {
            printf("Please enter a keyword with letters and no numbers\n");
            return 1;
        }
    }

    string m = get_string("plaintext: ");
    int o;
    int j = 0; // keeping j independent of i

    // move the letters by the key
    printf("ciphertext: ");
    for (int i = 0, n = strlen(m); i < n; i++)
    {
        // keeping j independent of i and only moving forward if char in l isalpha == true
        j = j % strlen(l);

        // for all alphabetic values
        if (isalpha(m[i]))
        {
            // preserve case
            if (isupper(m[i]))
            {
                // shift upper case plaintext character by key
                if (isupper(l[j]))
                {
                    // ensure that characters in l will be treated irrespective of case
                    o = ((((int) m[i]) - 65) + (l[j] - 65)) % 26;
                    printf("%c", (o + 65));
                }
                else
                {
                    o = ((((int) m[i]) - 65) + (l[j] - 97)) % 26;
                    printf("%c", (o + 65));
                }

            }
            else
            {
                // shift lower case plaintext character by key
                if (isupper(l[j]))
                {
                    // ensure that characters in l will be treated irrespective of case
                    o = ((((int) m[i]) - 97) + (l[j] - 65)) % 26;
                    printf("%c", (o + 97));
                }
                else
                {
                    o = ((((int) m[i]) - 97) + (l[j] - 97)) % 26;
                    printf("%c", (o + 97));
                }
            }
            j++; //increasing j if ith char in l isalpha == true
        }
        else
        {
            // anything non-alphabetic will be printed without changes
            printf("%c", m[i]);
        }
    }

    // after enciphering, move to the next row
    printf("\n");
}