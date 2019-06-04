"""
This is a pure python implementation of the bogosort algorithm  ------> 这是 BogoSort 算法的纯python实现方法
For doctests run following command:                             ------> 对于 doctests 运行以下命令：
python -m doctest -v bogosort.py                                ------> python -m doctest -v bogosort.py
or                                                                                  或者
python3 -m doctest -v bogosort.py                               ------> python3 -m doctest -v bogosort.py
For manual testing run:                                         ------> 对于手动测试运行如下：
python bogosort.py                                              ------> python bogosort.py
"""

from __future__ import print_function
import random


def bogosort(collection):
    """
    Pure implementation of the bogosort algorithm in Python
    ------> BogoSort 算法的纯python实现方法
    :param collection: some mutable ordered collection with heterogeneous comparable items inside
    ------> 内部具有异构可比项的可变有序集合
    :return: the same collection ordered by ascending
    ------> 按升序排列的相同集合
    Examples:
    >>> bogosort([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]
    >>> bogosort([])
    []
    >>> bogosort([-2, -5, -45])
    [-45, -5, -2]
    这个感觉算不上是算法，它的运行逻辑就是完全交给了运气，每次去判断这个数组是否是有序的，没有就重新打乱，直到碰巧有那么一种可能是排好序的数组
    """
    def isSorted(collection):
        if len(collection) < 2:
            return True
        for i in range(len(collection) - 1):
            if collection[i] > collection[i + 1]:
                return False
        return True
    while not isSorted(collection):
        # 用于将一个数组进行打乱
        random.shuffle(collection)
    return collection


# 测试代码
if __name__ == "__main__":
    user_input = input('Enter numbers separated by a comma:\n').strip()
    unsorted = [int(item) for item in user_input.split(',')]
    print(bogosort(unsorted))