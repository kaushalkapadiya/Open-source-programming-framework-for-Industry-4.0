# -*- coding: utf-8 -*-
"""Tutorial on using the InfluxDB client."""

import argparse
import time
from influxdb import InfluxDBClient

f=open('t.txt','r')
f=f.read()
print(f)
def main(host='localhost', port=8086):
    """Instantiate a connection to the InfluxDB."""

    user = 'root'
    password = 'root'
    dbname = 'mydb'

    query = 'select Float_value from cpu_load_short;'
    client = InfluxDBClient(host, port, user, password, dbname)
    print("Drop database: " + dbname)
    client.drop_database(dbname)
    print("Create database: " + dbname)
    client.create_database(dbname)

    print("Create a retention policy")
    client.create_retention_policy('awesome_policy', '3d', 3, default=True)
            #time.sleep(1)
    json_body=[
    {
      "device": {
        "deviceID": "device-001"
      },
      "measurements": [
        {
          "ts": "2018-11-17T18:13:08.205586+05:30",
          "result": "OK",
          "series": {
            "$_time": [
              0
            ],
            "rms.x": [
              11.029159575398387
            ],
            "rms.y": [
              0.9948208508373756
            ],
            "rms.z": [
              1.4954372950192194
            ],
            "skewness.x": [
              -0.15336864014516252
            ],
            "skewness.y": [
              -0.0017978633445505498
            ],
            "skewness.z": [
              -0.030553187194228126
            ],
            "deviation.x": [
              0.4604183505282917
            ],
            "deviation.y": [
              0.2745409035611802
            ],
            "deviation.z": [
              0.7501121596607814
            ]
          }
        }
      ],
      "content-spec": "urn:spec://eclipse.org/unide/measurement-message#v2"
    }]
    print("Write points: {0}".format(json_body))
    client.write_points(json_body)

    '''client = InfluxDBClient(host, port, user, password, dbname)

    print("Create database: " + dbname)
    client.create_database(dbname)

    print("Create a retention policy")
    client.create_retention_policy('awesome_policy', '3d', 3, default=True)

    print("Switch user: " + dbuser)
    client.switch_user(dbuser, dbuser_password)

    print("Write points: {0}".format(json_body))
    client.write_points(json_body)'''
    '''print("Drop database: " + dbname)
    client.drop_database(dbname)
    '''

def parse_args():
    """Parse the args."""
    parser = argparse.ArgumentParser(
        description='example code to play with InfluxDB')
    parser.add_argument('--host', type=str, required=False,
                        default='localhost',
                        help='hostname of InfluxDB http API')
    parser.add_argument('--port', type=int, required=False, default=8086,
                        help='port of InfluxDB http API')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(host=args.host, port=args.port)
