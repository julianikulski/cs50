#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover forensic image name\n");
        return 1;
    }

    // input and output files
    char *file = argv[1];
    char outfile[4];

    // open input file
    FILE *inptr = fopen(file, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", file);
        return 2;
    }

    // FAT block size
    int block = 512;

    // temporary storage
    unsigned char *tempstor = malloc((block + 1) * sizeof(char));

    // counter for names of files
    int i = 0;

    // output file
    FILE *outptr = NULL;

    // repeat until the end of the file
    while (!feof(inptr))
    {
        // New JPEG? Condition to check whether read bytes are file header
        if (tempstor[0] == 0xff &&
            tempstor[1] == 0xd8 &&
            tempstor[2] == 0xff &&
            (tempstor[3] & 0xf0) == 0xe0)
        {
            // already found a JPEG, then close it
            if (outptr != NULL)
            {
                fclose(outptr);
            }

            // label new JPEG file;
            sprintf(outfile, "%03i.jpg", i); //file name
            // open output file
            outptr = fopen(outfile, "w");

            // check whether output file was created
            if (outptr == NULL)
            {
                fclose(inptr);
                fprintf(stderr, "Could not create %s.\n", outfile);
                return 3;
            }

            // write part of JPEG to new file
            fwrite(tempstor, sizeof(tempstor), 1, outptr);

            // count up the file numbers
            i++;
        }
        else if (i > 0)
        {
            // write part of JPEG to existing file
            fwrite(tempstor, sizeof(tempstor), 1, outptr);
        }

        // read data from input file
        fread(tempstor, sizeof(tempstor), 1, inptr);
    }

    // close infile
    fclose(inptr);

    // close outfiles
    fclose(outptr);

    // free allocated memory
    free(tempstor);

    // success
    return 0;
}

