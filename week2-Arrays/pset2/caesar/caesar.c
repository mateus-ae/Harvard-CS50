# include <stdio.h>
# include <cs50.h>
# include <ctype.h>
# include <string.h>
# include <stdlib.h>

string get_plaintext(void);
void print_cipher(string text, int key);

int main(int argc, string argv[])
{
    //check if the command line is acceptable
    if (argc != 2)
    {
        //if it isn't return an error message
        printf("Usage: ./caesar key\n");
        
        return 1;
    }
    
    for (int i = 0; i < strlen(argv[1]); i++)
    {
        if (!isdigit(argv[1][i]))
        {
            //if it isn't return an error message
            printf("Usage: ./caesar key\n");
            
            return 1;
        }
    }
    
    //convert the key to an integer
    int k = atoi(argv[1]);
    
    //ask the user for the plaintext
    string plaintext = get_plaintext();
    
    //execute the transformation to ciphertext
    print_cipher(plaintext, k);
}


string get_plaintext(void)
{
    string plaintext;
    do
    {
        // prompt user for a text. Don't accept if user types nothing
        plaintext = get_string("plaintext: ");
    }
    while (plaintext[0] == '\0');
    
    return plaintext;
}

void print_cipher(string text, int key)
{
    string plaintext = text;
    int k = key;
    
    printf("ciphertext: ");
    
    for (int i = 0; i < strlen(plaintext); i++)
    {
        //check if character is alphabetic. If it is, do the conversion
        if (isalpha(plaintext[i]))
        {
            int subtract;
            
            if (isupper(plaintext[i]))
            {
                subtract = 65;
            }
            else
            {
                subtract = 97;
            }
        
            int pi = plaintext[i] - subtract;
            int ci = (pi + k) % 26;
        
            printf("%c", ci + subtract);
        }
        else
        {
            //if it's not alphabetic, print the same character
            printf("%c", plaintext[i]);
        }
    }
    printf("\n");
}