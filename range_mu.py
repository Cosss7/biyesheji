import logging
import generator
import algorithm
import matplotlib.pyplot as plt
import time
import numpy as np
import matplotlib
from matplotlib.font_manager import FontProperties
logging.basicConfig(filename='log.log', level=logging.INFO)


def range_mu(op):
    # x -- n, y -- overpayment ratio, z -- social cost.
    x = []
    y = []
    z = []
    for mu in range(0, 3):
        # print('in n = ' + str(n))
        y_sum = 0
        z_sum = 0
        loop = 20
        for i in range(0, loop):
            # print('in loop ' + str(i))
            tasks = generator.generate_tasks(m)
            bids = generator.generate_bids_mu(op, tasks, n, mu)
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
    x, y0, z0 = range_mu(0)
    x, y1, z1 = range_mu(1)
    x, y2, z2 = range_mu(2)

    n_groups = 3
    index = np.arange(n_groups)
    bar_width = 0.25
    opacity = 0.8

    rects1 = plt.bar(index, y0, bar_width,
                     alpha=opacity,
                     label=u'均匀分布')

    rects2 = plt.bar(index + bar_width, y1, bar_width,
                     alpha=opacity,
                     label=u'正态分布')

    rects3 = plt.bar(index + 2 * bar_width, y2, bar_width,
                     alpha=opacity,
                     label=u'指数分布')

    plt.xlabel(u'真实成本的平均数', fontproperties=myfont)
    plt.ylabel(u'超额偿付率 $\lambda$', fontproperties=myfont)
    # plt.title('Scores by person')
    plt.xticks(index + bar_width, ('15', '20', '25'))
    plt.legend(prop=myfont)

    plt.tight_layout()
    plt.savefig('Overpayment ratio vs. Cost range R.png')
    plt.show()


    plt.figure(2)
    plt.bar(index, z0, bar_width,
                     alpha=opacity,
                     label=u'均匀分布')

    plt.bar(index + bar_width, z1, bar_width,
                     alpha=opacity,
                     label=u'正态分布')

    plt.bar(index + 2 * bar_width, z2, bar_width,
                     alpha=opacity,
                     label=u'指数分布')

    plt.xlabel(u'真实成本的平均数', fontproperties=myfont)
    plt.ylabel(u'社会成本 $\omega$', fontproperties=myfont)
    # plt.title('Scores by person')
    plt.xticks(index + bar_width, ('15', '20', '25'))
    plt.legend(prop=myfont)

    plt.tight_layout()
    plt.savefig('Social cost vs. Cost range R.png')
    plt.show()



