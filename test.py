import logging
import generator
import main
import algorithm
import time
import matplotlib.pyplot as plt
import numpy as np
logging.basicConfig(filename='log.log', level=logging.INFO)

n = 120
m = 9
r = 3

tasks = generator.generate_tasks(m)
bids = generator.generate_bids(0, tasks, n)
print(bids)
bids = generator.generate_bids(1, tasks, n)
print(bids)
bids = generator.generate_bids(2, tasks, n)
print(bids)
bids = main.generate_bids(0, tasks, n)
print(bids)

# start = time.clock()
# cb, p = algorithm.TMDP(bids[50], bids, n, m, r)
# end = time.clock()
# print('{:10.6} s', end - start)

# data to plot
n_groups = 4
means_frank = (90, 55, 40, 65)
means_guido = (85, 62, 54, 20)

# create plot
fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.35
opacity = 0.8

rects1 = plt.bar(index, means_frank, bar_width,
                 alpha=opacity,
                 color='b',
                 label='Frank')

rects2 = plt.bar(index + bar_width, means_guido, bar_width,
                 alpha=opacity,
                 color='g',
                 label='Guido')

plt.xlabel('Person')
plt.ylabel('Scores')
plt.title('Scores by person')
plt.xticks(index + bar_width / 2, ('A', 'B', 'C', 'D'))
plt.legend()

plt.tight_layout()
plt.show()

