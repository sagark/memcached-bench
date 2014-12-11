import pylibmc
mc = pylibmc.Client(["172.16.1.2"])
#mc = pylibmc.Client(["127.0.0.1"])


def load():
    for x in range(200):
        res = False
        while not res:
            res = mc.set(str(x) + "hello", str(x) + "hello")
        print("sending (" + str(x) + "hello, " + str(x) + "hello)")


def check():
    for x in range(100):
        mc[str(x)+"hello"]
