from sys import argv
import csv


def main():
    # Check if command line arguments requirementes are satisfied
    check_usage()
    
    # Load the csv file into memory
    people = load_csv(argv[1])
    
    # Load the txt file into memory
    sequence = load_txt(argv[2])
    
    # Count maximum STR repititions for each STR:
    str_counts = count_str(sequence)
    
    # Compare the STR counts to the people to find any match
    result = check_matches(people, str_counts)
    
    print(result)
    
    
def check_usage():
    if len(argv) != 3:
        print("Usage: python dna.py database.csv sequence.txt")


def load_csv(file):
    with open(file, "r") as csv_file:
        reader = csv.DictReader(csv_file)
        # Create a list of the people in the csv file
        people = []
        
        # Load the people list with each person's name and STR's in a dictionary structure
        for row in reader:
            people.append(row)
    
    return people


def load_txt(file):
    with open(file, "r") as txt_file:
        sequence = []
        
        sequence.append(txt_file.read().strip())
        
    return sequence


def count_str(sequence):
    # Possible STR's are AGATC,TTTTTTCT,AATG,TCTAG,GATA,TATC,GAAA,TCTG
    possible_str = ['AGATC', 'TTTTTTCT', 'AATG', 'TCTAG', 'GATA', 'TATC', 'GAAA', 'TCTG']
    counts = []
    
    # Iterate through the possible_str list
    for str_sequence in possible_str:
        # Extract the sequence string
        new_sequence = sequence[0]
        # Create a list that will contain the current STR counts
        counter_list = []
        
        # Start the count
        while True:
            counter = 0
        
            # Check if the current STR is in the sequence
            if str_sequence in new_sequence:
                # Get a new sequence starting from the found STR
                index = new_sequence.index(str_sequence)
                counter += 1
                # Remove the first occurence of the found STR from the sequence
                new_sequence = new_sequence[(index + len(str_sequence)):]
                
                # Check the next genes of the sequence matches the STR. Repeat it until it's not
                while True:
                    if new_sequence[0: len(str_sequence)] == str_sequence:
                        counter += 1
                        new_sequence = new_sequence[len(str_sequence):]
                        
                    # Append the counter value to the counter list when there are no more STR's found in that sequence
                    else:
                        counter_list.append(counter)
                        break
            
            else:
                break
        
        # Find the maximum count from the counter list if any count was found
        if counter_list != []:
            counter = max(counter_list)
        else:
            counter = 0
        
        # Start a dictionary for each STR and append it to the counts list
        str_dictionary = {f"{str_sequence}": counter}
        
        counts.append(str_dictionary)
        
    return counts
    
    
def check_matches(people, str_counts):
    # Get a list with the STR's found in the sequence from the str_counts list
    str_counts_list = list()
    
    for str_count in str_counts: 
        str_counts_list.extend(list(str_count.keys()))
    
    # Check if there's a match for each person from the csv file
    for person in people:
        matches = 0
        # Get a list with the registered STR's from that person
        person_str_list = list(person.keys())
        person_str_list.remove('name')
        person_str_size = len(person_str_list)
        
        # For each STR in this list, check if it's also in the the str_counts_list and if so, get this list's index for that STR
        for str_sequence in person_str_list:
            if str_sequence in str_counts_list:
                str_counts_list_index = str_counts_list.index(str_sequence)
                
                # Get the count value from the str_counts list for this particular STR
                str_count_value = str_counts[str_counts_list_index][str_sequence]
                
                # Compare the count value above with the STR value for this person from the people's list of dictionaries
                if int(person[str_sequence]) == str_count_value:
                    matches += 1
        
        # If all the STR count values for this person matches the counts for str_counts list, then we've found a match 
        if matches == person_str_size:
            return person['name']
        
    # If no matches were found, return so
    return 'No match'


main()