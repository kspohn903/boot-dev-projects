# Python program for implementation of Insertion Sort

# Function to sort array using insertion sort
def quick_sort(arr, low=1, high=None):
    if high is None:
       high = len(arr) - 1 
    for i in range(low, high+1, 1):
        key = arr[i]
        j = i - 1

        # Move elements of arr[0..i-1], that are
        # greater than key, to one position ahead
        # of their current position
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

# A utility function to print array of size n
def printArray(arr):
    for i in range(len(arr)):
        print(arr[i], end=" ")
    print()

# Driver method
