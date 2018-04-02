import csv
import time

with open('1.txt', 'r') as f:
  reader = csv.reader(f)
  your_list = list(reader)

print(your_list[0][1])

a = your_list[0][1]
b = your_list[1][1]

print(a - b)


print(your_list)




