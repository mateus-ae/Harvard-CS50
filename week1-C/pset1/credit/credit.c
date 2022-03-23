#include <stdio.h>
#include <cs50.h>
#include <math.h>

long get_number(void);
int sum_numbers(long number);
bool validate_length(long number);
void check_type(long number);

int main(void)
{
    //get the number from the user
    long number = get_number();

    //validate the card's length
    if (validate_length(number))
    {   
        //if length is valid than execute the luhn's algorithm
        int result_sum = sum_numbers(number);
        //if the sum ends with 0 check the type, else just print invalid
        if (result_sum % 10 == 0)
        {
            check_type(number);
        }
        
        else
        {
            printf("%s\n", "INVALID");
        }
    }
    
    else
    {
        printf("%s\n", "INVALID");
    }
}


//function for getting the number from user
long get_number(void)
{
    long number;
    
    do
    {
        number = get_long("Number: ");
    }
    while (number <= 0);
    
    return number;
}

//function to perform luhn's algorithm
int sum_numbers(long number)
{
    int r;
    
    long n = number;
    
    int i = 0; 
    int sum = 0;
    
    do
    {
        r = n % 10;
        //see if it's divisible by 2
        if (i % 2 == 0)
        {
            //if it is, just add r to sum
            sum += r;
        }
      
        else
        {
            //if it isn't multiply by 2 and separate digits if necessary
            r = r * 2;
            sum += r / 10 + r % 10;
        }
      
        n = n / 10;
        i++;
    }
    while (n > 0);
    
    return sum;
}

//function to validate the length
bool validate_length(long number)
{
    bool valid;
    
    long n = number;
    
    int i;
    
    for (i = 0; n > 0; i++)
    {
        n = n / 10;
    }
    //return tru if the length is equal to 13, 15 or 16
    if (i == 13 || i == 15 || i == 16)
    {
        valid = true;
    }
    
    
    else
    {
        valid = false;
    }
    
    return valid;
}

//function to check the type
void check_type(long number)
{
    if (number > 340000000000000 && number < 350000000000000)
    {
        printf("%s\n", "AMEX");
    }
    else if (number > 370000000000000 && number < 380000000000000)
    {
        printf("%s\n", "AMEX");
    }
    else if (number > 5100000000000000 && number < 5600000000000000)
    {
        printf("%s\n", "MASTERCARD");
    }
    else if (number > 4000000000000 && number < 5000000000000)
    {
        printf("%s\n", "VISA");
    }
    else if (number > 4000000000000000 && number < 5000000000000000)
    {
        printf("%s\n", "VISA");
    }
    else
    {
        printf("%s\n", "INVALID");
    }
}