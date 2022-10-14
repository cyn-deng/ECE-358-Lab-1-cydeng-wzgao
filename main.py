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

if __name__ == '__main__':
    # prints mean and var of the exponential array w/ lambda = 75
    generateExponential(1000, 75)