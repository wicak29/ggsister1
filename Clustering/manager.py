from tasks import add
from tasks import gen_prime
from tasks import messageParse
import os
import json
import glob
import timeit
import threading
import time

eventLogs = []
events = {}
threads = []

i = 0
msg = ''
start = timeit.default_timer()

for file in glob.glob("*"):
    n = open(file, 'r').read()
    msg = messageParse(str(n))
    eventLogs.append(msg)

print "MSG : ", msg

for event in eventLogs:
    for key, value in event:
        if key in events:
            events[key] = events[key] + value
        else:
            events[key] = value

stop = timeit.default_timer()
print " Waktu komputasi yang dibutuhkan : ", (stop - start)

flag = 1
topTen = sorted(events.items(), key = lambda t:t[1], reverse=True)
for key, value in topTen:
    print key,' ',value
    flag+=1
    if (flag > 10):
        break;

result = add.delay(4, 4)
prima = gen_prime.delay(100)

print result.get()
print prima.get()