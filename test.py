import generator
import main

n = 10
m = 10

tasks = generator.generate_tasks(m)
bids = generator.generate_bids(0, tasks, n)
print(bids)
bids = generator.generate_bids(1, tasks, n)
print(bids)
bids = generator.generate_bids(2, tasks, n)
print(bids)
bids = main.generate_bids(0, tasks, n)
print(bids)


