# coding=utf-8

from math import ceil


def round_up(x, n=2):
    hundreds = 10 ** n
    return ceil(x * hundreds) / hundreds