import numpy as np
from pylab import *


a = file("out");

h = []
s = []

b = a.readlines()

for x in b:
    if "h" in x:
        h.append(int(x.split(" ")[1].replace("\n", "")))
    else:
        s.append(int(x.split(" ")[1].replace("\n", "")))



print sum(h)/ (1.0*len(h))
print sum(s)/ (1.0*len(s))

a = list(range(0, 110, 10))
h = np.array(h)
s = np.array(s)

print(np.percentile(h, 50))
print(np.percentile(s, 50))

percentilesh = []
percentiless = []
for x in range(11):
    percentilesh.append(np.percentile(h, 10*x))
    percentiless.append(np.percentile(s, 10*x))

print(a)
print(percentilesh)
print(percentiless)


print("MAXES:")
print(max(h))
print(max(s))


plot(a, percentilesh)
plot(a, percentiless)
grid(True)
savefig("test.png")
show()
