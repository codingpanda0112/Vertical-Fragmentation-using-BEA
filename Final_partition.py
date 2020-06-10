import algo
import math

QA_matrix = algo.query_access_matrix  # Query access matrix
sum_attr_access = algo.sum_attr_access  # Sum of accesses by the query applications
order_CA = algo.mat[0][1:]
print(order_CA)
no_of_queries = algo.no_of_queries


def sum_access(arr):
    sum = 0
    for items in arr:
        sum = sum + sum_attr_access[items - 1]
    return sum


def partition():
    z = []
    fragments = []
    for split_point in range(1, len(order_CA)):
        frag1 = order_CA[0:split_point]
        frag2 = order_CA[split_point:len(order_CA)]
        fragments.append([frag1, frag2])
        print("Fragments =", frag1, frag2)

        TA = [] #
        TB = []
        for i in range(no_of_queries):
            use_frag1 = 0
            for items in frag1:
                if QA_matrix[i, items - 1] == 1:
                    use_frag1 = 1
                    break
            TA.append(use_frag1)

            use_frag2 = 0
            for items in frag2:

                if QA_matrix[i, items - 1] == 1:
                    use_frag2 = 1
                    break
            TB.append(use_frag2)
        print("\t","TA =", TA)
        print("\t","TB =", TB)

        TQ = []
        BQ = []
        OQ = []
        for i in range(no_of_queries):
            if TA[i] == 0 and TB[i] == 1:
                BQ.append(i + 1)
            elif TA[i] == 1 and TB[i] == 0:
                TQ.append(i + 1)
            else:
                OQ.append(i + 1)
        print("\t","TQ =", TQ)
        print("\t","BQ =", BQ)
        print("\t","OQ =", OQ)

        CTQ = sum_access(TQ)
        CBQ = sum_access(BQ)
        COQ = sum_access(OQ)

        z.append(CTQ * CBQ - math.pow(COQ, 2))
        print("\t","z =", z)

    if max(z) < 0:
        print("Vertical Fragmentation not possible.")
    else:
        print("Best partition = ", fragments[z.index(max(z))][0], fragments[z.index(max(z))][1])


partition()
