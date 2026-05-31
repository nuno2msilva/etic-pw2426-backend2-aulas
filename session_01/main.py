# --- Tutorial Example: Linear Search ---
# O(n): Runtime grows in a linear fashion with list size

def linear_search(list, target):
    for item in list:
        if item == target:
            return True
    return False


# --- Problem: Recursive Factorial (O(n)) ---
# O(n): the function is called exactly n+1 times for input n

def factorial(n):
    if n == 0:          # base case: 0! = 1
        return 1
    return n * factorial(n - 1)


# --- Challenge: Bubble Sort (Optimized, with early exit if sorted True) ---
# Worst case O(n²), but O(n) when the list is already sorted
# Flag "already_swapped" detects a fully sorted pass and exits early

def bubble_sort(items):
    n = len(items) # saves list length as n
    for i in range(n - 1): # 
        processed = False 
        for j in range(n - 1 - i): # shrink inner range each pass
            if items[j] > items[j + 1]:
                placeholder = items[j] # save
                items[j] = items[j + 1] # overwrite
                items[j + 1] = placeholder # swap
                processed = True
        if not processed:
            break # exits early if no swaps happened
    return items # returns sorted list


def main():
    
    # Tutorial: Linear Search
    numbers_for_linear_search = [3, 1, 4, 1, 5, 9, 2, 6]
    
    print("Tutorial: Linear Search")
    print("Linear search (5):", linear_search(numbers_for_linear_search, 5))   # True
    print("Linear search (7):", linear_search(numbers_for_linear_search, 7))   # False

    # Problem: Recursive Factorial
    print("Problem: Recursive Factorial")
    
    # From the defined number, it diminishes by 1 until base reaches 0
    # When n=0, returns 1, and then multiplies back up the call stack to give the final result
    # For example, factorial(5) computes as:
    # 5*4*3*2*1 = 120
    
    print("5! =", factorial(5))     # 120
    print("0! =", factorial(0))     # 1

    # Challenge: Bubble Sort (Optimized)
    unsorted = [5, 3, 8, 1, 2]
    sorted = [1, 2, 3, 4, 5]
    
    print("Challenge: Bubble Sort (Optimized)")
    
    print("Unsorted:", bubble_sort(unsorted)) # [1, 2, 3, 5, 8]
    print("Sorted:", bubble_sort(sorted))  # SKIP


if __name__ == "__main__":
    main()
