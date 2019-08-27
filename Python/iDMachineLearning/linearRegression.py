x = []
y = []

fName = raw_input("data file? ")

with open("./" + fName, 'r') as inFile:
    for line in inFile:
        x.append(int(line.strip().split(',')[0]))
        y.append(int(line.strip().split(',')[1]))
xAvg = 0.0; yAvg = 0.0
for i in range(0, len(x)):
    xAvg += x[i]/len(x)
    yAvg += y[i]/len(x)
num = 0; den = 0
for i in range(0, len(x)):
    num += ((x[i] - xAvg) * (y[i] - yAvg))
    den += ((x[i] - xAvg)**2)
print num/den
