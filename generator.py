import random


def generate_tasks(m):
    # should be uniform dist
    tasks = []
    for i in range(0, m):
        tup = (i, 0, 0)
        tasks.append(tup)
    return tasks


def task_in_user(task, user):
    return True


def generate_cost(op, mu=2):
    c = 0
    if op == 0:
        # uniform
        if mu == 0:
            c = random.uniform(0, 30)
        elif mu == 1:
            c = random.uniform(0, 40)
        elif mu == 2:
            c = random.uniform(0, 50)
    elif op == 1:
        # normal
        c = 0
        while c <= 1 or c > 50:
            if mu == 0:
                c = random.normalvariate(15, 25 / 1.3)
            elif mu == 1:
                c = random.normalvariate(20, 25 / 1.3)
            elif mu == 2:
                c = random.normalvariate(25, 25 / 1.3)
    elif op == 2:
        # exponential
        if mu == 0:
            c = random.expovariate(1 / 15)
        elif mu == 1:
            c = random.expovariate(1 / 20)
        elif mu == 2:
            c = random.expovariate(1 / 25)
    return c


def generate_bids(op, tasks, n):
    random.seed()
    m = len(tasks)
    bids = []
    task2user = []
    n //= 10
    for i in range(0, n):
        task2user.append([])
    # iterate tasks, a task assign to at least two users.
    for i in range(0, m):
        num = random.randrange(2, 10)
        s = random.sample(range(0, n), num)
        # add the task to selected users.
        for j in s:
            task2user[j].append([i])
    # iterate users, generate bids
    for i in range(0, n):
        # a bid
        sub_tasks = task2user[i]
        # add each sub-tasks as a bid, guarantee every sub-tasks can be take.
        for j in sub_tasks:
            bid = []
            bid.append(0)
            bid.append(tuple(j))
            bid.append(generate_cost(op))
            bid.append(i)
            bids.append(bid)
        # random the number of bids the user submitted.
        k = random.randrange(0, len(sub_tasks) + 1)
        for itk in range(0, k):
            bid = []
            q_tmp = random.sample(sub_tasks, random.randrange(1, len(sub_tasks) + 1))
            q = []
            for qi in q_tmp:
                q.append(qi[0])
            bid.append(0)
            bid.append(tuple(q))
            bid.append(generate_cost(op) * len(q))
            bid.append(i)
            bids.append(bid)
    return bids


def generate_bids_mu(op, tasks, n, mu):
    random.seed()
    m = len(tasks)
    bids = []
    task2user = []
    n //= 10
    for i in range(0, n):
        task2user.append([])
    # iterate tasks, a task assign to at least two users.
    for i in range(0, m):
        num = random.randrange(2, 10)
        s = random.sample(range(0, n), num)
        # add the task to selected users.
        for j in s:
            task2user[j].append([i])
    # iterate users, generate bids
    for i in range(0, n):
        # a bid
        sub_tasks = task2user[i]
        if len(sub_tasks) == 0:
            continue
        # add each sub-tasks as a bid, guarantee every sub-tasks can be take.
        for j in sub_tasks:
            bid = []
            bid.append(0)
            bid.append(tuple(j))
            bid.append(generate_cost(op, mu))
            bid.append(i)
            bids.append(bid)
        # random the number of bids the user submitted.
        k = random.randrange(1, len(sub_tasks) + 2)
        for itk in range(0, k):
            bid = []
            q_tmp = random.sample(sub_tasks, random.randrange(1, len(sub_tasks) + 1))
            q = []
            for qi in q_tmp:
                q.append(qi[0])
            bid.append(0)
            bid.append(tuple(q))
            bid.append(generate_cost(op, mu) * len(q))
            bid.append(i)
            bids.append(bid)
    return bids

