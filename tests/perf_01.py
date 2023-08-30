from tgos.common_types import Vector2
from itertools import zip_longest
import datetime

N = 1000000


def perf(callback):
    start_time = datetime.datetime.now()
    callback()
    end_time = datetime.datetime.now()
    return end_time - start_time


def vsum_as_tupple_test(v1: list, v2: list):
    return (e1+e2 for e1, e2 in zip_longest(v1, v2, fillvalue=0))


def vsum_as_list_test(v1: list, v2: list):
    return [e1+e2 for e1, e2 in zip_longest(v1, v2, fillvalue=0)]


def vsum_list2(v1: list, v2: list):
    return (v1[0]+v2[0], v1[1]+v2[1])


def t0():
    a = (1, 2)
    b = (3, 4)
    for _ in range(N):
        _ = (a[0]+b[0], a[1]+b[1])


def t0_e():
    a = (1, 2)
    b = (3, 4)
    for _ in range(N):
        _ = vsum_list2(a, b)


def t0_m():
    a = (1, 2)
    b = (3, 4)
    def sum():
        _ = (a[0]+b[0], a[1]+b[1])
    map(lambda x: sum(), range(N))


def t0_em():
    a = (1, 2)
    b = (3, 4)
    map(lambda x: vsum_list2(a, b), range(N))


def t1():
    a = (1, 2)
    b = (3, 4)
    for _ in range(N):
        _ = vsum_as_tupple_test(a, b)


def t1_d():
    for i in range(N):
        a = (i, i+1)
        b = (i+2, i+3)
        _ = vsum_as_tupple_test(a, b)


def t1_du():
    for i in range(N):
        a = (i, i+1)
        b = (i+2, i+3)
        _ = list(vsum_as_tupple_test(a, b))


def t1_m():
    a = (1, 2)
    b = (3, 4)
    c = (4, 5)
    d = (5, 6)
    for i in range(N):
        _ = vsum_as_tupple_test(vsum_as_tupple_test(a, b),
                                vsum_as_tupple_test(c, d))


def t2():
    a = (1, 2)
    b = (3, 4)
    for _ in range(N):
        _ = vsum_as_list_test(a, b)


def t2_d():
    for i in range(N):
        a = (i, i+1)
        b = (i+2, i+3)
        _ = vsum_as_list_test(a, b)


def t2_m():
    a = (1, 2)
    b = (3, 4)
    c = (4, 5)
    d = (5, 6)
    for i in range(N):
        _ = vsum_as_list_test(vsum_as_list_test(a, b),
                              vsum_as_list_test(c, d))


def t3():
    a = Vector2(1, 2)
    b = Vector2(3, 4)
    for _ in range(N):
        _ = a+b


def t3_d():
    for i in range(N):
        a = Vector2(i, i+1)
        b = Vector2(i+2, i+3)
        _ = a+b


def t3_m():
    a = Vector2(1, 2)
    b = Vector2(3, 4)
    c = Vector2(4, 5)
    d = Vector2(5, 6)
    for i in range(N):
        _ = (a+b)+(c+d)


print(f"No call: {perf(t0)}")
print(f"No call with map: {perf(t0_m)}")
print(f"Simple func: {perf(t0_e)}")
print(f"Simple func with map: {perf(t0_em)}")
print(f"Tupple old: {perf(t1)}")
print(f"Tupple new: {perf(t1_d)}")
print(f"Tupple to list: {perf(t1_du)}")
print(f"List old: {perf(t2)}")
print(f"List new: {perf(t2_d)}")
print(f"Vector2 old: {perf(t3)}")
print(f"Vector2 new: {perf(t3_d)}")
print("")
print(f"Tupple multiple: {perf(t1_m)}")
print(f"List multiple: {perf(t2_m)}")
print(f"Vector2 multiple: {perf(t3_m)}")
