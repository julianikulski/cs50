# Print a pyramid of maximum height of 23 based on the users input height

from cs50 import get_int

# Maximum height of the pyramid
HEIGHT = 23

# If number is negative or greater than 23, reprompt the user for input
while True:
    n = get_int("Height of pyramid less than 23: ")
    if n >= 0 and n < (HEIGHT + 1):
        break

# Print columns
for i in range(n):

    # Print spaces in rows
    for j in range(n - (i + 1)):
        print(" ", end="")

    # Print bricks in rows
    for k in range(i + 1):
        print("#", end="")

    # Print additional column
    print("#")