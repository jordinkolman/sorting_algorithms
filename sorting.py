from random import randint
from timeit import repeat
from statistics import median

def run_sorting_algorithm(algorithm, array):
    # Set up context and algorithm call using supplied array
    
    # Only import algorithm function if its not the built-in sorted()
    setup_code = f"from __main__ import {algorithm}" \
        if algorithm != "sorted" else ""
        
    stmt = f"{algorithm}({array})"
    
    # Executed code 10 different times and return time in seconds execution took
    times = repeat(setup=setup_code, stmt=stmt, repeat=3, number=10)
    
    # Display name of algorithm and minimum time it took to run
    print(f"Algorithm: {algorithm}. Minimum execution time: {min(times)}")
    
def bubble_sort_basic(array):
    n = len(array)
    
    for i in range(n):
        # Look at each item 1 by 1, comparing with adjacent value. With each iteration,
        # portion of array you are looking at shrinks as items at end become sorted
        for j in range(n - i - 1):
            if array[j] > array[j + 1]:
                # if item you're looking at is greater than its adjacent value, swap
                array[j], array[j+1] = array[j + 1], array[j]

    return array
    

def bubble_sort(array):
    n = len(array)
    
    for i in range(n):
        # Create flag to allow function to terminate early if nothing left to sort
        already_sorted = True
        
        # Look at each item 1 by 1, comparing with adjacent value. With each iteration,
        # portion of array you are looking at shrinks as items at end become sorted
        for j in range(n - i - 1):
            if array[j] > array[j + 1]:
                # if item you're looking at is greater than its adjacent value, swap
                array[j], array[j+1] = array[j + 1], array[j]
                
                #since you had to swap, set already_sorted to "False" so algorithm doesn't terminate prematurely
                already_sorted = False
            
        # if no swaps during last iteration, array sorted. terminate algorithm
        if already_sorted:
            break
        
    return array
    

def insertion_sort(array, left=0, right=None):
    if right is None:
        right = len(array) - 1
    # Loop from second element of array until last elmement
    for i in range(left + 1, right + 1):
        # This is the element we want to position in its correct place
        key_item = array[i]
        
        # Initialize variable that will be used to find correct position of key_item
        j = i - 1
        
        # Run through list of items (left portion of array) and find correct position
        # Only do if key_item is smaller than adjacent values
        while j >= left and array[j] > key_item:
            # Shift value one position to the left and reposition j to point to next element (from right to left)
            array[j + 1] = array[j]
            j -= 1
            
        # When you finish shifting the elements, you can position key_item in its correct location
        array[j + 1] = key_item
        
    return array


def merge(left, right):
    # If first array is empty, nothing needs merged. Return second array as result
    if len(left) == 0:
        return right
    
    # Ditto for the second array, return first array
    if len(right) == 0:
        return left
    
    result = []
    index_left = index_right = 0
    
    # Iterate through both arrays until all emements are in result
    while len(result) < len(left) + len(right):
        # Elements need to be sorted to be added to result, so decide whether to get next element
        # from first or second array
        if left[index_left] <= right[index_right]:
            result.append(left[index_left])
            index_left += 1
        else:
            result.append(right[index_right])
            index_right += 1
    
        # If you reach the end of either array, add remaining elements from other array to result and break
        if index_right == len(right):
            result += left[index_left:]
            break
        
        if index_left == len(left):
            result += right[index_right:]
            break
        
    return result
        
        
def merge_sort(array):
    # If input array contains less than 2 elements, return as result (end condition for recursion)
    if len(array) < 2:
        return array
    
    midpoint = len(array)//2
    
    # Sort array by recursively splitting input into 2 halves, sorting each half, and merging
    return merge(
        left=merge_sort(array[:midpoint]),
        right=merge_sort(array[midpoint:])
    )
    
    
def quicksort(array):
    # If input array contains less than 2 elements, return as result of function
    if len(array) < 2:
        return array
    
    low, same, high = [], [], []
    
    #Select `pivot` element randomly
    pivot = array[randint(0, len(array) - 1)]
    
    for item in array:
        # Elements smaller than pivot go to low
        # Elements larger than pivot go to high
        # Elements == pivot go to same
        if item < pivot:
            low.append(item)
        elif item > pivot:
            high.append(item)
        else:
            same.append(item)
    
    # final result combines sorted 'low' list with 'same' and sorted 'high' list
    
    return quicksort(low) + same + quicksort(high)


