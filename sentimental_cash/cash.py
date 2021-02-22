from cs50 import get_float, get_int

# Defining value of coins possible to dispense
QUARTER = 25
DIME = 10
NICKEL = 5
PENNY = 1

# Prompting user for input, which will be stored as float
while True:
    n = get_float("Change owed: ")
    if n > 0:
        break

# Converting float to int
k = int(round(n * 100))

# How many quarters will be dispensed
j = k % QUARTER
if k >= QUARTER:
    o = (k - j) / QUARTER
else:
    o = 0

# How many dimes will be dispensed
i = j % DIME
if j >= DIME:
    p = (j - i) / DIME
else:
    p = 0

# How many nickels will be dispensed
h = i % NICKEL
if i >= NICKEL:
    r = (i - h) / NICKEL
else:
    r = 0

# How many penny will be dispensed
if h >= PENNY:
    s = h
else:
    s = 0

# How many coins will be dispensed
f = o + p + r + s

print(f"{f}")