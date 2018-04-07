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

def generate_bids(op, tasks, users):
    n = len(users)
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

    q = dict()
    for i in range(0, n):
        q[i] = []
    for i in range(0, m):
        num = random.randrange(2, n + 1)
        s = random.sample(range(0, n), num)
        for j in s:
            q[j].append(i)
    for i in range(0, n):
        bid = []
        if op == 0:
            # uniform
            c = random.uniform(0, 50)
        elif op == 1:
            # exponential
            c = random.expovariate()
        elif op == 2:
            # normal
            c = random.normalvariate()
        bid.append(0)
        bid.append(tuple(q[i]))
        bid.append(c)
        bid.append(i)
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


n = 10
m = 40
r = 3

users = []
for i in range(1, n + 1):
    with open('taxi_log_2008_by_id/' + str(i) + '.txt', 'r') as f:
        reader = csv.reader(f)
        users.append(list(reader))

#print(users[0])

x = []
y = []
for n in range(400, 1100, 100):
    y_sum = 0
    for i in range(0, 20):
        tasks = generate_tasks(m)
        bids = generate_bids(0, tasks, users)
        res = WDBP(tasks, bids, r, n)
        s = res[0]
        w = res[1]
        print(s)
        print(w)
        p_all = 0
        for bid in s:
            # bid[0] = 0
            bids.remove(bid)
            ans = TMDP(bid, bids, n, m)
            bids.append(bid)
            cd = ans[0]
            p = ans[1]
            # print(p)
            p_all = p_all + p
        overpayment = (p_all - w) / w
        print(overpayment)
        y_sum += overpayment
    x.append(n)
    y.append(y_sum / 20)
plt.figure(1)
blue_line = mlines.Line2D([], [], mfc='none',
                          marker='^', label='UNM')
plt.legend(handles=[blue_line])
plt.plot(x, y, "-^", mfc='none')
#plt.axis([300, 1100, 0, 2])
plt.show()





