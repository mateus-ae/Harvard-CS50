# include <stdio.h>
# include <cs50.h>
# include <string.h>
# include <ctype.h>
# include <math.h>

string get_text(void);
int count_letters(string text);
int count_words(string text);
int count_sentences(string text);
int calculate_grade(int letters, int words, int sentences);

int main(void)
{
    //get the text from the user
    string text = get_text();

    //count the letters
    int letters = count_letters(text);

    //count the words
    int words = count_words(text);

    //count sentences
    int sentences = count_sentences(text);

    //calculate grade
    int grade = calculate_grade(letters, words, sentences);

    //print the grade
    if (grade >= 16)
    {
        printf("Grade 16+\n");
    }

    else if (grade < 1)
    {
        printf("Before Grade 1\n");
    }

    else
    {
        printf("Grade %i\n", grade);
    }
}

string get_text(void)
{
    string text;
    do
    {
        text = get_string("Text: ");
    }
    while (text[0] == '\0');

    return text;
}

int count_letters(string text)
{
    int letters = 0;

    for (int i = 0; i < strlen(text); i++)
    {
        char c = text[i];

        //we just want alphabetic characters as letters
        if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z'))
        {
            letters++;
        }
    }
    return letters;
}

int count_words(string text)
{
    int spaces = 0;

    for (int i = 0; i < strlen(text); i++)
    {
        char c = text[i];

        // when there are spaces, it means that we have a word
        if (c == ' ')
        {
            spaces++;
        }
    }
    // we need to return words + 1 because when we have 1 space, we have 2 words
    return spaces + 1;
}

int count_sentences(string text)
{
    int sentences = 0;

    for (int i = 0; i < strlen(text); i++)
    {
        char c = text[i];

        // when encountering one of these symbols, we should consider it as a sentence
        if (c == '.' || c == '!' || c == '?')
        {
            sentences++;
        }
    }
    return sentences;
}

int calculate_grade(int letters, int words, int sentences)
{
    //calculate letters per 100 words and sentences per hundred words
    float L = (float) letters * 100 / words;
    float S = (float) sentences * 100 / words;

    //calculate the index
    int index = round(0.0588 * L - 0.296 * S - 15.8);

    return index;
}