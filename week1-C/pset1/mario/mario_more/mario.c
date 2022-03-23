#include <stdio.h>
#include <cs50.h>

int get_input(void);

int main(void)
{
    //Ask user for the height of the pyramide
    int height;
    height = get_input();
    
    for (int i = 0; i < height; i++)
    {
        //Print the spaces of the left parcel (number of rows - number of the current row)
        for (int s = 0; s < height - (i + 1); s++)
        {
            printf(" ");
        }
        
        //Print the hashes of the left parcel (number of the current row)
        for (int j = 0; j < (i + 1) ; j++)
        {
            printf("#");
        }
        
        //Print the gap between parcels left and right
        printf("  ");
        
        //Print the hashes of the right parcel
        for (int j = 0; j < (i + 1) ; j++)
        {
                
            printf("#");
        }
       
        //Go to the next row
        printf("\n");
    }
}


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