# Questions

## What's `stdint.h`?

It's a header file that provides typedefs and macros for fixed-width integral types in accordance with the C99 standard.

## What's the point of using `uint8_t`, `uint32_t`, `int32_t`, and `uint16_t` in a program?

These data types are used to define integers with specific lengths and ranges. I.e. uint8_t will be an unsigned char with length of 8 bits. Unsigned means that the integer gives you numbers within the range of 0 and 255.

## How many bytes is a `BYTE`, a `DWORD`, a `LONG`, and a `WORD`, respectively?

BYTE: 1 byte
DWORD: 4 bytes
LONG: 4 bytes
WORD: 2 bytes

## What (in ASCII, decimal, or hexadecimal) must the first two bytes of any BMP file be? Leading bytes used to identify file formats (with high probability) are generally called "magic numbers."

WORD bfType

## What's the difference between `bfSize` and `biSize`?

bfSize: The size, in bytes, of the bitmap file. This is used in the BITMAPFILEHEADER and includes pixels, padding, and headers.
biSize: The number of bytes required by the structure. This is used in the BITMAPINFOHEADER and includes only pixels and padding.

## What does it mean if `biHeight` is negative?

If biHeight is negative, the bitmap is a top-down DIB and its origin is the upper-left corner.

## What field in `BITMAPINFOHEADER` specifies the BMP's color depth (i.e., bits per pixel)?

biBitCount

## Why might `fopen` return `NULL` in lines 24 and 32 of `copy.c`?

If the input or output file cannot be opened, e.g. because of an incorrect format, it may return NULL.

## Why is the third argument to `fread` always `1` in our code?

In the first two instances I am reading just the header each time, which is considered one element. The thrid and fourth instance looks at one RGBTRIPLE at a time in a for loop, thus, always just checking for one element at a time as well.

## What value does line 63 of `copy.c` assign to `padding` if `bi.biWidth` is `3`?

3

## What does `fseek` do?

Moving pointer to different address.

## What is `SEEK_CUR`?

It specifies the current position so that if fseek is executed it'll move the pointer by x number of bytes relative to the current position.
