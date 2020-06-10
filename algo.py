import numpy as np

#A1 =reportsTo , A2 =officeCode. A3 =  lastname, A4 = jobtitle

# SELECT     lastName,        reports To FROM     employees WHERE     reportsTo IS NULL;
# SELECT     lastName,     officeCode FROM     employees WHERE     officeCode IN (1 , 2, 3);
# SELECT     officeCode, jobTitle  FROM     employees WHERE     jobtitle = 'Sales Rep';
# SELECT   lastname,     jobtile     FROM     employees WHERE     lastName LIKE '%son';
#


query_access_matrix = [[1, 0, 1, 0],
                [0, 1, 1, 0],
                [0, 1, 0, 1],
                [0, 0, 1, 1]]

query_access_matrix = np.array(query_access_matrix)
print("Query Access Matrix = ")
print(query_access_matrix)
no_of_queries = query_access_matrix.shape[0]

# Frequency Access Matrix - no of times the queries accesses the sites in a day
# Assuming random values
Frequency_access_matrix = [[15, 20, 10],  # Q1
                    [5, 0, 0],  # Q2
                    [25, 25, 25],  # Q3
                    [3, 0, 0]]  # q4
Frequency_access_matrix = np.array(Frequency_access_matrix)
print("Frequency Access Matrix = ")
print(Frequency_access_matrix)

Frequency_access_matrix_np = np.array(Frequency_access_matrix)
sum_attr_access = np.sum(Frequency_access_matrix_np, axis=1)
print("Sum of attr access by each query = ")
print(sum_attr_access)

no_of_attr = query_access_matrix.shape[1]
n = no_of_attr
_rightmostIndex = 0
_maxContribRightIndex = 0
_maxContribMidIndex = 0
_maxContribLeftIndex = 0


def recordplacement(left, mid, right):
    global _maxContribMidIndex
    global _maxContribRightIndex
    global _maxContribLeftIndex

    _maxContribLeftIndex = left
    _maxContribMidIndex = mid
    _maxContribRightIndex = right


def findquery(i, j):
    query_id = 0
    found = 0
    query_lis = []
    for query in query_access_matrix:

        if query[i] == 1 and query[j] == 1:
            query_lis.append(query_id)
        # return query_id

        query_id = query_id + 1

    # print("query list", query_lis)
    return query_lis


def aff(Ai, Aj):
    q = findquery(Ai, Aj)
    sum_ = 0;
    if len(q) == 0:
        sum_ = 0
    else:
        for qu in q:
            sum_ = sum_ + sum(Frequency_access_matrix[qu])
    return sum_


AA = []
for i in range(no_of_attr):
    row = []
    for j in range(no_of_attr):
        sum_ = aff(i, j)
        row.append(sum_)
    AA.append(row)

# transform the row matrix
row0 = [i for i in range(no_of_attr + 1)]
attr_affinity_matrix = [row0]
for i in AA:
    row_ = [0]
    for k in i:
        row_.append(k)
    attr_affinity_matrix.append(row_)


def calculatebond(Ax, Ay):
    total = 0
    for i in range(1, no_of_attr + 1):
        total = total + attr_affinity_matrix[i][Ax] * attr_affinity_matrix[i][Ay]
    return total


def cont(Ai, Ak, Aj):
    if Ai == 0:
        return 2 * calculatebond(Ak, Aj)
    if Aj == Ak + 1:
        return 2 * calculatebond(Ai, Ak)
    val = 2 * calculatebond(Ai, Ak) + 2 * calculatebond(Ak, Aj) - 2 * calculatebond(Ai, Aj)
    return val


def getcol(colno, arr):
    res = []
    # print("inside getcol")
    # print(colno)
    for i in range(len(arr)):
        # print(arr[i][colno])
        res.append(arr[i][colno])
    return res


def copy_col_attr_affinity_matrixto_CA(col, CA, AA):
    global _rightmostIndex

    colval = getcol(col, AA)
    for i in range(len(CA)):
        CA[i][col] = colval[i]
    _rightmostIndex = col


def BEA():
    CA = np.zeros([no_of_attr + 1, no_of_attr + 1], dtype=int)
    # placecolumn(CA, attr_affinity_matrix)
    copy_col_attr_affinity_matrixto_CA(1, CA, attr_affinity_matrix)
    copy_col_attr_affinity_matrixto_CA(2, CA, attr_affinity_matrix)
    # print(CA)

    index = 3
    # print("Index",index)
    # print("n",n)

    while index <= n:
        contrib = 0
        maxcontribution = 0
        record = []

        for i in range(1, index):
            contrib = cont(CA[0][i - 1], index, CA[0][i])
            # print(contrib)
            # print(contrib)
            if contrib >= maxcontribution:
                maxcontribution = contrib
                record.append((CA[0][i - 1], index, CA[0][i]))
                recordplacement(CA[0][i - 1], index, CA[0][i])

        contrib = cont(CA[0][index - 1], index, index + 1)
        # print(contrib)
        if contrib >= maxcontribution:
            maxcontribution = contrib
            record.append((CA[0][index - 1], index, index + 1))
            recordplacement(CA[0][index - 1], index, index + 1)
        # print(record[-1])
        # print(index,_rightmostIndex,_maxContribMidIndex,_maxContribLeftIndex,_maxContribRightIndex)
        placecolumn(CA, attr_affinity_matrix)
        index = index + 1
    # print("final",CA)
    temp = np.zeros([no_of_attr + 1, no_of_attr + 1], dtype=int)
    for i in range(1, n + 1):
        row = CA[0][i]
        temp[0][i] = row
        for j in range(1, n + 1):
            temp[i][j] = CA[row][j]
    # print("trans",temp)
    return temp


def copycol(col, CA, arr):
    global _rightmostIndex
    # print("prints",col,arr)
    for i in range(len(CA)):
        CA[i][col] = arr[i]
    _rightmostIndex = col


def placecolumn(CA, AA):
    global _rightmostIndex
    global _maxContribMidIndex
    global _maxContribRightIndex
    global _maxContribLeftIndex
    # left = places[0]
    # mid = places[1]
    if _maxContribLeftIndex == 0:
        for i in range(_rightmostIndex, 1, -1):
            copycol(i, CA, getcol(i - 1, AA))
        copycol(1, CA, getcol(_maxContribMidIndex, AA))
        _rightmostIndex = _rightmostIndex + 1
        return

    start = 0
    for i in range(1, no_of_attr + 1):  # check
        start = i
        if CA[0][start] == _maxContribLeftIndex:
            break
    # print("start",start)

    if start == _rightmostIndex:
        _rightmostIndex = _rightmostIndex + 1
        copycol(_rightmostIndex, CA, getcol(_maxContribMidIndex, AA))
    # print('inside 1',CA)

    for i in range(_rightmostIndex + 1, start + 1, -1):
        # print("end",i,getcol(i - 1, AA))
        if i == no_of_attr + 1:
            copycol(i - 1, CA, getcol(i - 1, AA))
        else:
            copycol(i, CA, getcol(i - 1, AA))
    # print("insid2",CA)

    copycol(start + 1, CA, getcol(_maxContribMidIndex, AA))
    _rightmostIndex = _rightmostIndex + 1


#


CA = np.zeros([no_of_attr + 1, no_of_attr + 1], dtype=int)

print("Affinity matrix")

for i in attr_affinity_matrix:
    print("\t", i[1:])
# print(AA)

mat = BEA()

print("final matrix")
for i in mat:
    print("\t", i[1:])