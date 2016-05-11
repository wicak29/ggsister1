#manager file - file On Manager
#!/usr/bin/env python
import uuid
import os
import glob
import json
import timeit
from celery import Celery
app = Celery('tasks', broker='amqp://ggsister:ggsister@10.151.43.230//', backend='amqp://ggsister:ggsister@10.151.43.230//')

eventLogs = []
events = {}

start = timeit.default_timer()

os.chdir("log")

for file in glob.glob("*.*"):
    n = open(file,'r').read()
    # print(" [x] fib(30)")
    event = app.send_task('tasks.messageParse', args=[str(n)])
    eventLogs.append(event.get())

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
