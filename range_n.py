import logging
import generator
import algorithm
import matplotlib.pyplot as plt
import time
logging.basicConfig(filename='log.log', level=logging.INFO)


def range_n(op):
    # x -- n, y -- overpayment ratio, z -- social cost.
    x = []
    y = []
    z = []
    for n in range(400, 1100, 100):
        # print('in n = ' + str(n))
        y_sum = 0
        z_sum = 0
        loop = 20
        for i in range(0, loop):
            # print('in loop ' + str(i))
            tasks = generator.generate_tasks(m)
            bids = generator.generate_bids(op, tasks, n)
            bids_tmp = bids
            s, w = algorithm.WDBP(tasks, bids_tmp, r, n)
            print(s)
            print(w)
            # logging.info(s)
            # logging.info(w)
            # compute payment.
            p_all = 0
            # print("s = " + str(len(s)))
            for bid in s:
                bid_tmp = bid
                bid_tmp[0] = 0
                bids.remove(bid_tmp)
                bids_tmp = bids
                cb, p = algorithm.TMDP(bid_tmp, bids_tmp, n, m, r)
                bids.append(bid_tmp)
                # logging.info(p)
                p_all = p_all + p
            overpayment = (p_all - w) / w
            print(overpayment)
            y_sum += overpayment
            z_sum += w
        x.append(n)
        y.append(y_sum / loop)
        z.append(z_sum / loop)
    return x, y, z


if __name__ == '__main__':
    n = 500
    m = 40
    r = 3
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


