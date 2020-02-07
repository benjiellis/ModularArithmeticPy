from primefac import primefac
from itertools import product
from mod_int import ComposedGroup, ModularInt

def get_combinations(order):
    factors = list(primefac(order))
    factor_set = set(factors)
    factors_listed = []
    for factor in factor_set:
        current_factor_combos = []
        factor_count = factors.count(factor)
        for partition in accel_asc(factor_count):
            current_factor_combos.append([factor ** value for value in partition])
        factors_listed.append(current_factor_combos)

    all_combos = product(*factors_listed)

    combinations_list = []
    for combo in all_combos:
        flattened = [item for sublist in combo for item in sublist]
        combinations_list.append(flattened)

    return combinations_list

## NOT MY CODE, CREDITS TO JEROME KELLEHER
## http://jeromekelleher.net/generating-integer-partitions.html
def accel_asc(n):
    a = [0 for i in range(n + 1)]
    k = 1
    y = n - 1
    while k != 0:
        x = a[k - 1] + 1
        k -= 1
        while 2 * x <= y:
            a[k] = x
            y -= x
            k += 1
        l = k + 1
        while x <= y:
            a[k] = x
            a[l] = y
            yield a[:k + 2]
            x += 1
            y -= 1
        a[k] = x + y
        y = x + y - 1
        yield a[:k + 1]

def get_groups(order):
    group_factors = get_combinations(order)

    group_list = []

    for factor_set in group_factors:
        group_list.append(ComposedGroup(*[ModularInt(0, mod) for mod in factor_set]))

    return group_list

def get_all_groups_in_range(start, end):
    group_list = []
    for i in range(start, end+1):
        group_list.extend(get_groups(i))

    return group_list