// Implements a dictionary's functionality

#include <stdbool.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>

#include "dictionary.h"

// Defining a trie node
typedef struct _node
{
    bool is_word;
    struct _node *children[27];
}
node;

// Defining the dictionary words counter
int dict_words = 0;

//Defining root node
node *root = NULL;

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // declaring pointer current and setting its value equal to pointer
    node *current = root;

    // check if allocating space suceeded
    if (!current)
    {
        printf("Could not create current");
        return false;
    }

    // check whether word can be found in dictionary
    for (int i = 0; word[i] != '\0'; i++)
    {
        // Turn character from ASCII to 1-26 format
        int f = 0;

        if (isalpha(word[i]) && islower(word[i]))
        {
            f = (word[i] - 97) % 26;
        }
        else if (isalpha(word[i]) && isupper(word[i]))
        {
            f = (word[i] - 65) % 26;
        }
        else if (word[i] == '\'')
        {
            f = CHAR_SIZE - 1; // this '\'' character should be in the 27th place of the array of children
        }

        // iterate through the trie with the current words given in 'word'
        if (current->children[f] != NULL)
        {
            current = current->children[f];
        }
        else
        {
            return false;
        }
    }

    // check whether it's the end of the word
    if (current->is_word == 1)
    {
        return true;
    }
    else
    {
        return false;
    }
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Prepare to load dictionary
    int counter = 0, e = 0;
    dict_words = 0;

    // callocing space for root node
    root = calloc(1, sizeof(node));

    // check if allocating space suceeded
    if (!root)
    {
        printf("Could not create root");
        return false;
    }

    // tracking the most current node
    node *current = root;

    // Try to open dictionary file
    FILE *dict_file = fopen(dictionary, "r");
    if (dict_file == NULL)
    {
        printf("Could not open %s.\n", dictionary);
        unload();
        return 1;
    }

    // Read characters from dictionary
    for (int d = fgetc(dict_file); d != EOF; d = fgetc(dict_file))
    {
        // Allow only alphabetical characters and apostrophes
        if (isalpha(d) || (d == '\'' && counter > 0))
        {
            // Turn character from ASCII to 1-26 format
            if (isalpha(d) && islower(d))
            {
                e = (d - 97) % 26;
            }
            else if (isalpha(d) && isupper(d))
            {
                e = (d - 65) % 26;
            }
            else if (d == '\'')
            {
                e = CHAR_SIZE - 1; // this '\'' character should be in the 27th place of the array of children
            }

            // move down the trie if the path already exists, otherwise create new node pointer
            if (current->children[e] == NULL)
            {
                current->children[e] = calloc(1, sizeof(node));
            }

            // current->children[e] = d;
            current = current->children[e]; //insert the character from the dictionary in this root node

            e = 0; // set e equal to 0 again to avoid old data when running through the loop
            counter++;
        }

        // We must have found a whole word
        else if (counter > 0)
        {
            // set boolean is_word to yes
            current->is_word = true;

            // update word counter
            dict_words++;

            // Prepare for next word
            counter = 0;

            current = root;
        }
    }

    // check whether the file was able to be opened
    if (ferror(dict_file))
    {
        fclose(dict_file);
        printf("Error reading dictionary");
        unload();
        return false;
    }

    // Close dictionary file
    fclose(dict_file);

    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    if (dict_words != 0)
    {
        return dict_words;
    }
    else
    {
        return 0;
    }
}

// Unloads dictionary from memory, returning true if successful else false
// looked at https://benjaminbrandt.com/dictionaries-are-made-from-tries/ to come up with recursive solution below
// recursive function to delete last node in the trie
void freememory(node *trav)
{
    // move to last node pointer, then free the node
    for (int index = 0; index < CHAR_SIZE; index++)
    {
        if (trav->children[index] != NULL)
        {
            freememory(trav->children[index]);
        }
    }

    free(trav);

}

// function to delete all nodes, including the root node
bool unload(void)
{

    if (root != NULL)
    {
        node *last = root;
        freememory(last);
        return true;
    }
    else
    {
        return false;
    }

}
