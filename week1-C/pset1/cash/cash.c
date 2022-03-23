#include <stdio.h>
#include <cs50.h>
#include <math.h>

float get_change_owed(void);

int main(void)
{
    float change = get_change_owed();
    //number of dolars
    int dolars = floor(change);
    //number of cents
    int cents = round((change - dolars) * 100); 
    
    //Calculating the amount of each coin
    int quarters_d = dolars / 0.25;
    int quarters_c = floor(cents / 25);
    int dimes = floor((cents - quarters_c * 25) / 10);
    int nickels = floor((cents - (quarters_c * 25) - (dimes * 10)) / 5);
    int pennies = cents - quarters_c * 25 - dimes * 10 - nickels * 5;
    
    //Summing the amount of coins
    int coins = quarters_d + quarters_c + dimes + nickels + pennies;
    
    //printf("%i dolars and %i cents\n", dolars, cents);
    //printf("quarters_d: %i\n", quarters_d);
    //printf("quarters_c: %i\n", quarters_c);
    //printf("dimes: %i\n", dimes);
    //printf("nickels: %i\n", nickels);
    //printf("pennies: %i\n", pennies);
    printf("%i\n", coins);
}

float get_change_owed(void)
{
    float d;
    do
    {
        d = get_float("Change owed: ");
    }
    while (d < 0);
    return d;
}