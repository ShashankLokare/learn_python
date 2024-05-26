from array import *

def printArr(arr1):
    for j in arr1:
        print("\n arr1 numbers = " + str(j))

def findNum(key,n,arr):
    for i in range(n):
        print("\n arr item" + str(arr[i]))
        if(arr[i] == key):
            return i
        

    return -1   

if __name__ == '__main__':
    arr = [12, 34, 45, 11, 4]
    key = 12
    n = len(arr)

    index = findNum(key,n,arr)
    if index == -1:
        print("item not found")
    else:
        print("item found" + str(index + 1))
    
    arr1 = array('i',[1, 34, 67, 78])
    printArr(arr1)
    
    print("---------insert operation-----------")
    arr1.insert(1, 40)
    printArr(arr1)
    print("---------pop operation-----------")
    arr1.pop(1)
    printArr(arr1)

    print("---------update operation-----------")
    arr1[1] = 80
    printArr(arr1)

    print("---------remove operation-----------")
    arr1.remove(1)
    printArr(arr1)