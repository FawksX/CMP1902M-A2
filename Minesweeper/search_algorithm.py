#
# Binary Search Algorithm - V1.0
# Author: Oliver Whitehead (26345141)
# Date: 22/12/2022
#

# Imports the words from words.txt into a file
# We ensure that the newline character is removed from each word so that it can be directly matched
# with the users input
def importWords():
    # Read the file and store the words in a list
    with open("words.txt", "r") as file:
        data = file.readlines()

    for x in range(len(data)):
        data[x] = data[x].replace("\n", "") # remove newline from the words so we can match with user input

    return data


# A Method which performs a binary search on a list and return it's position
# Binary search is a Divide+Conquer algorithm, so we split the list in half in each iteration
def findPositionBinarySearch(data, word):
    # The first index we will check is the whole list, so we start at 0
    # If word >= middle then this is moved to middle +1 to search the right hand side of the list
    first = 0
    # The last index, if word <= middle then this gets moved to middle - 1
    last = len(data) - 1
    found = False
    # While the list is >= 1 element in size and is not found we will iterate
    while first <= last and not found:
        middle = (first + last) // 2
        # We call .lower() here to ensure that the words are not case sensitive.
        if data[middle].lower() == word.lower():
            found = True
        else:
            # If the word is in the left hand side of the data, move the last index to the middle-1
            # (as the middle was already checked)
            # If not, perform the reverse
            if word.lower() < data[middle].lower():
                last = middle - 1
            else:
                first = middle + 1
    # At this point, the word has either been found or the whole list has been searched, so return the position or
    # Raise an error.
    if found:
        return middle
    else:
        raise ValueError("Word not found")


# Main Logic for the program. We will begin by importing the words from the text file and then attempting
# to find the position of the word the user inputs.
# If an error is thrown, that means the word is not in the list, so we will print an error message and
# restart the algorithm.
def main():
    data = importWords()
    word = input("Enter a word to search for: ")
    try:
        position = findPositionBinarySearch(data, word)
        print("The word is at position: " + str(position+1)) # Files start at position 1 whereas lists are position 0
    except ValueError:  # Handle the error if the word is not found
        print("The word is not in the list of words supplied")
        main()

if __name__ == "__main__":
    main()
