// Implements a dictionary's functionality

#include <stdbool.h>
#include "dictionary.h"
#include <strings.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>



// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table (takes as much as the zize of an int)
const unsigned int N = 65536;

// Hash table
node *table[N];

// Word count
int word_count = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    int length = strlen(word);
    char copy[length + 1]; 
    copy[length] = '\0'; 


    for (int i = 0; i < length; i++) 
    {
        copy[i] = tolower(word[i]);
    }


    unsigned int hashcode = hash(copy);
       
    node *tmp = table[hashcode]; 
       
    if (tmp == NULL) 
    {
        return false;
    }

    while (tmp != NULL) 
    {
        if (strcasecmp(tmp->word, copy) == 0) 
        {
            return true; 
        }

        tmp = tmp->next; 
    }

    return false; 
}

// taken from http://www.cse.yorku.ca/~oz/hash.html
unsigned int hash(const char *word)
{
    unsigned long hash = 5381;

    int c = *word;

    while (c == *word++)
    {
        hash = ((hash << 5) + hash) + c; /* hash * 33 + c */
    }
    return hash % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    FILE *file = fopen(dictionary, "r");
    
    if (file == NULL)
    {
        fclose(file);
        return false;
    }
    
    char word[LENGTH + 1];
    
    while (fscanf(file, "%s", word) != EOF)
    {
        node *new_node = malloc(sizeof(node));
        
        if (new_node == NULL)
        {
            unload();
            return false;
        }
        
        strcpy(new_node->word, word);
        
        new_node->next = NULL;
        
        unsigned int hash_index = hash(word);
        
        new_node->next = table[hash_index];
        
        table[hash_index] = new_node;
        
        word_count++;
    }
    
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // Just return the count that was already done in the load function
    return word_count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
    
        node *tmp = table[i]; 
    
        while (tmp != NULL) 
        {
            node *cursor = tmp; 
            tmp = tmp->next; 
            free(cursor); 
        }
    }

    return true;
    
}