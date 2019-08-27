import numpy as np
x = []
y = []

fName = raw_input("data file? ")

with open("./" + fName, 'r') as inFile:
    for line in inFile:
        x.append(float(line.strip().split(',')[0]))
        y.append(float(line.strip().split(',')[1]))

for i in range(0, len(x)):
    x[i] = ((x[i]-min(x))/(max(x)-min(x)))
    y[i] = ((y[i]-min(y))/(max(y)-min(y)))

centers = []
n = input("number of centers")
for i in range(n):
    centers.append([np.random.rand(), np.random.rand()])
print centers

for i in range(0, 100000):
    groups = []
    for j in range(n):
        groups.append([])
    for j in range(0, len(x)):
        distances = []
        for k in range(0, n):
            distances.append(np.sqrt((centers[k][0] - x[j])**2 + (centers[k][1] - y[j])**2))
        groups[distances.index(min(distances))].append(j)
    for j in range(len(groups)):
        xAvg = 0
        yAvg = 0
        for k in groups[j]:
            xAvg += x[k]
            yAvg += y[k]
        if len(groups[j]) != 0:
            xAvg /= len(groups[j])
            yAvg /= len(groups[j])
        centers[j] = [xAvg, yAvg]
    if i%1000 == 0:
        print centers
            
