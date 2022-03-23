#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Calculate average of red, blue and green
            int average = round((image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / (float) 3);

            image[i][j].rgbtRed = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtBlue = average;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int Sred = round(image[i][j].rgbtRed * 0.393 + image[i][j].rgbtGreen * 0.769 + image[i][j].rgbtBlue * 0.189);
            int Sgreen = round(image[i][j].rgbtRed * 0.349 + image[i][j].rgbtGreen * 0.686 + image[i][j].rgbtBlue * 0.168);
            int Sblue = round(image[i][j].rgbtRed * 0.272 + image[i][j].rgbtGreen * 0.534 + image[i][j].rgbtBlue * 0.131);

            // Image cannot have color number higher than 255
            if (Sred > 255)
            {
                Sred = 255;
            }

            if (Sgreen > 255)
            {
                Sgreen = 255;
            }

            if (Sblue > 255)
            {
                Sblue = 255;
            }

            image[i][j].rgbtRed = Sred;
            image[i][j].rgbtGreen = Sgreen;
            image[i][j].rgbtBlue = Sblue;
        }
    }

    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        // Case for even width
        if (width % 2 == 0)
        {
            for (int j = 0; j < (width / 2); j++)
            {
                RGBTRIPLE temp = image[i][j];

                image[i][j] = image[i][(width - 1) - j];
                image[i][(width - 1) - j] = temp;
            }
        }

        // Case for odd width
        else
        {
            for (int j = 0; j < ((width - 1) / 2); j++)
            {
                RGBTRIPLE temp = image[i][j];

                image[i][j] = image[i][(width - 1) - j];
                image[i][(width - 1) - j] = temp;
            }
        }
    }

    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Create new array to record the new pixel colors
    RGBTRIPLE copy[height][width];

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int avgRed, avgGreen, avgBlue;

            // Top left corner case
            if (i == 0 && j == 0)
            {
                avgRed = round((image[0][0].rgbtRed + image[0][1].rgbtRed + image[1][0].rgbtRed + image[1][1].rgbtRed) / (float) 4);
                avgGreen = round((image[0][0].rgbtGreen + image[0][1].rgbtGreen + image[1][0].rgbtGreen + image[1][1].rgbtGreen) / (float) 4);
                avgBlue = round((image[0][0].rgbtBlue + image[0][1].rgbtBlue + image[1][0].rgbtBlue + image[1][1].rgbtBlue) / (float) 4);
            }

            // First row case
            else if (i == 0 && j != (width - 1))
            {
                avgRed = round((image[0][j - 1].rgbtRed + image[0][j].rgbtRed + image[0][j + 1].rgbtRed + image[1][j - 1].rgbtRed + 
                                image[1][j].rgbtRed + image[1][j + 1].rgbtRed) / (float) 6);
                
                avgGreen = round((image[0][j - 1].rgbtGreen + image[0][j].rgbtGreen + image[0][j + 1].rgbtGreen + image[1][j - 1].rgbtGreen + 
                                  image[1][j].rgbtGreen + image[1][j + 1].rgbtGreen) / (float) 6);
                
                avgBlue = round((image[0][j - 1].rgbtBlue + image[0][j].rgbtBlue + image[0][j + 1].rgbtBlue + image[1][j - 1].rgbtBlue + 
                                 image[1][j].rgbtBlue + image[1][j + 1].rgbtBlue) / (float) 6);
            }

            // Top right corner case
            else if (i == 0 && j == (width - 1))
            {
                avgRed = round((image[0][j - 1].rgbtRed + image[0][j].rgbtRed + image[1][j - 1].rgbtRed + image[1][j].rgbtRed) / (float) 4);
                
                avgGreen = round((image[0][j - 1].rgbtGreen + image[0][j].rgbtGreen + image[1][j - 1].rgbtGreen + image[1][j].rgbtGreen) / 
                                 (float) 4);
                
                avgBlue = round((image[0][j - 1].rgbtBlue + image[0][j].rgbtBlue + image[1][j - 1].rgbtBlue + image[1][j].rgbtBlue) / (float) 4);
            }

            // First column case
            else if (i != (height - 1) && j == 0)
            {
                avgRed = round((image[i - 1][0].rgbtRed + image[i][0].rgbtRed + image[i + 1][0].rgbtRed + image[i - 1][1].rgbtRed + 
                                image[i][1].rgbtRed + image[i + 1][1].rgbtRed) / (float) 6);
                
                avgGreen = round((image[i - 1][0].rgbtGreen + image[i][0].rgbtGreen + image[i + 1][0].rgbtGreen + image[i - 1][1].rgbtGreen + 
                                  image[i][1].rgbtGreen + image[i + 1][1].rgbtGreen) / (float) 6);
                
                avgBlue = round((image[i - 1][0].rgbtBlue + image[i][0].rgbtBlue + image[i + 1][0].rgbtBlue + image[i - 1][1].rgbtBlue + 
                                 image[i][1].rgbtBlue + image[i + 1][1].rgbtBlue) / (float) 6);
            }

            // Bottom left corner case
            else if (i == (height - 1) && j == 0)
            {
                avgRed = round((image[i - 1][0].rgbtRed + image[i][0].rgbtRed + image[i - 1][1].rgbtRed + image[i][1].rgbtRed) / (float) 4);
                
                avgGreen = round((image[i - 1][0].rgbtGreen + image[i][0].rgbtGreen + image[i - 1][1].rgbtGreen + image[i][1].rgbtGreen) / 
                                 (float) 4);
                
                avgBlue = round((image[i - 1][0].rgbtBlue + image[i][0].rgbtBlue + image[i - 1][1].rgbtBlue + image[i][1].rgbtBlue) / (float) 4);
            }

            // Last column case
            else if (i != (height - 1) && j == (width - 1))
            {
                avgRed = round((image[i - 1][j].rgbtRed + image[i][j].rgbtRed + image[i + 1][j].rgbtRed + image[i - 1][j - 1].rgbtRed + 
                                image[i][j - 1].rgbtRed + image[i + 1][j - 1].rgbtRed) / (float) 6);
                
                avgGreen = round((image[i - 1][j].rgbtGreen + image[i][j].rgbtGreen + image[i + 1][j].rgbtGreen + image[i - 1][j - 1].rgbtGreen + 
                                  image[i][j - 1].rgbtGreen + image[i + 1][j - 1].rgbtGreen) / (float) 6);
                
                avgBlue = round((image[i - 1][j].rgbtBlue + image[i][j].rgbtBlue + image[i + 1][j].rgbtBlue + image[i - 1][j - 1].rgbtBlue + 
                                 image[i][j - 1].rgbtBlue + image[i + 1][j - 1].rgbtBlue) / (float) 6);
            }

            // Last row case
            else if (i == (height - 1) && j != (width - 1))
            {
                avgRed = round((image[i][j - 1].rgbtRed + image[i][j].rgbtRed + image[i][j + 1].rgbtRed + image[i - 1][j - 1].rgbtRed + 
                                image[i - 1][j].rgbtRed + image[i - 1][j + 1].rgbtRed) / (float) 6);
                
                avgGreen = round((image[i][j - 1].rgbtGreen + image[i][j].rgbtGreen + image[i][j + 1].rgbtGreen + image[i - 1][j - 1].rgbtGreen + 
                                  image[i - 1][j].rgbtGreen + image[i - 1][j + 1].rgbtGreen) / (float) 6);
                
                avgBlue = round((image[i][j - 1].rgbtBlue + image[i][j].rgbtBlue + image[i][j + 1].rgbtBlue + image[i - 1][j - 1].rgbtBlue + 
                                 image[i - 1][j].rgbtBlue + image[i - 1][j + 1].rgbtBlue) / (float) 6);
            }

            // Bottom right corner case
            else if (i == (height - 1) && j == (width - 1))
            {
                avgRed = round((image[i - 1][j].rgbtRed + image[i][j].rgbtRed + image[i - 1][j - 1].rgbtRed + image[i][j - 1].rgbtRed) / 
                               (float) 4);
                
                avgGreen = round((image[i - 1][j].rgbtGreen + image[i][j].rgbtGreen + image[i - 1][j - 1].rgbtGreen + image[i][j - 1].rgbtGreen) / 
                                 (float) 4);
                
                avgBlue = round((image[i - 1][j].rgbtBlue + image[i][j].rgbtBlue + image[i - 1][j - 1].rgbtBlue + image[i][j - 1].rgbtBlue) / 
                                (float) 4);
            }

            // All the other pixels
            else
            {
                avgRed = round((image[i - 1][j - 1].rgbtRed + image[i - 1][j].rgbtRed + image[i - 1][j + 1].rgbtRed + 
                                image[i][j - 1].rgbtRed + 
                                image[i][j].rgbtRed + image[i][j + 1].rgbtRed + image[i + 1][j - 1].rgbtRed + image[i + 1][j].rgbtRed + 
                                image[i + 1][j + 1].rgbtRed) / (float) 9);
                
                avgGreen = round((image[i - 1][j - 1].rgbtGreen + image[i - 1][j].rgbtGreen + image[i - 1][j + 1].rgbtGreen + 
                                  image[i][j - 1].rgbtGreen + 
                                  image[i][j].rgbtGreen + image[i][j + 1].rgbtGreen + image[i + 1][j - 1].rgbtGreen + image[i + 1][j].rgbtGreen + 
                                  image[i + 1][j + 1].rgbtGreen) / (float) 9);
                
                avgBlue = round((image[i - 1][j - 1].rgbtBlue + image[i - 1][j].rgbtBlue + image[i - 1][j + 1].rgbtBlue + image[i][j - 1].rgbtBlue + 
                                 image[i][j].rgbtBlue + image[i][j + 1].rgbtBlue + image[i + 1][j - 1].rgbtBlue + image[i + 1][j].rgbtBlue + 
                                 image[i + 1][j + 1].rgbtBlue) / (float) 9);
            }

            copy[i][j].rgbtRed = avgRed;
            copy[i][j].rgbtGreen = avgGreen;
            copy[i][j].rgbtBlue = avgBlue;
        }
    }

    // Paste the copy array into the image array
    for (int i  = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = copy[i][j];
        }
    }

    return;
}
