import pylibmc
mc = pylibmc.Client(["172.16.1.2"])
#mc = pylibmc.Client(["127.0.0.1"])


def load():
    res = False
    while not res:
        res = mc.set("a", "0")

    for x in range(200):
        res = False
        while not res:
            res = mc.set(str(x) + "hello", str(x) + "hello2")
        print("sending (" + str(x) + "hello, " + str(x) + "hello2)")


def check():
    mc['a']
    for x in range(100):
        mc[str(x)+"hello"]
