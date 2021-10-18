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
    
    def getSortName(self):
        return self.__class__.__name__.replace('_', ' ')

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
class Merge_Sort(Sort):
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
class Quick_Sort(Sort):
    def partition(self, array, begin, end):
        pivotIdx = begin
        le = list()
        gt = list()
        for i in range(begin + 1, end + 1):
            if array[i] <= array[begin]:
                le.append(array[i])
                pivotIdx += 1
            else:
                gt.append(array[i])
        array[begin:(end + 1)] = le + [array[begin]] + gt
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
class Bubble_Sort(Sort):
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
class Insertion_Sort(Sort):
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
"Medianizes" the given array by repeatedly splitting it in two,
"medianizing" the two halves, and returning an array with the
median as the first element. "Medianizing" a sorted array should
result in a best-case array for quick sort.

@author: Archer Murray
"""
def medianize(arr):
    if len(arr) < 2:
        return arr
    middle = len(arr) // 2
    left = medianize(arr[:middle])
    right = medianize(arr[(middle + 1):])
    return [arr[middle]] + left + right


"""
Returns a 7-tuple of arrays of the given size.
The first array is random.
The second array is the first array sorted.
The third array is the second array reversed.
The fourth array is the second array "shattered".
The fifth array is the fourth array reversed.
The sixth array is the second array "medianized".
The seventh array is the sixth array reversed.

@author: Archer Murray
"""
def getArraySuite(size):
    arr1 = [i for i in range(size)]
    for i in range(1, size):
        index = rnd.randrange(i)
        arr1[i], arr1[index] = arr1[index], arr1[i]
    arr2 = dcopy(arr1)
    arr2.sort()
    arr3 = dcopy(arr2)
    arr3.reverse()
    arr4 = shatter(dcopy(arr2))
    arr5 = dcopy(arr4)
    arr5.reverse()
    arr6 = medianize(dcopy(arr2))
    arr7 = dcopy(arr6)
    arr7.reverse()
    return (arr1, arr2, arr3, arr4, arr5, arr6, arr7)


# The number of times to run each sorting algorithm
# for each case in the integration test.
NUM_TRIALS = 100
# The number of times to trim at each edge
# when computing the average time for each sort and size.
NUM_TRIMS = 10

"""
Integration test.

@author: Archer Murray
"""
def integrationTest():
    sorts = (Merge_Sort(), Quick_Sort(), Bubble_Sort(), Insertion_Sort())
    # Perform the test
    with open('results.txt', 'w') as f:
        f.write('*' * 80 + '\n')
        f.write('Sorting Algorithm Experiment Results\n')
        f.write('Each table entry is the trimmed average of '
                + str(NUM_TRIALS) + ' trials.\n')
        f.write('Blank cells indicate insufficient successful trials.\n')
        f.write('*' * 80 + '\n\n')
        for s in sorts:
            # Write table header
            f.write('=' * 80 + '\n')
            f.write(s.getSortName() + '\n')
            f.write('=' * 80 + '\n\n')
            f.write('{:>10}'.format('Size'))
            f.write('{:>10}'.format('Random'))
            f.write('{:>10}'.format('Sorted'))
            f.write('{:>10}'.format('Reversed'))
            f.write('{:>10}'.format('Shattered'))
            f.write('{:>10}'.format('Rev-Shat'))
            f.write('{:>10}'.format('Med-ized'))
            f.write('{:>10}'.format('Rev-Med') + '\n')
            f.write('-' * 80 + '\n')
            # Get sizes to test
            sizes = list()
            print('Enter array sizes to test for', s.getSortName())
            print('Enter sizes one at a time, then enter "s" '
                  + 'to begin the test.')
            print('Warning: Sizes exceeding 2000 may cause recursion errors '
                  + 'when testing divide-and-conquer sorts.')
            sz_str = ''
            while not sz_str.lower().startswith('s'):
                sz_str = input('Size ' + str(len(sizes) + 1) + ': ')
                try:
                    sizes.append(int(sz_str))
                except ValueError:
                    # The user inputted something that
                    # cannot be converted to int
                    pass
            # Perform sorts based on sizes
            for sz in sizes:
                times = [list(), list(), list(), list(),
                         list(), list(), list()]
                for trial in range(NUM_TRIALS):
                    arrs = getArraySuite(sz)
                    for i in range(7):
                        t = s.testSort(arrs[i])
                        if t >= 0:
                            times[i].append(t)
                f.write('{:>10d}'.format(sz))
                for i in range(7):
                    # Compute the trimmed average of the times
                    times[i].sort()
                    if len(times[i]) > 2 * NUM_TRIMS:
                        trimmed = times[i] \
                            [NUM_TRIMS:(len(times[i]) - NUM_TRIMS)]
                        time = 0
                        for t in trimmed:
                            time += t
                        time /= len(trimmed)
                        f.write('{:>10f}'.format(time))
                    else:
                        f.write(' ' * 10)
                f.write('\n')
                print('Completed size', sz)
            f.write('\n')
            print('\n')
    print('Experiment complete. Results can be found in results.txt.')


if __name__ == '__main__':
    # Test all sorts
    arrs = getArraySuite(10)
    sorts = (Merge_Sort(), Quick_Sort(), Bubble_Sort(), Insertion_Sort())
    for s in sorts:
        print(s.getSortName(), 'test')
        print(s.sort(dcopy(arrs[0])))
        print('Time:', s.testSort(dcopy(arrs[0])), 'seconds')
    # Test array suite
    for a in arrs:
        print(a)
    print('\n')
    # Integration test
    integrationTest()