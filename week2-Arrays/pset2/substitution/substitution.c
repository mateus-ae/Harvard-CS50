#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>

string get_plaintext(void);
void print_ciphertext(string plaintext, string key);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        //if it isn't return an error message
        printf("Usage: ./substitution key\n");

        return 1;
    }

    //check if key has 26 characters
    if (strlen(argv[1]) == 26)
    {
        for (int i = 0; i < strlen(argv[1]); i++)
        {
            //check if key contains only alphabetical characters
            if (!isalpha(argv[1][i]))
            {
                printf("Usage: ./substitution key\n");

                return 1;
            }

            //check if characters repeat
            for (int j = i + 1; j < strlen(argv[1]); j++)
            {
                if (argv[1][i] == argv[1][j])
                {
                    printf("Usage: ./substitution key\n");

                    return 1;
                }
            }
        }
    }
    else
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }

    //get the plaintext from user
    string plaintext = get_plaintext();
    string key = argv[1];

    print_ciphertext(plaintext, key);
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

void print_ciphertext(string plaintext, string key)
{
    //reindex ascii alphabet
    //compare characters from plaintext with char from key
    //if some of them is lowercase it matters

    printf("ciphertext: ");

    for (int i = 0; i < strlen(plaintext); i++)
    {
        if (islower(plaintext[i]))
        {
            int index = plaintext[i] - 97;

            printf("%c", tolower(key[index]));
        }

        else if (isupper(plaintext[i]))
        {
            int index = plaintext[i] - 65;

            printf("%c", toupper(key[index]));
        }

        else
        {
            printf("%c", plaintext[i]);
        }
    }
    printf("\n");
}
