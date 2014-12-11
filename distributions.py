from scipy.stats import genextreme, genpareto


def key_distribution(num_samples):
    dist = genextreme(30.7984, 8.20449, 0.078688)
    return dist.rvs(num_samples)

def value_distribution(num_samples):
    dist = genpareto(0, 214.476, 0.348238)
    return dist.rvs(num_samples)

def inter_arrival_dist(num_samples):
    dist = genpareto(0, 16.0292, 0.154971)
    return dist.rvs(num_samples)


def gen_dist(num_samples):
    a = key_distribution(num_samples)
    b = value_distribution(num_samples)
    c = inter_arrival_dist(num_samples)

