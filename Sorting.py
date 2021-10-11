from datetime import datetime
import random
import time

class Sort:
    def __init__(self, args):
        s = time.time()
        a2 = []
        a2.extend(args)
        self.sort(a2)
        print("Execution Time For",self.__class__.__name__.replace("_", " "),":", time.time() - s, "seconds for",len(a2),"elements")        
    
    def sort(self, args):
        pass
    
    def isSorted(self, args):
        lastVal = None
        for i in args:
            if lastVal:
                if lastVal > i:
                    #print("Not sorted")
                    return False
            lastVal = i
        return True
        
class Merge_Sort(Sort):
    def sort(self,args):
        if(len(args) <= 1):
            return args
        middle = len(args) // 2
        left = args[:middle]
        right = args[middle:]

        left = self.sort(left)
        right = self.sort(right)
        return list(self.merge(left, right))

    def merge(self,left, right):
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

class Quick_Sort(Sort):
    def partition(self,array, begin, end):
        pivot_idx = begin
        for i in range(begin+1, end+1):
            if array[i] <= array[begin]:
                pivot_idx += 1
                array[i], array[pivot_idx] = array[pivot_idx], array[i]
        array[pivot_idx], array[begin] = array[begin], array[pivot_idx]
        return pivot_idx

    def quick_sort_recursion(self,array, begin, end):
        if begin >= end:
            return 
        pivot_idx = self.partition(array, begin, end)
        self.quick_sort_recursion(array, begin, pivot_idx-1)
        self.quick_sort_recursion(array, pivot_idx+1, end)
    
    def sort(self,array, begin=0, end=None):
        if end is None:
            end = len(array) - 1 
        self.quick_sort_recursion(array, begin, end)
        return array
            
class Bubble_Sort(Sort):
    def sort(self,args):
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

max_length = 100000
my_list = list(random.randint(0, 500) for i in range(max_length))  
for j in range(0,max_length + 1, 1000):  
    li = my_list[:j]
    #Bubble_Sort(li)
    Merge_Sort(li)
    Quick_Sort(li)
    print()