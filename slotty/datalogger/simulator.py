import random
import time
from operator import itemgetter


def read():
    #TODO: add the datalogger data here

    lap_time_estimate = 6.500
    variation = 0.500
    lap_time = random.uniform(lap_time_estimate,
                              lap_time_estimate + 0.100)
    data = []
    for controller in range(6):
        data.append({'lap_time': lap_time,
                     'controller': controller})
        offset = random.uniform(-variation, variation)
        lap_time += offset

    time.sleep(lap_time)
    for i in sorted(data, key=itemgetter('lap_time')):
        time.sleep(i['lap_time'] - lap_time)
        yield i
