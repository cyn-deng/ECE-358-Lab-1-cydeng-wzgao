# importing necessary libraries
import random
import math
import matplotlib.pyplot as plt
import datetime

# function generateExponentialVar returns a value x which is an exponential random variable
# takes in integer lamb which is the rate parameter
def generateExponentialVar(lamb):
    # generate a random value between 0 and 1
    U = random.random()

    # using given equation, return a random exponential value
    return -(1 / lamb) * math.log(1 - U)

# populateArrays generates the arrays that contain packet arrivals, packet departures, and observations
def populateArrays(lamb, lambL, C, T):
    # initializing variables
    packet_arrivals = []  # array that will carry all the packet arrival times
    packet_length = []  # array that contains all packet lengths
    packet_departure = []  # array that contains packet departure times
    observations = []  # array that contains observation times

    arrival_time = 0  # cumulative value of all random exponential values for arrival time
    observation_time = 0  # cumulative value of all random exponential values for observation time

    # for a simulation time, generate arrival times and packet lengths until arrival time exceeds simulation time
    while arrival_time < T:

        arrival_time += generateExponentialVar(lamb)
        packet_arrivals.append(arrival_time)

        # since there is a 1 to 1 for arrival time and packet length,
        # we can generate one random length for every one arrival time
        packet_length.append(generateExponentialVar(lambL))

    # for observation time, we do the same thing as arrival time, except with a rate 5 times faster
    while observation_time < T:
        observation_time += generateExponentialVar(lamb*5)
        observations.append(observation_time)

    # with given information about arrival time and packet length, we can now calculate the departure times
    # and since there is a 1 to 1 for arrivals and departures,
    # we will also be doing as many iterations as there are arrival times
    for i in range(len(packet_arrivals)):

        # calculate the service time given a single packet length and C value
        service_time = packet_length[i]/C

        a_i = packet_arrivals[i]

        # for every iteration that is not the first one, we will perform the following calculation
        if i > 0:
            # d_i0 is set as the previous departure time
            d_i0 = packet_departure[i-1]

            # if the current arrival time is greater than the previous departure time,
            # that means we can just add the service time of the current package to arrival time
            # in order to determine the departure time of the package
            if a_i > d_i0:
                departure = a_i + service_time
            # otherwise, departure time of the current package is given by the sum of the
            # previous departure time and the current service time
            else:
                departure = d_i0 + service_time
        else:  # for the first iteration, it will be a simple addition of arrival time and service time
            departure = a_i + service_time

        # add the departure value to the departure time array
        packet_departure.append(departure)

    return packet_departure, packet_arrivals, observations

# createDES takes in 3 arrays that contain packet arrival times, packet departure times,
# and observation times the output is an array of dictionaries
def createDES(p_a, p_d, o):

    DES = []

    for i in range(len(p_a)):
        DES.append({"type": "Arrival", "time": p_a[i]})

    for i in range(len(p_d)):
        DES.append({"type": "Departure", "time": p_d[i]})

    for i in range(len(o)):
        DES.append({"type": "Observation", "time": o[i]})

    newDES = sorted(DES, key=lambda x: x["time"], reverse=False)

    return newDES

def queueProcessing(DES, T):

    # initialize variables
    N_a = 0  # Number of arrivals
    N_d = 0  # Number of departures
    N_o = 0  # Number of observations
    idle = 0  # idle counter
    total_packets = 0  # total packets processed counter
    i = 0  # used later to iterate

    # while the iteration counter is less than the length of DES,
    # and the value of DES is less than simulation time, perform the following code
    while i < len(DES) and DES[i]['time'] < T:

        # based on event type, increment the correct counter
        if DES[i]['type'] == "Arrival":
            N_a += 1
        elif DES[i]['type'] == "Departure":
            N_d += 1
        else:
            N_o += 1

            # idle is incremented if there are no packets in queue, used to calculate P_IDLE
            if N_d == N_a:
                idle += 1

            # used for calculating E[N], cumulating packets in the queue at observation times
            total_packets += (N_a - N_d)
        i += 1

    # calculating E[N] and P_IDLE
    E_N = total_packets/N_o
    P_IDLE = idle/N_o

    return E_N, P_IDLE

def oneSimulation(lamb, avg_l, C, T):
    lambL = 1/avg_l  # calculating the lambda needed to generate random lengths

    # generating arrays packet_departure, packet_arrivals, and observations
    # takes in 4 integer inputs: lamb, lambL, C, and T
    packet_departure, packet_arrivals, observations = populateArrays(lamb, lambL, C, T)

    # generating 2 arrays: eventTypes, and DES
    # takes in 3 array inputs: packet_arrivals, packet_departure, observations
    DES = createDES(packet_arrivals, packet_departure, observations)

    # generating E_N, and P_IDLE
    # takes in 2 array inputs: eventTypes
    E_N, P_IDLE = queueProcessing(DES, T)

    return E_N, P_IDLE


if __name__ == '__main__':

    # initializing variables
    avg_l = 2000  # average length of packets in bit
    C = 10**6  # transmission rate of output link in bits per second
    T = 2000  # the total time for simulation

    # initializing arrays that keep track of E[N], P_IDLE, and rho
    ENArray = []
    PIDLEArray = []
    rhoArray = []

    for i in range(25, 96, 10):
        rho = i/100  # utilization of queue
        lamb = (C*rho)/avg_l  # average number of packets generated / second

        E_N, P_IDLE = oneSimulation(lamb, avg_l, C, T)

        ENArray.append(E_N)
        PIDLEArray.append(P_IDLE)
        rhoArray.append(rho)

    print(ENArray)
    print(PIDLEArray)

    f1 = plt.figure()
    f2 = plt.figure()

    ax1 = f1.add_subplot(111)
    ax1.plot(rhoArray, ENArray)
    ax1.set_xlabel('rho')
    ax1.set_ylabel('E[N]')
    ax1.set_title("E[n] vs rho")

    ax2 = f2.add_subplot(111)
    ax2.plot(rhoArray, PIDLEArray)
    ax2.set_xlabel('rho')
    ax2.set_ylabel('P_IDLE')
    ax2.set_title("P_IDLE vs rho")

    plt.show()

