#include <stdio.h>
#include <cs50.h>

int main(void)
{
    // Ask user for height n that is a positive number less than 23
    int n;
    int j;
    int k;
    do
    {
        n = get_int("Height of pyramid less than 23: ");
    }
    while (n < 0 || n > 23);

    // Print height of pyramid
    for (int i = 0; i < n; i++)
    {
        // Print spaces
        for (k = (i + 1); k < n; k++)
        {
            printf(" ");
        }

        // Print hashes
        for (j = (n - (i + 1)); j < n; j++)
        {
            printf("#");
        }

        // Print additional column
        printf("#");

        // Print new line
        printf("\n");
    }
}
