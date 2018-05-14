import logging
import generator
import algorithm
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.font_manager import FontProperties
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
    myfont = FontProperties(
        fname='/usr/share/fonts/truetype/wqy/wqy-microhei.ttc')
    # 解决负号'-'显示为方块的问题
    matplotlib.rcParams['axes.unicode_minus'] = False

    plt.figure(1)
    zz = []
    plt.ylabel(u'超额偿付率 $\lambda$', fontproperties=myfont)
    plt.xlabel(u'智能手机用户数量 $n$', fontproperties=myfont)
    x, y, z = range_n(0)
    zz.append(z)
    plt.plot(x, y, "-^", mfc='none', label=u'均匀分布')

    x, y, z = range_n(1)
    zz.append(z)
    plt.plot(x, y, "-o", mfc='none', label=u'正态分布')

    x, y, z = range_n(2)
    zz.append(z)
    plt.plot(x, y, "-s", mfc='none', label=u'指数分布')

    plt.legend(loc='best', prop=myfont)
    plt.savefig('Overpayment ratio vs. Number of smartphones.png')
    plt.show()

    plt.figure(2)
    plt.ylabel(u'社会成本 $\omega$', fontproperties=myfont)
    plt.xlabel(u'智能手机用户数量 $n$', fontproperties=myfont)
    plt.plot(x, zz[0], "-^", mfc='none', label=u'均匀分布')
    plt.plot(x, zz[1], "-o", mfc='none', label=u'正态分布')
    plt.plot(x, zz[2], "-s", mfc='none', label=u'指数分布')
    plt.legend(loc='best', prop=myfont)
    plt.savefig('Social cost vs. Number of smartphones.png')
    plt.show()


