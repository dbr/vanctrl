import json
import datetime
import fileinput
import influxdb


class InfluxLogger(object):
    def __init__(self):
        self.connection = influxdb.InfluxDBClient(database='solar')

    def handle_data(self, d):
        # {"time" : "2019-07-07 00:20:41", "model" : "Digitech-XC0324", "id" : "90", "temperature_C" : 20.000, "flags" : 128, "mic" : "CHECKSUM", "message_num" : 1}

        points = []
        points.append({
            #'time': timestamp,
            'measurement': 'van_temp',
            'fields': {
                'temperature_C': d['temperature_C'],
            },
            'tags': {
                'sensor_id': d['id'],
                'model': d['model'],
            },
        })
        print(datetime.datetime.now(), points)
        self.connection.write_points(points)


x = InfluxLogger()
for line in fileinput.input():
    data = json.loads(line)
    x.handle_data(data)
