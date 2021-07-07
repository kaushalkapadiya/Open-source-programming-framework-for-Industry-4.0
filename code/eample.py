# -*- coding: utf-8 -*-
"""Tutorial on using the InfluxDB client."""

import argparse
import time
from influxdb import InfluxDBClient


def main(host='localhost', port=8086):
    """Instantiate a connection to the InfluxDB."""

    user = 'root'
    password = 'root'
    dbname = 'example'
    dbuser = 'smly'
    dbuser_password = 'my_secret_password'
    query = 'select Float_value from cpu_load_short;'
    client = InfluxDBClient(host, port, user, password, dbname)
    print("Drop database: " + dbname)
    client.drop_database(dbname)
    print("Create database: " + dbname)
    client.create_database(dbname)

    print("Create a retention policy")
    client.create_retention_policy('awesome_policy', '3d', 3, default=True)
    b,z=0.0,0.0
    print("Switch user: " + dbuser)
    client.switch_user(dbuser, dbuser_password)
    for i in range(1,23):
        if(i in range(0,5)):
            z+=i
        elif(i in range(5,10)):
            z-=i
        else:
            z+=i
        for j in range(0,59):
            if(j in range(0,20)):
                b+=j
            elif(j in range(20,40)):
                b-=j
            else:
                b+=j
            if(z!=0 and z>1):
                z=b/z
            json_body = [
                {
                    "measurement": "cpu_load_short",
                    "tags": {
                        "host": "server01",
                        "region": "us-west"
                        },
                    "time": "2018-07-28T"+str(i)+":"+str(j)+":00Z",
                    "fields": {
                        "Float_value": z,
                        "Int_value": 3,
                        "String_value": "Text",
                        "Bool_value": True
                            }
                        }
                    ]
            #time.sleep(1)
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
    print("Querying data: " + query)
    result = client.query(query)

    print("Result: {0}".format(result))


    print("Result: {0}".format(result))
    print("Switch user: " + user)
    client.switch_user(user, password)

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
