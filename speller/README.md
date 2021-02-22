# Questions

## What is pneumonoultramicroscopicsilicovolcanoconiosis?

It represents an example word with the maximum length of 45 characters as defined in the constant LENGTH in dictionary.h.

## According to its man page, what does `getrusage` do?

getrusage()  returns resource usage measures for who, which can be one of
    the following:
    RUSAGE_SELF
    RUSAGE_CHILDREN
    RUSAGE_THREAD

## Per that same man page, how many members are in a variable of type `struct rusage`?

16

## Why do you think we pass `before` and `after` by reference (instead of by value) to `calculate`, even though we're not changing their contents?

Using pointers saves memory and time. If we use a pointer, we will not copy the entire variable again into memory and feed it into our 'calculate' function.
Since optimizing time is our goal for this exercise, we want to avoid spending any unnecessary time on copying data.
A pointer will just reference the data in that particular storage location that it points to.

## Explain as precisely as possible, in a paragraph or more, how `main` goes about reading words from a file. In other words, convince us that you indeed understand how that function's `for` loop works.

When executing the main function, it first checks whether the input givenby the user was in the correct format. Structure for measuring
data usage and benchmarks are defined. Then the dictionary is loaded. It is then checked whether the dictionary was in fact loaded and
the time to load it is measured. Our file with the text to be checked is then opened (and checked whether it successfully opened).

The spell-check is the prepared by setting index to 0, mispellings to 0 and words to 0. The variable word is then defined as a string of length 46.
We then enter the spell-check loop: this loop is executed until the end of the file. One character at a time is read from the file,
checked whether it is a letter or an apostrophe that is not at the beginning of a word and then appends that character to the word and counts up
the index to move one position further the next time a character is read. Numerical values are skipped. If we have at least one character in our
new word and we find a a space value, the current word is terminated with '\0' and our word counter is increased by 1.

We then check the spelling of the word, measure the time of that and if the word is misspelled, it is printed and the misspellings counter is
increased by 1. Then the index is set to 0 to prepare for the next word. After this loop, we check whether there was an error reading the file
and close the file. The size of the dictionary is determined at the end and the time for the size determination is measured. The memory for the
dictionary is then freed again and this functions time is measured. Finally, the list of benchmarks is printed.

## Why do you think we used `fgetc` to read each word's characters one at a time rather than use `fscanf` with a format string like `"%s"` to read whole words at a time? Put another way, what problems might arise by relying on `fscanf` alone?

We want to check whether the data we read into our load function only contains letters and the '\'' (apostrophe character).
We need to check with isalpha() whether the individual characters are indeed only letters or '\''.
If we used fscanf to scan entire words and we didn't utilize any additional checks, we would read in words that contain numbers.

Moreover, using fscanf() requires to know the layout of the data within an input file before the function is run.
This also means that it needs to be adjusted every time we run it on a different text file.

This leads to issues with the maximum length of a word we allow. If we read in a string that is longer than the maximum of 45 characters, we risk segmentation fault.

## Why do you think we declared the parameters for `check` and `load` as `const` (which means "constant")?

The words in the dictionary and the words from the text files that is our input file should not be changed once we load and check them in our program.
'check' and 'load' are created containing a mutable pointer to an immutable string/character. This means that the contents of 'word' and 'dictionary' cannot be changed

