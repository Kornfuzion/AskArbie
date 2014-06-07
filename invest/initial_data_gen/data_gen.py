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

types = [(baller_proto, "baller"), (mom_proto, "mom"), (old_proto, "old"), (stock_proto, "stock"), (rounded_proto, "rounded"), (stable_proto, "stable")]
people = [(genPerson(proto), name) for proto, name in (types * 1000)]
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
    with open("first.txt", "r") as first_file:
        first = first_file.read().split()
    with open("last.txt", "r") as last_file:
        last = last_file.read().split()
    for i in range(len(last)):
        chars = [last[i][0]]
        for c in range(1,len(last[i])):
            chars.append(last[i][c].lower())
        last[i] = ''.join(chars)
    return (first, last)

aboutAll()

first, last = getNames()

from invest.models import RBC_Customer

for i, p in enumerate(people):
    args = {"investmentData_%s" % n : v for n,v in enumerate(p[0])}
    f = first[random.randint(0, len(first)-1)]
    l = last[random.randint(0, len(last)-1)]
    args["name"] = "%s %s" % (f, l)
    args["income"] = 0
    args["clusterID"] = idx[i]

    c = RBC_Customer(**args)
    
    c = RBD_Customer
