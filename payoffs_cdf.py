import logging
import generator
import algorithm
import matplotlib.pyplot as plt
logging.basicConfig(filename='log.log', level=logging.INFO)


def cdf(op, n, m):

    x = []
    y = []
    z = []
    p_list = []
    for i in range(0, n):
        p_list.append(0)

    y_sum = 0
    z_sum = 0
    loop = 1
    for i in range(0, loop):
        tasks = generator.generate_tasks(m)
        bids = generator.generate_bids(op, tasks, n)
        bids_tmp = bids
        res = algorithm.WDBP(tasks, bids_tmp, r, n)
        s = res[0]
        w = res[1]
        logging.info(w)
        p_all = 0
        for bid in s:
            bid_tmp = bid
            bid_tmp[0] = 0
            bids.remove(bid_tmp)
            bids_tmp = bids
            ans = algorithm.TMDP(bid_tmp, bids_tmp, n, m, r)
            bids.append(bid_tmp)
            cd = ans[0]
            p = ans[1]
            print(bid[3])
            p_all = p_all + p
            p_list[bid[3]] += p
        overpayment = (p_all - w) / w
        logging.info(overpayment)
        y_sum += overpayment
        z_sum += w
    x.append(m)
    y.append(y_sum / loop)
    z.append(z_sum / loop)
    p_list = sorted(p_list)
    return p_list


if __name__ == '__main__':
    n = 500
    m = 40
    r = 3

    # fig, ax = plt.subplots()
    plt.figure(1)
    plt.ylabel('Empirical CDF')
    plt.xlabel('Payoffs')
    n = 1000
    m = 40
    x = []
    y = []
    p_list = cdf(0, n, m)
    for i in range(0, n):
        x.append(p_list[i])
        y.append((i + 1) / n)

    plt.plot(x, y, label='n=1000, m=40')
    plt.legend(loc='best')
    plt.savefig('Empirical CDF vs. Payoffs.png')
    plt.show()




