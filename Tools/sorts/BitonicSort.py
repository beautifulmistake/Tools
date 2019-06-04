# Python program for Bitonic Sort. Note that this program works only when size of input is a power of 2.
# 用于 Bitonic Sort 的 python程序。需要注意的是这个程序只有当数组的元素个数的大小是 2 的幂时才有效。


# The parameter dir indicates the sorting direction, ASCENDING
# or DESCENDING; if (a[i] > a[j]) agrees with the direction,
# then a[i] and a[j] are interchanged.*/
# It recursively sorts a bitonic sequence in ascending order,
def compAndSwap(a, i, j, dire):
    """
    比较和位置交换的方法：
    参数 dire 代表着排序的方向，如果 a[i] > a[j] 与 dire 表示的方向一致，则a[i] 和 a[j] 互换位置
    程序递归的对一个 bitonic sequence 进行升序排序
    :param a:
    :param i:
    :param j:
    :param dire:
    :return:
    """
    if (dire == 1 and a[i] > a[j]) or (dire == 0 and a[i] < a[j]):
        a[i], a[j] = a[j], a[i]


# if dir = 1, and in descending order otherwise (means dir=0).
# The sequence to be sorted starts at index position low,
# the parameter cnt is the number of elements to be sorted.
# This funcion first produces a bitonic sequence by recursively
def bitonicMerge(a, low, cnt, dire):
    """
    如果 dire = 1,则按照降序排序（意味着 dire = 0）
    要排序的序列从索引位置较低的一端开始，而 cnt 参数表示需要排序的元素个数
    这个函数首先通过递归生成一个 bitonic 序列
    :param a:
    :param low:
    :param cnt:
    :param dire:
    :return:
    """
    if cnt > 1:
        k = int(cnt / 2)
        for i in range(low, low + k):
            compAndSwap(a, i, i + k, dire)
        bitonicMerge(a, low, k, dire)
        bitonicMerge(a, low + k, k, dire)


# sorting its two halves in opposite sorting orders, and then
# calls bitonicMerge to make them in the same order
# Caller of bitonicSort for sorting the entire array of length N
def bitonicSort(a, low, cnt, dire):
    """
    将它的两部分按照相反的顺序进行排序，然后再调用  bitonicMerge 方法使他们按照相同顺序排序
    BitonicSort 这个排序方法的主要调用方法，用于对长度为 N 的整个数组进行排序
    :param a:
    :param low:
    :param cnt:
    :param dire:
    :return:
    """
    if cnt > 1:
        k = int(cnt / 2)
        bitonicSort(a, low, k, 1)
        bitonicSort(a, low + k, k, 0)
        bitonicMerge(a, low, cnt, dire)


# in ASCENDING order
def sort(a, N, up):
    """
    按照升序排序
    :param a:
    :param N:
    :param up:
    :return:
    """
    bitonicSort(a, 0, N, up)


# Driver code to test above
if __name__ == "__main__":
    # a = []
    #
    # n = int(input())
    # for i in range(n):
    #     a.append(int(input()))
    # up = 1
    #
    # sort(a, n, up)
    # print("\n\nSorted array is ")
    # for i in range(n):
    #     print("%d" % a[i])
    a = [2, 6, 4, 7, 9, 8, 10, 50, 100, 63, 19, 29, 45, 84, 20, 87]
    n = len(a)
    up = 1
    sort(a, n, up)
    print(a)