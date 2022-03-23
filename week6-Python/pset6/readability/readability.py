from cs50 import get_string


def main():
    while True:
        text = get_string("Text: ")
        
        if text.strip() != "":
            break
    
    # Count the letters
    letters = count_letters(text)
    
    # Count the words
    words = count_words(text)
    
    # Count the sentences
    sentences = count_sentences(text)
    
    # Calculate the grade
    grade = calculate_grade(letters, words, sentences)
    
    # Print the grade
    print_grade(grade)
    

def count_words(text):
    # Separate to words into a list and then return the length of the list
    words = text.split()
    return len(words)
    

def count_letters(text):
    letters = 0
    
    # Count all the characters that are alphabetic
    for character in text:
        if character.isalpha():
            letters += 1
    
    return letters
    
    
def count_sentences(text):
    # We should consider a sentence when delimited by ! or . or ?
    sentences = 0 
    
    for character in text:
        if (character == '.') or (character == '?') or (character == '!'):
            sentences += 1
    
    return sentences
    
    
def calculate_grade(letters, words, sentences):
    L = (letters * 100 / words)
    S = (sentences * 100 / words)
    
    grade = round(0.0588 * L - 0.296 * S - 15.8)
    
    return grade
    
    
def print_grade(grade):
    # Print out he grade accordingly to the conditions below
    if grade >= 16:
        print("Grade 16+")
    
    elif grade < 1:
        print("Before Grade 1")
        
    else:
        print(f"Grade {grade}")

        
main()
