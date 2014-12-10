import pylibmc
mc = pylibmc.Client(["172.16.1.2"])
#mc = pylibmc.Client(["127.0.0.1"])


def load():
    for x in range(200):
        mc[str(x)] = str(x)


def check():
    for x in range(100):
        mc[str(x)]