def quicksort_optimized(array):
    if len(array) <= 1:
        return array
    
    # pivot point is selected using median of first, middle, and last element (median of three method)
    pivot = median([array[0], array[len(array)//2], array[-1]])
        
    # items are added into lists using generator statements
    low, same, high = (
        [i for i in array if i < pivot],
        [i for i in array if i == pivot],
        [i for i in array if i > pivot]
    )
    
    return quicksort(low) + same + quicksort(high)


def timsort(array):
    min_run = 32
    n = len(array)
    
    # Start by slicing and sorting small portions of input array
    # Size of slices is defined by min_run size
    for i in range(0, n, min_run):
        insertion_sort(array, i, min((i + min_run - 1), n - 1))
        
    # start merging sorted slices
    # start from min_run, doubling the size on each iteration until surpassing array length
    size = min_run
    while size < n:
        # Determine arrays that will be merged
        for start in range(0, n, size * 2):
            # Compute midpoint (where first array ends and second starts) and endpoint of second array
            midpoint = start + size - 1
            end = min((start + size * 2 - 1), (n-1))
            
            # Merge 2 subarrays
            # Left should go from start to midpoint + 1
            # Right should go from midpoint + 1 to end + 1
            merged_array = merge(
                left=array[start:midpoint + 1],
                right=array[midpoint + 1:end + 1]
            )
            
            # Put merged array back into your array
            array[start:start + len(merged_array)] = merged_array
            
        # Each iteration should double size of arrays
        size *= 2
        
    return array

        
ARRAY_LENGTH = 10000

if __name__ == '__main__':
    # Generate an array of 'ARRAY_LENGTH' items consiting of random integers 0 - 999
    array = [randint(0, 1000) for _ in range(ARRAY_LENGTH)]
    array_two = [i for i in range(ARRAY_LENGTH)]
    array_three = (
        [i for i in range(3333)]
        + [i for i in range(3333)]
        + [i for i in range(3334)]
        )
    
    # Call function using name of sorting algorithm and array you just created
    
    #Built-In sorted() Algorithm
    run_sorting_algorithm(algorithm="sorted", array=array)
    
    #Bubble Sort without Final Pass Optimization
    #run_sorting_algorithm(algorithm="bubble_sort_basic", array=array)
    
    #Bubble Sort with Final Pass Optimization
    #run_sorting_algorithm(algorithm='bubble_sort', array=array)
    
    #Insertion Sort
    run_sorting_algorithm(algorithm='insertion_sort', array=array)
    
    #Merge Sort
    run_sorting_algorithm(algorithm='merge_sort', array=array)
    
    #Merge Sort on an already sorted array
    print('sorted array')
    run_sorting_algorithm(algorithm='merge_sort', array=array_two)

    #Quicksort
    run_sorting_algorithm(algorithm='quicksort', array=array)
    
    #Quicksort on an already sorted array
    print('sorted array')
    run_sorting_algorithm(algorithm='quicksort', array=array_two)
    
    #Quicksort on a partially sorted array
    print('partially sorted array')
    run_sorting_algorithm(algorithm='quicksort', array=array_three)
    
    #Optimized Quicksort with Median-of-Three Pivot and Generated Sublists
    run_sorting_algorithm(algorithm='quicksort_optimized', array=array)
    
    #Optimized Quicksort on an already sorted array
    print('sorted array')
    run_sorting_algorithm(algorithm='quicksort_optimized', array=array_two)
    
    #Optimized Quicksort on a partially sorted array
    print('partially sorted array')
    run_sorting_algorithm(algorithm='quicksort_optimized', array=array_three)
    
    #Timsort
    run_sorting_algorithm(algorithm='timsort', array=array)
    
    #Timsort on an already sorted array
    print('sorted array')
    run_sorting_algorithm(algorithm='timsort', array=array_two)
    
    #Timsort on a partially sorted array
    print('partially sorted array')
    run_sorting_algorithm(algorithm='timsort', array=array_three)