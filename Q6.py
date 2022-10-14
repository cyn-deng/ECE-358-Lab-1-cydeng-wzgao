# importing necessary libraries
import random
import math
import matplotlib.pyplot as plt
import datetime
from collections import deque


# function generateExponentialVar returns a value x which is an exponential random variable
# takes in integer lamb which is the rate parameter
def generateExponentialVar(lamb):
    # generate a random value between 0 and 1
    U = random.random()

    # using given equation, return a random exponential value
    return -(1 / lamb) * math.log(1 - U)


# populateArrays generates the arrays that contain packet arrivals, packet departures, and observations
def populateArrays(lamb, lambL, C, T, k):
    # initializing variables
    all_packet_arrivals = []  # array that will carry all the packet arrival times
    packet_length = []  # array that contains all packet lengths
    packet_departure = []  # array that contains packet departure times
    observations = []  # array that contains observation times
    total_lost = 0  # counter of total packets lost
    departure_queue = deque()  # queue that will be used to simulate finite size
    actual_packet_arrivals = []  # array that will contain all the packet arrival times that weren't lost
    total_created = 0  # variable to keep track of total created packets for P Loss

    arrival_time = 0  # cumulative value of all random exponential values for arrival time
    observation_time = 0  # cumulative value of all random exponential values for observation time

    # for a simulation time, generate arrival times and packet lengths until arrival time exceeds simulation time
    while arrival_time < T:
        arrival_time += generateExponentialVar(lamb)
        all_packet_arrivals.append(arrival_time)

        # since there is a 1 to 1 for arrival time and packet length,
        # we can generate one random length for every one arrival time
        packet_length.append(generateExponentialVar(lambL))

    # for observation time, we do the same thing as arrival time, except with a rate 5 times faster
    while observation_time < T:
        observation_time += generateExponentialVar(lamb * 5)
        observations.append(observation_time)

    # with given information about arrival time and packet length, we can now calculate the departure times
    # and since there is a 1 to 1 for arrivals and departures,
    # we will also be doing as many iterations as there are arrival times
    for i in range(len(all_packet_arrivals)):

        # calculate the service time given a single packet length and C value
        service_time = packet_length[i] / C

        a_i = all_packet_arrivals[i]

        # process and add run through the departure queue until the arrival time is greater than the first
        # element of the queue or until the queue is empty
        while len(departure_queue) != 0 and departure_queue[0] <= a_i:
            departure = departure_queue.popleft()
            packet_departure.append(departure)
        # for every iteration that is not the first one, we will perform the following calculation

        # if the departure queue is full, skip the iteration and increment the total packets lost by 1
        if len(departure_queue) == k:
            total_lost += 1
            continue
        else:
            if i > 0 and len(departure_queue) != 0:
                # d_i0 is set as the last element in the departure queue
                d_i0 = departure_queue[-1]

                # if the current arrival time is greater than the last departure time in the queue,
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
            departure_queue.append(departure)  # add the departure time to the queue
            actual_packet_arrivals.append(a_i)  # add the arrival time to successfully processed arrival times
        total_created = len(all_packet_arrivals)

    return packet_departure, actual_packet_arrivals, observations, total_lost, total_created


# createDES takes in 3 arrays that contain packet arrival times, packet departure times,
# and observation times the output is an array of dictionaries
def createDES(p_a, p_d, o):
    # initialize DES array which is going to carry the dictionaries
    DES = []

    # for every value found in p_a
    for i in range(len(p_a)):
        # append a dictionary that contains Arrival as the event type, with it's corresponding value
        DES.append({"type": "Arrival", "time": p_a[i]})

    # the same thing that was done for p_a is done for p_d and o
    for i in range(len(p_d)):
        DES.append({"type": "Departure", "time": p_d[i]})

    for i in range(len(o)):
        DES.append({"type": "Observation", "time": o[i]})

    # sort the dictionaries in the array based on the time value in ascending order
    newDES = sorted(DES, key=lambda x: x["time"], reverse=False)

    # returns the sorted DES array
    return newDES


# queueProcessing takes in an array DES and integer T for simulation time
# the outputs are values for E_N and P_IDLE
def queueProcessing(DES, T, total_lost, total_created_packets):
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
    E_N = total_packets / N_o
    P_IDLE = idle / N_o
    P_LOSS = total_lost / total_created_packets

    return E_N, P_IDLE, P_LOSS


# oneSimulation calls the previous 3 functions in order to generate 1 value of E_N and P_IDLE
def oneSimulation(lamb, avg_l, C, T, K):
    lambL = 1 / avg_l  # calculating the lambda needed to generate random lengths

    # generating arrays packet_departure, packet_arrivals, and observations
    # takes in 4 integer inputs: lamb, lambL, C, and T
    packet_departure, packet_arrivals, observations, total_lost_count, total_packets_created = \
        populateArrays(lamb, lambL, C, T, K)

    # generating 2 arrays: eventTypes, and DES
    # takes in 3 array inputs: packet_arrivals, packet_departure, observations
    DES = createDES(packet_arrivals, packet_departure, observations)

    # generating E_N, and P_IDLE
    # takes in 2 array inputs: eventTypes
    E_N, P_IDLE, P_LOSS = queueProcessing(DES, T, total_lost_count, total_packets_created)

    return E_N, P_IDLE, P_LOSS


if __name__ == '__main__':
    # initializing variables
    avg_l = 2000  # average length of packets in bit
    C = 10 ** 6  # transmission rate of output link in bits per second
    T = 2000  # the total time for simulation

    f1 = plt.figure()
    f2 = plt.figure()
    ax1 = f1.add_subplot(1, 1, 1)
    ax2 = f2.add_subplot(1, 1, 1)
    ax1.set_xlabel('rho')
    ax1.set_ylabel('E[N]')
    ax1.set_title("E[n] vs rho")

    ax2.set_xlabel('rho')
    ax2.set_ylabel('P_LOSS')
    ax2.set_title("P_LOSS vs rho")

    for K in [10, 25, 50]:
        ENArray = []
        PLOSSArray = []
        rhoArray = []
        for j in range(50, 160, 10):
            rho = j / 100  # utilization of queue
            lamb = (C * rho) / avg_l  # average number of packets generated / second

            # calls one iteration of the simulation to output one pair of E[N] and P_IDLE
            E_N, P_IDLE, P_LOSS = oneSimulation(lamb, avg_l, C, T, K)

            # append the values onto an array to later graph
            ENArray.append(E_N)
            PLOSSArray.append(P_IDLE)
            rhoArray.append(rho)

        # create two subplots so that both E[N] and P_IDLE plot at the same time

        # setting up figure 1 for E[N] vs rho
        ax1.plot(rhoArray, ENArray, label="K=" + str(K))

        # setting up figure 2 for P_IDLE vs rho
        ax2.plot(rhoArray, PLOSSArray, label="K=" + str(K))

    ax1.legend()
    ax2.legend()
    plt.show()
    f1.savefig("E[n] vs rho for Finite Buffer.png")
    f1.savefig("P_LOSS vs rho for Finite Buffer.png")
    plt.close()
