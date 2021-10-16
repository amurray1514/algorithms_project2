import random as rnd
import time
from copy import deepcopy as dcopy

"""
Base class for all sorting algorithms.

@author: Josh Hicks
"""
class Sort:
    def __init__(self):
        pass

    def sort(self, args):
        pass

    def isSorted(self, args):
        for i in range(len(args) - 1):
            if args[i] > args[i + 1]:
                return False
        return True

    def testSort(self, args):
        t1 = time.perf_counter()
        try:
            args = self.sort(args)
        except RecursionError:
            return -2  # error return
        t2 = time.perf_counter()
        if not self.isSorted(args):
            return -1  # "not sorted" return
        return t2 - t1


"""
Implementation of merge sort.

@author: Josh Hicks
"""
class MergeSort(Sort):
    def sort(self, args):
        if(len(args) <= 1):
            return args
        middle = len(args) // 2
        left = args[:middle]
        right = args[middle:]
        left = self.sort(left)
        right = self.sort(right)
        return list(self.merge(left, right))

    def merge(self, left, right):
        result = []
        left_idx = 0
        right_idx = 0
        while left_idx < len(left) and right_idx < len(right):
            if left[left_idx] < right[right_idx]:
                result.append(left[left_idx])
                left_idx += 1
            else:
                result.append(right[right_idx])
                right_idx += 1
        if left_idx < len(left):
            result.extend(left[left_idx:])
        if right_idx < len(right):
            result.extend(right[right_idx:])
        return result


"""
Implementation of quick sort.

@author: Josh Hicks
"""
class QuickSort(Sort):
    def partition(self, array, begin, end):
        pivotIdx = begin
        for i in range(begin + 1, end + 1):
            if array[i] <= array[begin]:
                pivotIdx += 1
                array[i], array[pivotIdx] = array[pivotIdx], array[i]
        array[pivotIdx], array[begin] = array[begin], array[pivotIdx]
        return pivotIdx

    def quick_sort_recursion(self, array, begin, end):
        if begin >= end:
            return
        pivotIdx = self.partition(array, begin, end)
        self.quick_sort_recursion(array, begin, pivotIdx - 1)
        self.quick_sort_recursion(array, pivotIdx + 1, end)

    def sort(self, args):
        self.quick_sort_recursion(args, 0, len(args) - 1)
        return args


"""
Implementation of bubble sort.

@author: Josh Hicks
"""
class BubbleSort(Sort):
    def sort(self, args):
        swapped = True
        while swapped:
            swapped = False
            for i in range(len(args) - 1):
                if args[i] > args[i + 1]:
                    args[i], args[i + 1] = args[i + 1], args[i]
                    swapped = True
        return args


"""
Implementation of insertion sort.

@author: Levi Lewis
"""
class InsertionSort(Sort):
    def sort(self, args):
        for i in range(len(args)):
            index = i
            while index > 0 and args[index - 1] > args[i]:
                index -= 1
            args[i], args[index] = args[index], args[i]
        return args


"""
"Shatters" the given array by repeatedly splitting it in two,
"shattering" the two halves, and returning an array consisting of
alternating elements from the left half and the right half.
"Shattering" a sorted array should result in a worst-case array
for merge sort.

@author: Archer Murray
"""
def shatter(arr):
    if len(arr) == 1:
        return arr
    middle = len(arr) // 2
    left = shatter(arr[:middle])
    right = shatter(arr[middle:])
    ret = list()
    for i in range(middle):
        ret.append(right[i])
        ret.append(left[i])
    if len(arr) % 2 == 1:
        # Array length is odd, right has an extra element
        ret.append(right[middle])
    return ret


"""
Returns a 5-tuple of arrays of the given size.
The first array is random.
The second array is the first array sorted.
The third array is the second array reversed.
The fourth array is the second array "shattered".
The fifth array is the fourth array reversed.

@author: Archer Murray
"""
def getArraySuite(size):
    arr1 = [rnd.randrange(size) for i in range(size)]
    arr2 = dcopy(arr1)
    arr2.sort()
    arr3 = dcopy(arr2)
    arr3.reverse()
    arr4 = shatter(dcopy(arr2))
    arr5 = dcopy(arr4)
    arr5.reverse()
    return (arr1, arr2, arr3, arr4, arr5)


"""
Testing routine (work in progress).

@author: Archer Murray
"""
def integrationTest():
    with open('results.txt', 'w') as f:
        mst = MergeSort()
        qst = QuickSort()
        bst = BubbleSort()
        ist = InsertionSort()
        sz = 50
        out_str = '{:<30}'.format('Sort')
        out_str += '{:>10}'.format('Random')
        out_str += '{:>10}'.format('Sorted')
        out_str += '{:>10}'.format('Reversed')
        out_str += '{:>10}'.format('Shattered')
        out_str += '{:>10}'.format('Rev-Shat')
        f.write(out_str + '\n')
        f.write('-' * 80 + '\n')
        while sz < 2000:
            arrs = getArraySuite(sz)
            out_str = '{:<30}'.format('Merge Sort, size ' + str(sz))
            for i in range(5):
                out_str += '{0:>10f}'.format(mst.testSort(arrs[i]))
            f.write(out_str + '\n')
            out_str = '{:<30}'.format('Quick Sort, size ' + str(sz))
            for i in range(5):
                out_str += '{0:>10f}'.format(qst.testSort(arrs[i]))
            f.write(out_str + '\n')
            out_str = '{:<30}'.format('Bubble Sort, size ' + str(sz))
            for i in range(5):
                out_str += '{0:>10f}'.format(bst.testSort(arrs[i]))
            f.write(out_str + '\n')
            out_str = '{:<30}'.format('Insertion Sort, size ' + str(sz))
            for i in range(5):
                out_str += '{0:>10f}'.format(ist.testSort(arrs[i]))
            f.write(out_str + '\n')
            sz *= 2


if __name__ == '__main__':
    integrationTest()