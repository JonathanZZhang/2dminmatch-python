import copy
import math
import random


class Branch:
    name = ''
    long = 0
    lat = 0
    index = 0

    def __init__(self, name, long, lat):
        self.name = name
        self.long = long
        self.lat = lat
        self.index = 0

    def to_str(self):
        return self.name + ' at (' + str(self.long) + ', ' + str(self.lat) + ')'


def root(n):
    return math.sqrt(n)


def index(branches):
    for i in range(len(branches)):
        branches[i].index = i


def distance(b1, b2):
    return root((b1.long - b2.long) ** 2 + (b1.lat - b2.lat) ** 2)


def closest_pair_3p(p1, p2, p3):  # Helper
    # Find the pair with least distance among 3 pairs
    print(
        f'comparing: ({p1[0].name}, {p1[1].name}), ({p2[0].name}, {p2[1].name}), ({p3[0].name}, {p3[1].name}) with distance {[distance(i[0], i[1]) for i in [p1, p2, p3]]}')
    return min(p1, p2, p3, key=lambda x: distance(x[0], x[1]))


def cmp_long(b1, b2):
    # return True if longitude of b1 is less than that of b2
    return b1.long < b2.long


def cmp_lat(b1, b2):
    # return True if latitude of b1 is less than that of b2
    return b1.lat < b2.lat


def closest_pair_3b(branches):
    min = distance(branches[0], branches[1])
    b1 = branches[0]
    b2 = branches[1]
    for i in range(3):
        for j in range(i + 1, 3):
            d = distance(branches[i], branches[j])
            if d < min:
                b1 = branches[i]
                b2 = branches[j]
    return [b1, b2]


def sort_branches(branches):
    branches.sort(key=lambda x: x.long, reverse=False)
    for i in range(len(branches)):
        branches[i].index = i


def mid_branches(branches):
    l = len(branches)
    if l % 2 == 0:
        return [branches[l // 2 - 1], branches[l // 2]]
    else:
        mid_index = (l - 1) // 2
        return [branches[mid_index - 1], branches[mid_index], branches[mid_index + 1]]


def closest_pair(branches):
    if len(branches) == 2:
        #        print(f'base case reached: {[i.to_str() for i in branches]}')
        return branches
    elif len(branches) == 3:
        return closest_pair_3b(branches)
    else:
        l = len(branches)
        if l % 2 == 0:
            left = branches[:l // 2]
            right = branches[l // 2:]
            mid = mid_branches(branches)
            print(f'list of length {l} is spitted to {len(left)},{len(mid)},{len(right)}')
        else:
            left = branches[:(l - 1) // 2]
            right = branches[(l + 1) // 2:]
            mid = mid_branches(branches)
            print(f'list of length {l} is spitted to {len(left)},{len(mid)},{len(right)}')
    return closest_pair_3p(closest_pair(left), closest_pair(mid), closest_pair(right))


def match_branches_core(branches):
    lop = []
    l = len(branches)
    i = 0  # 初始化计数器，此计数器用来解决list.append后改变相关内存造成的list值改变的bug/:
    temp_list = [0] * 1000
    while len(branches) > 1:
        print(f'Matching branches: {[i.to_str() for i in branches]}')
        p = closest_pair(branches)
        temp_list[i] = copy.copy(p)
        lop.append(temp_list[i])
        #        print(f'size of generated list: {len(lop)}')
        b1 = temp_list[i][0]
        b2 = temp_list[i][1]
        i += 1
        #        print('founded indices: ' + str(b1.index) + ' ' + str(b2.index))
        if b1.index < b2.index:
            branches.pop(b1.index)
            branches.pop(b2.index - 1)
            print(len(branches))
        else:
            branches.pop(b1.index)
            branches.pop(b2.index)
            print(len(branches))
        #        print(f'{[i.name for i in branches]}')
        index(branches)
    if len(branches) == 1:
        lop.append([branches[0]])
    #       print(f'size of generated list: {len(lop)}')
    return lop


def match_branches(branches):
    lof_pairs = match_branches_core(branches)
    #    print(f'No. of pairs selected is {len(lof_pairs)}')
    lof_pair_names = []
    for p in lof_pairs:
        if len(p) == 1:
            lof_pair_names.append([p[0].name])
        lof_pair_names.append([p[0].name, p[1].name])
    return lof_pair_names


# Tests


def generate_test_branches():
    branches = []
    for i in range(100):
        b = Branch('branch' + str(i), round(random.uniform(116, 117), 4), round(random.uniform(36, 37), 4))
        branches.append(b)
    sort_branches(branches)
    print(f'Test branches generated: {len(branches)}')
    return branches


testb1 = Branch('branch1', 0, 0)
testb2 = Branch('branch2', 0.5, 0)
testb3 = Branch('branch3', 1, 0)
testb4 = Branch('branch4', 2, 0)
# print(distance(testb1, testb4))
test_branches = [testb1, testb2, testb3, testb4]
sort_branches(test_branches)
test_branches2 = generate_test_branches()

# print(f'found the closest pair: {[i. name for i in closest_pair(test_branches)]}', end = ' ')
# print(f'in the list {str([i.name for i in test_branches])}')
print(f'Generated the list of pairs of closest pairs: {(match_branches(test_branches2))}')
