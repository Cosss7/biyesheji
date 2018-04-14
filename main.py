import csv
import time
import random
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import matplotlib.lines as mlines



def generate_tasks(m):
    # should be uniform dist
    tasks = []
    for i in range(0, m):
        tup = (i, 0, 0)
        tasks.append(tup)
    return tasks

def task_in_user(task, user):
    return True

def generate_bids(op, tasks, n):
    # n = len(users)
    m = len(tasks)
    bids = []
    # for i in range(0, n):
    #     bid = []
    #     q = []
    #     c = 0
    #     for j in range(0, m):
    #         if task_in_user(tasks[j], users[i]):
    #             q.append(j)
    #     if op == 0:
    #         # uniform
    #         c = random.uniform(0, 50)
    #     elif op == 1:
    #         # exponential
    #         c = random.expovariate()
    #     elif op == 2:
    #         # normal
    #         c = random.normalvariate()
    #     bid.append(0)
    #     bid.append(tuple(q))
    #     bid.append(c)
    #     bid.append(i)
    #     bids.append(bid)

    for i in range(0, m):
        num = random.randrange(2, n + 1)
        s = random.sample(range(0, n), num)

        for j in s:
            bid = []
            if op == 0:
                # uniform
                c = random.uniform(0, 50)
            elif op == 1:
                # normal
                c = 0
                while c <= 0:
                    c = random.normalvariate(25, 25 / 1.3)
            elif op == 2:
                # exponential
                # c = random.expovariate(1)
                c = random.uniform(0, 50)
            bid.append(0)
            q = [i]
            q = tuple(q)
            bid.append(q)
            bid.append(c)
            bid.append(j)
            bids.append(bid)

    return bids












def WDBP(tasks, bids, r, n):
    m = len(tasks)
    cnt = dict()
    for i in range(0, n):
        cnt[i] = 0

    s = []
    w = 0
    qc = set()
    while len(qc) < m:
        bids = [bid for bid in bids
                if len(set(bid[1]).difference(qc)) > 0]
        for bid in bids:
            q = set(bid[1])
            c = bid[2]
            bid[0] = c / len(q.difference(qc))
        if len(bids) == 0:
            break
        bids = sorted(bids)
        s.append(bids[0])
        bid = bids[0]
        q = bid[1]
        c = bid[2]
        id = bid[3]
        w = w + c
        qc = qc.union(q)
        del bids[0]
        cnt[id] = cnt[id] + 1
        if cnt[id] >= r:
            bids = [bid for bid in bids
                    if bid[3] == id]

    return s, w


def TMDP(bidxy, bids, n, m):
    cnt = dict()
    for i in range(0, n):
        cnt[i] = 0

    qxy = set(bidxy[1])
    qc = set()
    while len(qc) != m:

        bids = [bid for bid in bids
                if len(set(bid[1]).difference(qc)) > 0]
        for bid in bids:
            q = set(bid[1])
            c = bid[2]
            bid[0] = c / len(q.difference(qc))
        if len(bids) == 0:
            bid = bidxy
            cb = bid
            p = bid[0] * len(qxy.difference(qc))
            return cb, p
        bids = sorted(bids)
        bid = bids[0]
        q = bid[1]
        c = bid[2]
        id = bid[3]
        if len(qxy.difference(qc.union(q))) == 0:
            cb = bid
            p = bid[0] * len(qxy.difference(qc))
            return cb, p
        qc = qc.union(q)
        del bids[0]
        cnt[id] = cnt[id] + 1
        if cnt[id] >= r:
            bids = [bid for bid in bids
                    if bid[3] == id]


if __name__ == '__main__':
    n = 500
    m = 40
    r = 3

    # users = []
    # for i in range(1, n + 1):
    #     with open('taxi_log_2008_by_id/' + str(i) + '.txt', 'r') as f:
    #         reader = csv.reader(f)
    #         users.append(list(reader))

    #print(users[0])

    def range_n(op):
        # range n

        x = []
        y = []
        z = []
        for n in range(400, 1100, 100):
            y_sum = 0
            z_sum = 0
            loop = 20
            for i in range(0, loop):
                tasks = generate_tasks(m)
                bids = generate_bids(op, tasks, n)
                bids_tmp = bids
                res = WDBP(tasks, bids_tmp, r, n)
                s = res[0]
                w = res[1]
                print(w)
                p_all = 0
                for bid in s:
                    bid_tmp = bid
                    bid_tmp[0] = 0
                    bids.remove(bid_tmp)
                    bids_tmp = bids
                    ans = TMDP(bid_tmp, bids_tmp, n, m)
                    bids.append(bid_tmp)
                    cd = ans[0]
                    p = ans[1]
                    # print(p)
                    p_all = p_all + p
                overpayment = (p_all - w) / w
                print(overpayment)
                y_sum += overpayment
                z_sum += w
            x.append(n)
            y.append(y_sum / loop)
            z.append(z_sum / loop)
        return x, y, z


    # fig, ax = plt.subplots()
    plt.figure(1)
    zz = []
    plt.ylabel('Overpayment ratio $\lambda$')
    plt.xlabel('Number of smartphones $n$')
    x, y, z = range_n(0)
    zz.append(z)
    plt.plot(x, y, "-^", mfc='none', label='UNM')

    x, y, z = range_n(1)
    zz.append(z)
    plt.plot(x, y, "-o", mfc='none', label='NORM')

    x, y, z = range_n(2)
    zz.append(z)
    plt.plot(x, y, "-s", mfc='none', label='EXP')

    plt.legend(loc='best')
    plt.savefig('Overpayment ratio vs. Number of smartphones.png')
    plt.show()

    plt.figure(2)
    plt.ylabel('Social cost $\omega$')
    plt.xlabel('Number of smartphones $n$')
    plt.plot(x, zz[0], "-^", mfc='none', label='UNM')
    plt.plot(x, zz[1], "-o", mfc='none', label='NORM')
    plt.plot(x, zz[2], "-s", mfc='none', label='EXP')
    plt.legend(loc='best')
    plt.savefig('Social cost vs. Number of smartphones.png')
    plt.show()



