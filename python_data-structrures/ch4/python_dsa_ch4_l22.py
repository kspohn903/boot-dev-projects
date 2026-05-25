# Python program for implementation of Selection
# Sort

def selection_sort(arr, left = 0, right = None):
    n = len(arr)
    if(right is None):
       right = n-1

    for i in range(left, right+1, 1):
        # Assume the current position holds
        # the minimum element
        min_idx = i
        
        # Iterate through the unsorted portion
        # to find the actual minimum
        for j in range(i+1, n, 1):
            if arr[j] < arr[min_idx]:
               # Update min_idx if a smaller element is found
               min_idx = j
        
        # Move minimum element to its
        # correct position
        arr[i], arr[min_idx] = arr[min_idx], arr[i] # swap(arr, i, min_idx)
    return arr

def print_array(arr):
    for val in arr:
        print(val, end=" ")
    print()
