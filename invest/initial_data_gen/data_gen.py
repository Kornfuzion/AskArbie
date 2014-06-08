def go():
    import random
    import numpy
    import scipy.cluster.vq
    from collections import Counter

    mutual_funds = ["%s risk %s term mutual fund" % (risk, term) for risk in ["High", "Low"] for term in ["short", "long"]]
    bonds = ["Bond A", "Bond B", "Bond C"]
    gics = ["GIC %s" % (enum) for enum in ["A", "B", "C"]]
    stocks = ["%s risk stock in industry %s" % (risk, industry) for risk in ["High", "Medium", "Low"] for industry in ["A", "B", "C"]]

    investments = stocks + mutual_funds + gics + bonds

    baller_proto = [([0,1,2],(10,30)) , ([3,4,5],(10,30)) , ([9,10],(10,30)) , ([11,12],(10,30))]
    mom_proto = [([16,17,18],(10,30)) , ([13,14,15],(20,40)) , ([11,12],(30,50)) , ([9,10],(10,20)), ([6,7,8],(5,10))]
    old_proto = [([13,14,15],(10,20)) , ([13,14,15],(10,20)) , ([11,12],(10,20))]
    stock_proto = [([0,1,2,3,4,5,6,7,8],(20,30)),
                   ([0,1,2,3,4,5,6,7,8],(20,30)),
                   ([0,1,2,3,4,5,6,7,8],(20,30)),
                   ([0,1,2,3,4,5,6,7,8],(20,30)),
                   ([0,1,2,3,4,5,6,7,8],(20,30)),
                   ([0,1,2,3,4,5,6,7,8],(20,30)),
                   ([0,1,2,3,4,5,6,7,8],(20,30)),
                   ([13,14,15,16,17,18],(165,185))]
    rounded_proto = [([3,4,5],(5,10)), ([6,7,8],(5,10)), ([9,10],(20,25)),
                     ([11,12],(25,30)), ([16,17,18],(20,30)), ([16,17,18],(20,30))]
    stable_proto = [([11,12],(10,50)), ([11,12],(10,50))]


    numInv = len(investments)

    def genPerson(proto):
        person = [0] * numInv
        for options, rng in proto:
            opt = None
            while opt is None or person[opt] != 0:
                opt = options[random.randint(0, len(options)-1)]
            low, high = rng
            val = random.uniform(low, high)
            person[opt] = val
        total = sum(person)
        return [x/total for x in person]
        
    def printPerson(person):
        for inv, percent in zip(investments, person):
            print round(percent * 100, 1), inv

    def printInv():
        for i, inv in enumerate(investments):
            print i, inv

    def genIncome(rng):
        low, high = rng
        return random.uniform(low, high)

    types = [(baller_proto, "baller"), (mom_proto, "mom"), (old_proto, "old"), (stock_proto, "stock"), (rounded_proto, "rounded"), (stable_proto, "stable")]
    incomeRanges = {"baller":(100000,500000), "mom":(40000, 70000), "old":(60000, 80000),
                    "stock":(80000, 100000), "rounded":(50000, 100000), "stable":(50000,60000)}
    people = [(genPerson(proto), name, genIncome(incomeRanges[name])) for proto, name in (types * 1000)]
    pa = numpy.array(people)
        
    data = numpy.array([person[0] for person in people])
    data = scipy.cluster.vq.whiten(data)
    centroids,_ = scipy.cluster.vq.kmeans(data, 6)
    idx,_ = scipy.cluster.vq.vq(data, centroids)

    def aboutAll():
        for c in range(len(types)):
            print Counter(pa[idx==c,1])

    def about(cluster):
        for i in range(len(investments)):
            array = numpy.array([p[i] for p in cluster])
            mean = round(numpy.mean(array) * 100, 1)
            std = round(numpy.std(array) * 100, 1)
            print investments[i], mean, std

    def getNames():
        with open("/home/james/mysite/invest/initial_data_gen/first.txt", "r") as first_file:
            first = first_file.read().split()
        with open("/home/james/mysite/invest/initial_data_gen/last.txt", "r") as last_file:
            last = last_file.read().split()
        for i in range(len(last)):
            chars = [last[i][0]]
            for c in range(1,len(last[i])):
                chars.append(last[i][c].lower())
            last[i] = ''.join(chars)
        return (first, last)

    aboutAll()

    first, last = getNames()

    def genStockInfo(target, volatility, points=20):
        linear = [(float(target) / (points-2)) * i for i in range(points-1)]
        return [0] + [x + random.uniform(0, volatility) for x in linear]

    roi = [0] * len(investments)
    roi[0] = genStockInfo(-10, 4)
    roi[1] = genStockInfo(10, 4)
    roi[2] = genStockInfo(15, 4)
    roi[3] = genStockInfo(-3, 4)
    roi[4] = genStockInfo(7, 4)
    roi[5] = genStockInfo(-7, 4)
    roi[6] = genStockInfo(4, 2)
    roi[7] = genStockInfo(-4, 2)
    roi[8] = genStockInfo(2, 1)
    roi[9] = genStockInfo(5, 4)
    roi[10] = genStockInfo(-5, 4)
    roi[11] = genStockInfo(3, 1)
    roi[12] = genStockInfo(1, 1)
    roi[13] = genStockInfo(0.5, 0.1)
    roi[14] = genStockInfo(1.5, 0.1)
    roi[15] = genStockInfo(1, 0.1)
    roi[16] = genStockInfo(0.5, 0.1)
    roi[17] = genStockInfo(1.5, 0.1)
    roi[18] = genStockInfo(1, 0.1)

    risk = [0] * len(investments)
    risk[0] = 100
    risk[1] = 100
    risk[2] = 100
    risk[3] = 70
    risk[4] = 70
    risk[5] = 70
    risk[6] = 40
    risk[7] = 40
    risk[8] = 40
    risk[9] = 30
    risk[10] = 30
    risk[11] = 20
    risk[12] = 20
    risk[13] = 10
    risk[14] = 10
    risk[15] = 10
    risk[16] = 10
    risk[17] = 10
    risk[18] = 10

    def getRisk(person):
        return sum([r * p for r, p in zip(risk, person)])

    def getRoi(person):
        return [sum([r[i] * p for r, p in zip(roi, person)]) for i in range(20)]

    from invest.models import RBC_Customer
    from invest.models import Investment_History

    for i, p in enumerate(people):
        args = {"investmentData_%s" % (n+1) : v for n,v in enumerate(p[0])}
        f = first[random.randint(0, len(first)-1)]
        l = last[random.randint(0, len(last)-1)]
        args["userName"] = "%s %s" % (f, l)
        args["income"] = p[2]
        args["clusterID"] = idx[i]

        personalRoi = getRoi(p[0])
        for n in range(20):
            args["roi_%s" % (n+1)] = personalRoi[n]
        args["risk"] = getRisk(p[0])

        c = RBC_Customer(**args)
        c.save()

    for i, inv in enumerate(investments):
        args = {}
        for n in range(20):
            args["roi_%s" % (n+1)] = roi[i][n]
        args["risk"] = risk[i]
        args["name"] = inv

        obj = Investment_History(**args)
        obj.save()
        


