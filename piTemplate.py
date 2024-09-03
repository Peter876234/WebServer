import os
import json
import socket
import threading
import random, multiprocessing,timeit
from random import random
from flask import Flask, request, jsonify

def partition(simulations, concurrency):
    size = simulations // concurrency # partition size, except for last partition
    starts = list(range(0, simulations+1, size))[0:concurrency] # p start values
    stops = list(range(0, simulations+1, size))[1:concurrency] + [simulations+1] # p stop values
    return list(zip(starts, stops))

def count_in_circle(size, results):
    count = 0
    for i in range(size):
        x = random()
        y = random()
        if x * x + y * y < 1:
            count += 1
    results.put(count)

def pi_processes(simulations, concurrency):
    start_time = timeit.default_timer()
    results = multiprocessing.Queue() # shared memory
    processes = []
    for start, stop in partition(simulations, concurrency):
        size = stop - start
        process = multiprocessing.Process(
        target=count_in_circle, args=[size, results])
        processes.append(process)
    for pr in processes: pr.start() 
    for pr in processes: pr.join()
    sum_ = 0
    while not results.empty():
        sum_ += results.get()
    pi = sum_ / simulations * 4
    end_time = timeit.default_timer()
    return pi, end_time-start_time

if __name__ == "__main__":
    for i in range(1,9):
        print(i,pi_processes(int(100000000), i))
