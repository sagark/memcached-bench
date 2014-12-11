from __future__ import print_function
from scipy.stats import genextreme, genpareto
from math import floor, log10
import argparse
import random
import pylibmc
import sys

def key_distribution(num_samples):
    dist = genextreme(30.7984, 8.20449, 0.078688)
    return dist.rvs(num_samples)

def value_distribution(num_samples):
    dist = genpareto(0.348238, loc=0, scale=214.476)
    return dist.rvs(num_samples)

def inter_arrival_dist(num_samples):
    dist = genpareto(0.154971, loc=15, scale=16.0292)
    number = random.random()
    output = []
    probs = [0.00536, 0.00047, 0.17820, 0.09239, 0.00018, 0.02740, 0.00065, 0.00606, 0.00023, 0.00837, 0.08989, 0.00092, 0.00326, 0.01980]
    for i in range(num_samples):
        if number < sum(probs[0:1]):
            output.append(0)
        elif number < sum(probs[0:2]):
            output.append(1)
        elif number < sum(probs[0:3]):
            output.append(2)
        elif number < sum(probs[0:4]):
            output.append(3)
        elif number < sum(probs[0:5]):
            output.append(4)
        elif number < sum(probs[0:6]):
            output.append(5)
        elif number < sum(probs[0:7]):
            output.append(6)
        elif number < sum(probs[0:8]):
            output.append(7)
        elif number < sum(probs[0:9]):
            output.append(8)
        elif number < sum(probs[0:10]):
            output.append(9)
        elif number < sum(probs[0:11]):
            output.append(10)
        elif number < sum(probs[0:12]):
            output.append(11)
        elif number < sum(probs[0:13]):
            output.append(12)
        elif number < sum(probs[0:14]):
            output.append(13)
        elif number < sum(probs[0:15]):
            output.append(14)
        else:
            output.append(dist.rvs())
    return output

def get_keys(num_samples, dist_function, max_size = 10000):
    keys = []
    for ind in dist_function(num_samples):
        if ind < 0:
            key = str(-ind)
        else:
            key = str(ind)
        ind = max(int(ind), int(floor(log10(max_size)) + 1 ))
        key = key[:ind]
        for _ in range(len(key), ind):
            key += '0'
        keys.append(key)
    return keys

def get_IAs(num_samples):
    IAs = []
    for sample in inter_arrival_dist(num_samples):
        IAs.append(str(sample))
    return IAs

def main():
    parser = argparse.ArgumentParser(description='Generate values from facebook distribution')
    parser.add_argument('samples', metavar='N', type=int, help='number of samples')
    args = parser.parse_args()
    keys = get_keys(args.samples, key_distribution)
    values = get_keys(args.samples, value_distribution)
    IAs = get_IAs(args.samples)
    mc = pylibmc.Client(["127.0.0.1"])
    temp_dict = {}

    for i in range(len(keys)):
        temp_dict[keys[i]] = values[i]

    output = []

    for i in range(len(keys)):
        mc.set(keys[i], temp_dict[keys[i]])
        output += [keys[i], temp_dict[keys[i]], IAs[i]]

    print("\n".join(output))

if __name__ == "__main__":
    main()
