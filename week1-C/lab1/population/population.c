#include <stdio.h>
#include <cs50.h>

int main(void)
{
    // TODO: Prompt for start size
    int start_size;
    do
    {
        start_size = get_int("Please, choose a starting size (9 or higher): ");
    }
    while (start_size < 9);
    
    // TODO: Prompt for end size
    int end_size;
    do
    {
        end_size = get_int("Now, choose the ending size (It can't be less than the starting size): ");   
    }
    while (end_size < start_size);
    
    // TODO: Calculate number of years until we reach threshold
    int new_size = start_size;
    int years;
    
    for (years = 0; new_size < end_size; years++)
    {
        new_size = new_size + new_size / 3 - new_size / 4;
    }
    
    
    // TODO: Print number of years
    printf("Years: %i\n", years);
}