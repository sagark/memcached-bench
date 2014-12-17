import numpy as np
from pylab import *
import argparse

blah = 91

parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('filename', metavar='N', type=str,
                           help='an integer for the accumulator')
parser.add_argument('title', metavar='N', type=str,
                           help='an integer for the accumulator')

args = parser.parse_args()

a = file(args.filename + "_accel");
e = file(args.filename + "_no_accel");

s = []
t = []

b = a.readlines()
f = e.readlines()

for x in b:
    s.append(int(x.split(" ")[1].replace("\n", "")))

for y in f:
    t.append(int(y.split(" ")[1].replace("\n", "")))

print sum(s)/ (1.0*len(s))
print sum(t) / (1.0*len(t))

a = list(range(0, blah))
e = list(range(0, blah))

s = np.array(s)
t = np.array(t)

print("PERCENTILES: (ACCEL FIRST)")
print(np.percentile(s, 50))
print(np.percentile(t, 50))

percentiless = []
percentiles = []
for x in range(blah):
    percentiless.append(np.percentile(s, x))
    percentiles.append(np.percentile(t, x))

print(a)
print(e)
print(percentiless)
print(percentiles)


print("MAXES:")
print(max(s))
print(max(t))

plot(a, percentiless)
plot(e, percentiles)
xlabel("Percentiles")
ylabel(u"Latency (\u03bcs)")
#yscale('log')
title(args.title)
#grid(True)
savefig(args.filename + ".pdf")
show()
