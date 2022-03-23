#include <stdio.h>
#include <cs50.h>

int get_input(void);

int main(void)
{
    //Ask user for pyramide height
    int height = get_input();
    
    
    for (int i = 0; i < height; i++)
    {
        //print the spaces (number of rows - number of the current row)
        for (int s = 0; s < height - (i + 1); s++)
        {
            printf(" ");
        }
        //print the hashes (number of the current row)
        for (int j = 0; j < (i + 1) ; j++)
        {
            //Go to next row    
            printf("#");
        }
        printf("\n");
    }
}

//Function for getting the height from user
int get_input(void)
{
    int n;
    do
    {
        n = get_int("What's the height (From 1 to 8)? ");
    }
    while (n < 1 || n > 8);
    return n;
}