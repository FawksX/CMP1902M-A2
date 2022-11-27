# Imports the CSV File "Data" and returns it as a list
# This will retain its order (with line 1 = list[0])
# The specification does not tell us if the data is sorted or not,
# so we will assume it is sorted for the time being // TODO - Check if Sorted.
def importCsvFile():
    # Import the CSV Library in the method as we will not use it elsewhere
    import csv
    with open('data.csv', 'r') as f:
        reader = csv.reader(f)
        data = list(reader)
    # Return the Data as a list (to retain order)
    return data


# Binary Search Algorithm
# Binary Search is an O(log N) algorithm. This means that it is faster than a Linear Search
# But will require more operations to complete (with our data set being small, this is fine)
# The binary search is a "divide and conquer" algorithm. This means that it will split the data set in half
# and then search the half that the word is in. This will continue until the word is found
# (or the whole dataset is searched)
# With the method below, our index/position of the word is the variable mid
def findPositionBinarySearch(data, word):
    found = False
    low = 0
    high = len(data) - 1
    mid = high // 2
    # Iterate through the data set until the word is found or the whole data set is searched
    while low <= high and not found:
        mid = (low + high) // 2
        if data[mid][0] == word:
            found = True
        elif data[mid][0] < word:
            low = mid + 1
        else:
            high = mid - 1
    if found:
        return mid
    else:
        raise ValueError("Word not found.")


def main():
    data = importCsvFile()
    word = input("Enter a word to search for: ")
    try:
        position = findPositionBinarySearch(data, word)
        print("The word is at position: " + str(position))
    except ValueError:  # Handle the error if the word is not found
        print("Word does not exist in the data set.")
        main()


if __name__ == "__main__":
    main()
