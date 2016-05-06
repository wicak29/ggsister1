from celery import Celery
from customParser import parseText
import timeit
import os
import glob
import json

app = Celery('tasks', backend='rpc://', broker='amqp://guest@localhost//')

os.chdir("log/")
eventLogs = []
events = {}

@app.task
def add(x, y):
    return x + y

@app.task(ignore_result=True)
def print_hello():
    print 'hello there'

@app.task
def gen_prime(x):
    multiples = []
    results = []
    for i in xrange(2, x+1):
        if i not in multiples:
            results.append(i)
            for j in xrange(i*i, x+1, i):
                multiples.append(j)
    return results

@app.task
def messageParse(file):
    hasil = file
    response = parseText(hasil)
    print hasil
    return response