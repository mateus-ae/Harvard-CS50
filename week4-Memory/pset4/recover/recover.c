#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
 
typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    // Check command line arguments.
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }
    
    // Open input file. if it fails to open, return error message.
    FILE *input = fopen(argv[1], "r");
    
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }
    
    int i = 0;
    
    FILE *output = NULL;
    
    bool found_jpg = false;
    
    // Start reading the input file
    BYTE buffer[512];
    
    // Read the file's 512 bytes long block until it reaches the end
    while (fread(buffer, sizeof(BYTE), 512, input))
    {
        
        // Identify if the block starts a new jpg file
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // Close the previous file, if there is one
            if (i != 0)
            {
                fclose(output);
            }
            
            // Create a new file in the format of ###.jpg
            char filename[8];
        
            sprintf(filename, "%03i.jpg", i);
        
            // Open the file
            output = fopen(filename, "w");
        
            if (output == NULL)
            {
                printf("Could not open file.\n");
                return 1;
            }
            
            found_jpg = true;
            
            i++;
        }
        
        // Keep writing to this file until the program finds a new jpg
        if (found_jpg)
        {
            fwrite(buffer, sizeof(BYTE), 512, output);
        }
        
    }
    
    fclose(input);
    
    return 0;
}
