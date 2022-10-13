import random
import math

def generateExponentialVar(lamb):
    U = random.random()

    return -(1/lamb)*math.log(1-U)

def generateExponential(numRuns, lamb):
    values = []
    sum = 0
    for i in range(numRuns):
        val = generateExponentialVar(lamb)
        values.append(val)
        sum += val
    mean = sum / numRuns
    var = 0
    for i in range(numRuns):
        sum = (values[i]-mean)**2/numRuns
        var += sum
    print(mean, var)

    return values

def packetArrival(lamb):


def queue(avg_l, T, C):
    lamb_L = 1/avg_l
    lamb_T = 1/T
    departure = [0]
    packet_length = []
    packet_arrival = packetArrival(lamb_T)
    i = 0
    while (departure[-1] < T):

if __name__ == '__main__':
    # prints mean and var of the exponential array w/ lambda = 75
    generateExponential(1000, 75)