#include <stdio.h>
#include <cs50.h>

int main(void)
{
    //Ask the users for their names
    string name = get_string("What is your name ?\n");
    
    //Greet the user
    printf("Hello, %s!\n", name);
}
