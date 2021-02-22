// Helper functions for music

#include <cs50.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

#include "helpers.h"
#include "wav.h"

// Notes in an octave
const string NOTES_a[] = {"C", "C#", "D", "D#", "E", "F",
                          "F#", "G", "G#", "A", "A#", "B"
                         };
const string NOTES_b[] = {"C", "Db", "D", "Eb", "E", "F",
                          "Gb", "G", "Ab", "A", "Bb", "B"
                         };

// string NOTES[0] = "-9" //C
// string NOTES[1] = "-8" //C#
// string NOTES[2] = "-7" //D
// string NOTES[3] = "-6" //D#
// string NOTES[4] = "-5" //E
// string NOTES[5] = "-4" //F
// string NOTES[6] = "-3" //F#
// string NOTES[7] = "-2" //G
// string NOTES[8] = "-1" //G#
// string NOTES[9] = "0" //A
// string NOTES[10] = "1" //A#
// string NOTES[11] = "2" //B

// Converts a fraction formatted as X/Y to eighths
int duration(string fraction)
{
    // breaking up the numerator and denominator
    string numerator = strtok(fraction, "/");
    string denominator = strtok(NULL, "/");

    float fraction_float = 0;
    int numerator_int = atoi(numerator);
    int denominator_int = atoi(denominator);
    float numerator_float = (float) numerator_int;
    float denominator_float = (float) denominator_int;
    fraction_float = ((numerator_float / denominator_float) * 8);
    return fraction_float;
}

// Calculates frequency (in Hz) of a note
int frequency(string note)
{
    // using note_a as conversion ratio from NOTES location to location in relation to note A4
    int note_a = 9;

    if (strlen(note) < 3 && strlen(note) > 0) // white key
    {
        char octave_1 = note[1];
        int octave_int = octave_1 - '0';
        for (int i = 0, n = 12; i < n; i++)
        {
            double x = 0;
            double y = 0;
            int compare_white = strncmp(note, NOTES_a[i], 1);
            if (compare_white == 0)
            {
                int num_note = i - note_a;
                double m = num_note + 12 * (octave_int - 4); // check second integer
                x = pow(2, (m / 12)) * 440;
                y = round(x);
                return y;
            }
        }
        return false;
    }
    else // if(strlen(note) == 3) // black key
    {
        // converting sharp notes
        if (note[1] == '#')
        {
            char octave_1 = note[2];
            int octave_int = octave_1 - '0';
            for (int i = 0, n = 12; i < n; i++)
            {
                double x = 0;
                double y = 0;
                int compare_black = strncmp(note, NOTES_a[i], 2);
                if (compare_black == 0)
                {
                    int num_note = i - note_a;
                    double m = num_note + 12 * (octave_int - 4); // check third integer
                    x = pow(2, (m / 12)) * 440;
                    y = round(x);
                    return y;
                }
            }
            return false;
        }
        else
        {
            // converting flat notes
            char octave_1 = note[2];
            int octave_int = octave_1 - '0';
            for (int i = 0, n = 12; i < n; i++)
            {
                double x = 0;
                double y = 0;
                int compare_black = strncmp(note, NOTES_b[i], 2);
                if (compare_black == 0)
                {
                    int num_note = i - note_a;
                    double m = num_note + 12 * (octave_int - 4); // check third integer
                    x = pow(2, (m / 12)) * 440;
                    y = round(x);
                    return y;
                }
            }
            return false;
        }
        return false;
    }
}

// Determines whether a string represents a rest
bool is_rest(string s)
{
    // checking input and returning true if only line ending returned
    // string s = get_string("");

    char empty[2] = "\0";
    int compare = strcmp(empty, s);

    if (compare == 0)
    {
        return true;
    }
    else
    {
        return false;
    };
}
