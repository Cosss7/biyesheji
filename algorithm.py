import logging
import time
logging.basicConfig(filename='log.log', level=logging.INFO)


def WDBP(tasks, bids, r, n):
    # logging.info('in WDBP')
    m = len(tasks)
    # cnt count each user has accommodated bids.
    cnt = dict()
    for i in range(0, n):
        cnt[i] = 0
    # s--winning bids, w--social cost, qc--complete tasks
    s = []
    w = 0
    qc = set()
    while len(qc) < m:
        # pick bid satisfy |q_i^k - qc| > 0.
        bids = [bid for bid in bids
                if len(set(bid[1]).difference(qc)) > 0]
        # notice! It's possible tasks may not complete.
        if len(bids) == 0:
            break
        # compute r(beta_i^k) for each bid.
        for bid in bids:
            q = set(bid[1])
            c = bid[2]
            bid[0] = c / len(q.difference(qc))
        bids = sorted(bids)
        bid = bids[0]
        # update.
        s.append(bid)
        q = bid[1]
        c = bid[2]
        id = bid[3]
        w += c
        qc = qc.union(q)
        del bids[0]
        # remove bids that conflict with beta_i^k.
        cnt[id] += 1
        if cnt[id] >= r:
            bids = [bid for bid in bids
                    if bid[3] == id]
    # logging.info('out WDBP')
    return s, w


def TMDP(bidxy, bids, n, m, r):
    # print('in TMDP')
    # cnt count each user has accommodated bids.
    cnt = dict()
    for i in range(0, n):
        cnt[i] = 0
    qxy = set(bidxy[1])
    qc = set()
    while len(qc) != m:
        # pick bid satisfy |q_i^k - qc| > 0.
        bids = [bid for bid in bids
                if len(set(bid[1]).difference(qc)) > 0]
        # notice! It's possible tasks may not complete.
        if len(bids) == 0:
            bid = bidxy
            cb = bid
            p = max(bidxy[2], bid[0] * len(qxy.difference(qc)))
            # logging.info('out TMDP')
            return cb, p
        # compute r(beta_i^k) for each bid.
        for bid in bids:
            q = set(bid[1])
            c = bid[2]
            bid[0] = c / len(q.difference(qc))
        bids = sorted(bids)
        bid = bids[0]
        q = bid[1]
        id = bid[3]
        if len(qxy.difference(qc.union(q))) == 0:
            cb = bid
            p = bid[0] * len(qxy.difference(qc))
            # logging.info('out TMDP')
            return cb, p
        qc = qc.union(q)
        del bids[0]
        cnt[id] += 1
        if cnt[id] >= r:
            bids = [bid for bid in bids
                    if bid[3] == id]
    # if cant find critical bid, return self
    # logging.info('out TMDP')
    return bidxy, bidxy[2]


dfs_s = []
dfs_w = 100000000000000


def dfs(tasks, bids, r, cur_bids, cur_idx):
    m = len(tasks)
    n = len(bids)
    q = set()
    for bid in cur_bids:
        q = q.union(bid[1])
    # if len(q) == m:
    #     return
    for i in range(cur_idx, n):
        cur_bids.append(bids[i])
        dfs(tasks, bids, r, cur_bids, i + 1)
        cur_bids.remove(bids[i])

