import zmq.green as zmq
import random
import gevent
from operator import itemgetter


def poll_sensor(address):
    """ Simulate polling a Carrera Control Unit

    The public api for race timers right now is
    and will be sent as json string
    data = {'lapTime': lap_time,
            'controller': controller,
            'lapTimeFastest': fastest,
            'laps': laps[controller]}
    Subject to be change!
    """
    fastest_laps = {i: 999.0 for i in range(1, 7)}
    laps = {i: 0 for i in range(1, 7)}
    lap_time_estimate = 6.500
    variation = 0.500

    def read():
        """ Simulate some sensor, that can push"""
        lap_time = random.uniform(lap_time_estimate,
                                  lap_time_estimate + 0.100)
        data_list = []
        for controller in range(1, 7):
            laps[controller] += 1
            fastest = fastest_laps[controller]
            data = {'lapTime': lap_time,
                    'controller': controller,
                    'lapTimeFastest': fastest,
                    'laps': laps[controller]}
            offset = random.uniform(-variation, variation)
            if lap_time < fastest:
                data["lapTimeFastest"] = lap_time
                fastest_laps[controller] = lap_time
            data_list.append(data)
            lap_time += offset

        gevent.sleep(lap_time)
        for i in sorted(data_list, key=itemgetter('lapTime')):
            gevent.sleep(i['lapTime'] - lap_time)
            yield i

    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind(address)
    while True:
        for race_data in read():
            socket.send_json({"event": "racetime",
                              "args": race_data})


if __name__ == "__main__":
    gevent.joinall([
        gevent.spawn(poll_sensor, "tcp://127.0.0.1:5000")])
