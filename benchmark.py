import logging
import time

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties

import algorithm
import generator

logging.basicConfig(filename='log.log', level=logging.INFO)


def TRAC(n, m):
    y_sum = 0
    z_sum = 0
    # print('in loop ' + str(i))
    tasks = generator.generate_tasks(m)
    bids = generator.generate_bids(0, tasks, n)
    bids_tmp = bids
    s, w = algorithm.WDBP(tasks, bids_tmp, r, n)
    print(s)
    print(w)
    # compute payment.
    p_all = 0
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
    y_sum /= loop
    z_sum /= loop


def OPT(n, m):
    tasks = generator.generate_tasks(m)
    bids = generator.generate_bids(0, tasks, n)
    print(len(bids))
    algorithm.dfs(tasks, bids, r, [], 0)


if __name__ == '__main__':
    n = 500
    m = 40
    r = 3
    y1 = []
    y2 = []
    for n in range(100, 130, 10):
        for m in range(8, 10):
            t1 = 0
            t2 = 0
            loop = 5
            for i in range(0, loop):
                start = time.clock()
                TRAC(n, m)
                end = time.clock()
                print('%.6f s', end - start)
                t1 += (end - start) * 1000
            for i in range(0, loop):
                start = time.clock()
                OPT(n, m)
                end = time.clock()
                print('%.6f s', end - start)
                t2 += (end - start) * 1000
            y1.append(t1 / loop)
            y2.append(t2 / loop)

    # data to plot
    n_groups = 6
    means_frank = (90, 55, 40, 65)
    means_guido = (85, 62, 54, 20)

    myfont = FontProperties(
        fname='/usr/share/fonts/truetype/wqy/wqy-microhei.ttc')
    # 解决负号'-'显示为方块的问题
    matplotlib.rcParams['axes.unicode_minus'] = False

    # create plot
    fig, ax = plt.subplots()
    ax.set_yscale('log')
    index = np.arange(n_groups)
    bar_width = 0.35
    opacity = 0.8

    rects1 = plt.bar(index, y1, bar_width,
                     alpha=opacity,
                     color='b',
                     label=u'实验')

    rects2 = plt.bar(index + bar_width, y2, bar_width,
                     alpha=opacity,
                     color='g',
                     label=u'对照')

    plt.xlabel(u'对于 n, m 不同的设置', fontproperties=myfont)
    plt.ylabel(u'运行时间 (毫秒)', fontproperties=myfont)
    # plt.title('Scores by person')
    plt.xticks(index + bar_width / 2,
               ('{100,8}', '{100,9}', '{110,8}', '{110,9}', '120,8', '120,9'))
    plt.legend(prop=myfont)

    plt.tight_layout()
    plt.savefig('Evaluation of computation efficiency.png')
    plt.show()
