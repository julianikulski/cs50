#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, string argv[])
{
    // denominating int k
    int k;
    if (argc == 2)
    {
        k = atoi(argv[1]);
    }
    else
    {
        printf("Usage: ./caesar k \n");
        return 1;
        k = 0;
    }
    // check whether input is only 2 strings and an integer
    int j;
    if (argc == 2 && k != 0)
    {
        // ask the user for the text to be enciphered
        string l = get_string("plaintext: ");

        // move the letters by the key
        printf("ciphertext: ");
        for (int i = 0, n = strlen(l); i < n; i++)
        {
            // for all alphabetic values
            if (isalpha(l[i]))
            {
                // preserve case
                if (isupper(l[i]))
                {
                    // shift upper case plaintext character by key
                    j = ((((int) l[i]) - 65) + k) % 26;
                    printf("%c", (j + 65));
                }
                else
                {
                    // shift lower case plaintext character by key
                    j = ((((int) l[i]) - 97) + k) % 26;
                    printf("%c", (j + 97));
                }
            }
            else
            {
                // anything non-alphabetic will be printed without changes
                printf("%c", l[i]);
            }
        }
        // after enciphering, move to the next row
        printf("\n");
    }
    else
    {
        // instructions on how to use this program
        printf("Usage: ./caesar k\n");
    }

}