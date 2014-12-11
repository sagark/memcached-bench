from scipy.stats import genextreme, genpareto
import argparse

def key_distribution(num_samples):
    dist = genextreme(30.7984, 8.20449, 0.078688)
    return dist.rvs(num_samples)

def value_distribution(num_samples):
    dist = genpareto(0, 214.476, 0.348238)
    return dist.rvs(num_samples)

def inter_arrival_dist(num_samples):
    dist = genpareto(0, 16.0292, 0.154971)
    return dist.rvs(num_samples)

def get_keys(num_samples, dist_function, max_size = 10000):
    keys = []
    for ind in dist_function(num_samples):
        key = str(ind)
        ind = int(ind)
        for _ in range(len(key), ind):
            key += '0'
        keys.append(key)
    return keys

def main():
    parser = argparse.ArgumentParser(description='Generate values from facebook distribution')
    parser.add_argument('samples', metavar='N', type=int, nargs='+', help='number of samples')
    args = parser.parse_args()
    keys = get_keys(args.samples, key_distribution)
    values = get_keys(args.samples, value_distribution)
    IAs = get_keys(args.samples, inter_arrival_dist)

    output = []

    for i in range(len(keys)):
        output += [keys[i], values[i], IAs[i]]

    print(" ".join(output))

if __name__ == "__main__":
    main()
