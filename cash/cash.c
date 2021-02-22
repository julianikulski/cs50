#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)

{
    // ask user for amount of change
    float n;
    int m;
    do
    {
        n = get_float("How much change is owed to you?: ");
    }
    while (n < 0);

    // convert the dollars into cents and round float to two decimals
    float y = (int)(n * 100 + .5);
    m = y;

    // trickle down check from largest to smallest coin
    // how many quarters will be paid out
    int l = (m % 25);
    int o;
    if (m >= 25)
    {
        o = ((m - l) / 25);
    }
    else
    {
        o = 0;
    }
    // how many nickles will be paid out
    int k = (l % 10);
    int p;
    if (l >= 10)
    {
        p = ((l - k) / 10);
    }
    else
    {
        p = 0;
    }
    // how many dimes will be paid out
    int j = (k % 5);
    int q;
    if (k >= 5)
    {
        q = ((k - j) / 5);
    }
    else
    {
        q = 0;
    }
    // how many pennies will be paid out
    int r;
    if (j >= 1)
    {
        r = j;
    }
    else
    {
        r = 0;
    }
    // total number of coins that will be paid out
    int h = (o + p + q + r);

    // print number of coins used
    printf("%i\n", h);
}