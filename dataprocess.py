import numpy as np
from pylab import *


a = file("out");

s = []

b = a.readlines()

for x in b:
    s.append(int(x.split(" ")[1].replace("\n", "")))

print sum(s)/ (1.0*len(s))

a = list(range(0, 110, 10))
s = np.array(s)

print(np.percentile(s, 50))

percentiless = []
for x in range(11):
    percentiless.append(np.percentile(s, 10*x))

print(a)
print(percentiless)


print("MAXES:")
print(max(s))


plot(a, percentiless)
grid(True)
savefig("test.png")
show()
