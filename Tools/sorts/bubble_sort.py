from __future__ import print_function


def bubble_sort(collection):
    """
    Pure implementation of bubble sort algorithm in Python
    纯python实现的冒泡排序
    :param collection: some mutable ordered collection with heterogeneous comparable items inside
    :return: the same collection ordered by ascending
    """
    # 获取数组的长度
    length = len(collection)
    for i in range(length - 1):
        # 标识, 交换了的
        swapped = False
        for j in range(length - 1 - i):
            if collection[j] > collection[j + 1]:
                swapped = True
                collection[j], collection[j+1] = collection[j+1], collection[j]
        if not swapped:
            break
    return collection


# 测试代码
if __name__ == "__main__":
    user_input = input('Enter numbers separated by a comma:').strip()
    unsorted = [int(item) for item in user_input.split(',')]
    print(*bubble_sort(unsorted), sep=',')
