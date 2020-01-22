import math
class Branch:
    name = ''
    long = 0
    lap = 0
    index = 0

    def __init__(self, name, long, lap):
        self.name = name
        self.long = long
        self.lap = lap
        self.index = 0
    
    def toStr(self):
        return self.name + ' at (' + self.long + ', ' + self.lap + ')'

def root(n):
    return math.sqrt(n)

def distance(b1, b2):
    return root((b1.long - b2.long) ** 2 + (b1.lap - b2.lap) ** 2)

def closestPair_3p(p1, p2, p3): #Helper
    #Find the pair with least distance among 3 pairs
    return min([p1, p2, p3], key = lambda x: distance(p1[0], p1[1]))

def cmpLong(b1, b2):
    # return True if longitude of b1 is less than that of b2
    return b1.long < b2.long

def cmpLap(b1, b2):
    #return True if laptitude of b1 is less than that of b2
    return b1.lap < b2.lap

def closestPair_3b(branches):
    min = distance(branches[0], branches[1])
    b1 = branches[0]
    b2 = branches[1]
    for i in range(3):
        for j in range(i+1, 3):
            d = distance(branches[i], branches[j])
            if d < min:
                b1 = branches[i]
                b2 = branches[j]
    return [b1, b2]

def sortBranches(branches):
    branches.sort(key = lambda x:x.long, reverse = False)
    for i in range(len(branches)):
        branches[i].index = i
    
def mid_branches(branches):
    l = len(branches)
    if l % 2 == 0: 
        return [branches[l/2], branches[l/2 + 1]]
    else:
        mid_index = (l+1)/2
        return [branches[l-1], branches[l], branches[l+1]]

def closestPair(branches):
    if len(branches) == 2:
        return branches
    elif len(branches) == 3:
        return closestPair_3b(branches)
    else:
        l = len(branches)
        if l % 2 == 0:
            left = branches[:l/2]
            right = branches[l/2+1:]
            mid = mid_branches(branches)
            return closestPair_3p(closestPair(left), closestPair(mid), closestPair(right))

def matchBranchesCore(branches):
    list = []
    while(len(branches) > 1):
        list.append(closestPair(branches))
        p = closestPair(branches)
        b1 = p[0]
        b2 = p[1]
        print('founded indices: ' + str(b1.index) + ' ' + str(b2.index))
        if b1.index < b2.index:
            branches.pop(b1.index)
            branches.pop(b2.index - 1)
        else:
            branches.pop(b1.index)
            branches.pop(b2.index)
    if len(branches) == 1:
        list.append([branches[0]])
    return list

def matchBranches(branches):
    lofPairs = matchBranchesCore(branches)
    lofPairNames = []
    for i in range(0, len(lofPairs)):
        lofPairNames.append([j.name for j in lofPairs[i]])
    return lofPairNames

testb1 = Branch('branch1', 0, 0)
testb2 = Branch('branch2', 0, 1)
testb3 = Branch('branch3', 0, 3)
test_branches = [testb1, testb2, testb3]
sortBranches(test_branches)
test_branches2 = []
print(f'found the closest pair: {[i.name for i in closestPair(test_branches)]}', end = ' ')
print(f'in the list {str([i.name for i in test_branches])}')

print(f'Generated the list of pairs of closest pairs: {(matchBranches(test_branches))}') 
