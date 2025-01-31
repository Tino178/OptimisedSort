
# File:    smartsort.py
# Author:  John Longley
# Date:    October 2024

# Template file for Inf2-IADS (2024-25) Coursework 1, Part A:
# Implementation of hybrid Merge Sort / Insert Sort,
# with optimization for already sorted segments.


import peekqueue
from peekqueue import PeekQueue

# Global variables

comp = lambda x,y: x<=y   # comparison function used for sorting

insertSortThreshold = 10

sortedRunThreshold = 10


# TODO: Task 1. Hybrid Merge/Insert Sort

# In-place Insert Sort on A[m],...,A[n-1]:
def insertSort(A,m,n):
    if n <= m:
        return
    for i in range(m+1, n):
        key = A[i]
        j = i -1
        while j >= m and not comp(A[j], key):
            A[j + 1] = A[j]
            j -= 1
        A[j + 1] = key

#   insertSort(A,m,n)

# Merge C[m],...,C[p-1] and C[p],...,C[n-1] into D[m],...,D[n-1]

#   merge(C,D,m,p,n)
def merge(C, D, m, p, n):
    i = m
    j = p
    k = m

    while i < p and j < n:
        if C[i] is None:
            i += 1
            continue
        if C[j] is None:
            j += 1
            continue
        
        if comp(C[i], C[j]):
            D[k] = C[i]
            i += 1
        else:
            D[k] = C[j]
            j += 1
        k += 1

    while i < p:
        D[k] = C[i]
        i += 1
        k += 1

    while j < n:
        D[k] = C[j]
        j += 1
        k += 1

# Merge Sort A[m],...,A[n-1] using just B[m],...,B[n-1] as workspace,
# deferring to Insert Sort if length <= insertSortThreshold

#   greenMergeSort(A,B,m,n)
def greenMergeSort(A, B, m, n):
    if n - m <= insertSortThreshold:
        insertSort(A, m, n)
        return

    q1 = m + (n - m) // 4
    q2 = m + (n - m) // 2
    q3 = m + 3 * (n - m) // 4

    greenMergeSort(A, B, m, q1)
    greenMergeSort(A, B, q1, q2)
    greenMergeSort(A, B, q2, q3)
    greenMergeSort(A, B, q3, n)

    merge(A, B, m, q1, q2)
    merge(A, B, q2, q3, n)

    merge(B, A, m, q2, n)
    


# Provided code:

def greenMergeSortAll(A):
    B = [None] * len(A)
    greenMergeSort(A,B,0,len(A))
    return A



# TODO: Task 2. Detecting already sorted runs.
        
# Build and return queue of sorted runs of length >= sortedRunThreshold
# Queue items are pairs (i,j) where A[i],...,A[j-1] is sorted

#   allSortedRuns(A)
def allSortedRuns(A):
    Q = PeekQueue()
    n = len(A)
    i = 0
    while i < n:
        j = i + 1
        while j < n and comp(A[j-1], A[j]):
            j += 1

        if j - i >= sortedRunThreshold:
            Q.push((i, j))

        i = j

    return Q



# Test whether A[i],...,A[j-1] is sorted according to information in Q

#   isWithinRun(Q,i,j)
def isWithinRun(Q, i, j):
    # heep checking the queue until we find a segment relevant to i
    while Q.peek() is not None and Q.peek()[1] <= i:
        Q.pop() #remove any segments that end before i

    # if the next segment starts at or before i and ends after or at j
    if Q.peek() is not None:
        start, end = Q.peek()
        if start <= i and end >= j:
            return True

    # if no valid segment is found, return False
    return False

# Improvement on greenMergeSort taking advantage of sorted runs

#   smartMergeSort(A,B,Q,m,n)
def smartMergeSort(A, B, Q, m, n):
    if isWithinRun(Q, m, n):
        return
    if n - m <= insertSortThreshold:
        insertSort(A, m, n)
        return

    q1 = m + (n - m)//4
    q2 = m + (n - m) //2
    q3 = m + 3 * (n - m)//4

    smartMergeSort(A, B, Q, m, q1)
    smartMergeSort(A, B, Q, q1, q2)
    smartMergeSort(A, B, Q, q1, q3)
    smartMergeSort(A, B, Q, q3, n)

    merge(A, B, m, q1, q2)
    merge(A, B, q2, q3, n)
    merge(B, A, m, q2, n)


# Provided code:

def smartMergeSortAll(A):
    B = [None] * len(A)
    Q = allSortedRuns(A)
    smartMergeSort(A,B,Q,0,len(A))
    return A


# TODO: Task 3. Asymptotic analysis of smartMergeSortAll

# 1. Justification of O(n lg n) bound.
# In the worst case, 'smartMergeSortAll' splits the list into 4 parts,
# resulting in a recurrence relation T(n) = 4*T(n/4) + O(n) for the merging
# step. By the Master Theorem, with a = 4 (sub-problems), b = 4 (quarter-size
# divisions), and f(n) = Theta(n), we find that n^log_b(a) = n^1 matches
# f(n) = Theta(n). This satisfies Case 2 of the Master Theorem, resolving
# to T(n) = Theta(n log n). Therefore, the worst-case runtime of
# 'smartMergeSortAll' remains O(n log n), with 'allSortedRuns' and
# 'isWithinRun' both operating in O(n).

# 2. Runtime analysis for nearly-sorted inputs.
# For nearly-sorted lists, `allSortedRuns` will identify the entire list (or
# nearly the entire list) as a single sorted segment, allowing `smartMergeSort`
# to avoid most recursive calls by recognizing large pre-sorted sections.
# The `allSortedRuns` function still takes O(n) for traversal, and the merging
# operations are minimized to constant time since only one or zero small segments
# are unsorted. Thus, the recursion largely avoids further division, making the
# runtime O(n) for nearly-sorted lists. The asymptotic worst-case runtime for
# `smartMergeSortAll` on nearly-sorted lists is therefore O(n).



# Functions added for automarking purposes - please don't touch these!

def set_comp(f):
    global comp
    comp = f

def set_insertSortThreshold(n):
    global insertSortThreshold
    insertSortThreshold = n

def set_sortedRunThreshold(n):
    global sortedRunThreshold
    sortedRunThreshold = n

def set_insertSort(f):
    global insertSort
    insertSort = f


# End of file

