# -*- coding: utf-8 -*-
"""Tutorial on using the server functions."""

from __future__ import print_function
import argparse

import datetime
import random
import time
import calendar

from influxdb import InfluxDBClient
from influxdb.client import InfluxDBClientError

USER = 'root'
PASSWORD = 'root'
DBNAME = 'tutorial'


def main(host='localhost', port=8086, nb_day=3):
    """Instantiate a connection to the backend."""
    nb_day = 3  # number of day to generate time series
    timeinterval_min = 5  # create an event every x minutes
    total_minutes = 1440 * nb_day
    total_records = int(total_minutes / timeinterval_min)
    now = datetime.datetime.today()
    metric = "server_data.cpu_idle"
    series = []

    for i in range(0, total_records):
        past_date = now - datetime.timedelta(minutes=i * timeinterval_min)
        value = random.randint(0, 200)
        hostName = "server-%d" % random.randint(1, 5)
        #past_date = calendar.timegm(now.utctimetuple())
        # pointValues = [int(past_date.strftime('%s')), value, hostName]
        pointValues = {#"%Y-%m-%d %H:%M:%S"
            "time": past_date.strftime ("%Y-%m-%dT%H:%M:%SZ"),
            "measurement": metric,
            "fields": {
                "value": value,
            },
            "tags": {
                "hostName": hostName,
            },
        }
        series.append(pointValues)

    print(series)

    client = InfluxDBClient(host, port, USER, PASSWORD, DBNAME)

    print("Create database: " + DBNAME)
    try:
        client.create_database(DBNAME)
    except InfluxDBClientError:
        # Drop and create
        client.drop_database(DBNAME)
        client.create_database(DBNAME)

    print("Create a retention policy")
    retention_policy = 'server_data'
    client.create_retention_policy(retention_policy, '12d', 12, default=True)

    print("Write points #: {0}".format(total_records))
    client.write_points(series, retention_policy=retention_policy)

    time.sleep(2)

    query = 'select value from server_data.cpu_idle;'
    result = client.query(query)
    print(result)
    print("Result: {0}".format(result))

    print("Drop database: {}".format(DBNAME))
    client.drop_database(DBNAME)


def parse_args():
    """Parse the args."""
    parser = argparse.ArgumentParser(
        description='example code to play with InfluxDB')
    parser.add_argument('--host', type=str, required=False,
                        default='localhost',
                        help='hostname influxdb http API')
    parser.add_argument('--port', type=int, required=False, default=8086,
                        help='port influxdb http API')
    parser.add_argument('--nb_day', type=int, required=False, default=3,
                        help='number of days to generate time series data')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    print(args)
    main(host=args.host, port=args.port, nb_day=args.nb_day)
