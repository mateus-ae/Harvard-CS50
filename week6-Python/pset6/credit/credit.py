from cs50 import get_int


def main():
    # Prompt the user for the card number
    card = get_int("Number: ")
    card = str(card)
    
    # Validate the length of the card
    if validate_length(card):
        # if length is ok, apply Luhn's algorithm
        if validate_card(card):
            # Detect the type of the card
            brand_of_card = type_of_card(card)
            # print the type of the card
            print(brand_of_card)
        
    else:
        # If it's not a valid card, print invalid
        print("INVALID")


def validate_length(card):
    # return true if the length is one of the below
    return (len(card) == 13) or (15 <= len(card) <= 16)


def validate_card(card):
    # separate the digits for the Luhn's calculation
    first_digits = card[-2::-2]
    second_digits = card[-1::-2]
    
    first_digits_int = []
    second_digits_int = []
    
    # Calculate the first part of the algorithm
    for digit in first_digits:
        digit = int(digit) * 2
        
        if len(str(digit)) > 1:
            digit = str(digit)
            
            first_digits_int.append(int(digit[0]))
            first_digits_int.append(int(digit[1]))
        
        else:
            first_digits_int.append(digit)
    
    # Calculate the second part of the algorithm
    for digit in second_digits:
        digit = int(digit)
        second_digits_int.append(digit)
    
    # Add the digits and check if it's divisible by 10
    sum_digits = str(sum(first_digits_int) + sum(second_digits_int))
    
    if sum_digits[-1] == '0':
        return True
    
    else:
        return False


def type_of_card(card):
    
    amex_numbers = ['34', '37']
    master_numbers = ['51', '52', '53', '54', '55']
    visa_numbers = ['4']
    
    # Verify the type of the card
    if card[0:2] in amex_numbers:
        return f"AMEX"
        
    elif card[0:2] in master_numbers:
        return f"MASTERCARD"
        
    elif card[0] in visa_numbers:
        return f"VISA"
    
    else:
        return f"INVALID"


main()