import numpy as np
from pylab import *

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

hfile = file("output_data/accelerator_onekey_94hello");
sfile = file("output_data/software_onekey_94hello");

h = []
s = []

bh = hfile.readlines()
bs = sfile.readlines()

for x in bh:
    h.append(int(x.split(" ")[1].replace("\n", "")))

for x in bs:
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

a = a[0:-1]
percentilesh = percentilesh[0:-1]
percentiless = percentiless[0:-1]


print(a)
print(percentilesh)
print(percentiless)


print("MAXES:")
print(max(h))
print(max(s))

title("Get Request Latency")
xlabel("Percentile")
ylabel("Latency (us)")
plot(a, percentilesh)
plot(a, percentiless)
grid(True)
green_patch = mpatches.Patch(color='green', label='Requests served by memcached on Rocket')
blue_patch = mpatches.Patch(color='blue', label='Requests served by accelerator')

legend(handles=[green_patch, blue_patch]) #bbox_to_anchor=(1, 0), bbox_transform=plt.gcf().transFigure)

#legend( handles=[red_patch, blue_patch],  bbox_to_anchor=(1, 1),
#           bbox_transform=plt.gcf().transFigure)


#handles, labels = get_legend_handles_labels()
#legend(handles, labels)


savefig("test.png")
show()
