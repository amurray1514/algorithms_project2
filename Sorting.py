import random
import time

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

    def experimentSort(self, args):
        t1 = time.perf_counter()
        args = self.sort(args)
        t2 = time.perf_counter()
        if not self.isSorted(args):
            return -1
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
        pivot_idx = begin
        for i in range(begin+1, end+1):
            if array[i] <= array[begin]:
                pivot_idx += 1
                array[i], array[pivot_idx] = array[pivot_idx], array[i]
        array[pivot_idx], array[begin] = array[begin], array[pivot_idx]
        return pivot_idx

    def quick_sort_recursion(self, array, begin, end):
        if begin >= end:
            return
        pivot_idx = self.partition(array, begin, end)
        self.quick_sort_recursion(array, begin, pivot_idx-1)
        self.quick_sort_recursion(array, pivot_idx+1, end)

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
                    temp = args[i]
                    args[i] = args[i + 1]
                    args[i + 1] = temp
                    swapped = True
        return args


"""
Implementation of insertion sort.

@author: Levi Lewis
"""
class InsertionSort(Sort):
    def sort(self, args):
        for i in range(len(args)):
            temp = args[i]
            index = i
            while index > 0 and args[index - 1] > temp:
                args[index] = args[index - 1]
                index -= 1
            args[index] = temp
        return args


"""
Main testing routine (work in progress).

@author: Archer Murray
"""
def test():
    mst = MergeSort()
    qst = QuickSort()
    bst = BubbleSort()
    ist = InsertionSort()
    print(mst.experimentSort(
        [random.randrange(1000) for i in range(1000)]))
    print(qst.experimentSort(
        [random.randrange(1000) for i in range(1000)]))
    print(bst.experimentSort(
        [random.randrange(1000) for i in range(1000)]))
    print(ist.experimentSort(
        [random.randrange(1000) for i in range(1000)]))


if __name__ == '__main__':
    test()