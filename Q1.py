# importing necessary libraries
import random
import math

# function generateExponentialVar returns a value x which is an exponential random variable
# takes in integer lamb which is the rate parameter
def generateExponentialVar(lamb):
    # generate a random value between 0 and 1
    U = random.random()

    # using given equation, return a random exponential value
    return -(1 / lamb) * math.log(1 - U)

# function generateExponential returns an array with multiple exponential random variables
# inputs are numRuns, which is the number of times a random variable is generated
# and lamb, which is the rate parameter
# returns values and prints mean and variance
def generateExponential(numRuns, lamb):
    # initializing variables
    values = []  # array that contains the exponential random variables
    total = 0  # the cumulative count of x

    # for a given numRuns amount of time, generate a random value and add it to values array
    for i in range(numRuns):
        val = generateExponentialVar(lamb)
        values.append(val)
        total += val

    # calculate the mean
    mean = total / numRuns

    # calculate the variance
    var = 0
    for i in range(numRuns):
        total = (values[i] - mean) ** 2 / numRuns
        var += total

    print("the mean is " + str(mean))
    print("the variance is " + str(var))

    return values


if __name__ == '__main__':
    # prints mean and var of the exponential array w/ lambda = 75 with 1000 points
    generateExponential(1000, 75)
