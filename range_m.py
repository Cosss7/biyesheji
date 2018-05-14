import logging
import generator
import algorithm
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.font_manager import FontProperties

def range_m(op):
    x = []
    y = []
    z = []
    for m in range(10, 60, 10):
        y_sum = 0
        z_sum = 0
        loop = 20
        for i in range(0, loop):
            tasks = generator.generate_tasks(m)
            bids = generator.generate_bids(op, tasks, n)
            bids_tmp = bids
            res = algorithm.WDBP(tasks, bids_tmp, r, n)
            s = res[0]
            w = res[1]
            # logging.info(w)
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
                # logging.info(p)
                p_all = p_all + p
            overpayment = (p_all - w) / w
            # logging.info(overpayment)
            y_sum += overpayment
            z_sum += w
        x.append(m)
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
    plt.xlabel(u'传感任务数量 $m$', fontproperties=myfont)
    x, y, z = range_m(0)
    zz.append(z)
    plt.plot(x, y, "-^", mfc='none', label=u'均匀分布')

    x, y, z = range_m(1)
    zz.append(z)
    plt.plot(x, y, "-o", mfc='none', label=u'正态分布')

    x, y, z = range_m(2)
    zz.append(z)
    plt.plot(x, y, "-s", mfc='none', label=u'指数分布')

    plt.legend(loc='best', prop=myfont)
    plt.savefig('Overpayment ratio vs. Number of sensing tasks.png')
    plt.show()

    plt.figure(2)
    plt.ylabel(u'社会成本 $\omega$', fontproperties=myfont)
    plt.xlabel(u'传感任务数量 $m$', fontproperties=myfont)
    plt.plot(x, zz[0], "-^", mfc='none', label=u'均匀分布')
    plt.plot(x, zz[1], "-o", mfc='none', label=u'正态分布')
    plt.plot(x, zz[2], "-s", mfc='none', label=u'指数分布')
    plt.legend(loc='best', prop=myfont)
    plt.savefig('Social cost vs. Number of Number of sensing tasks.png')
    plt.show()



