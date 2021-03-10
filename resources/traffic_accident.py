from flask import jsonify, make_response
from flask_restful import Resource, reqparse
import pymysql
import contextlib

parser = reqparse.RequestParser()
parser.add_argument("event_time")
parser.add_argument("event_location")
parser.add_argument("deaths")
parser.add_argument("injuries")
parser.add_argument("vehicle_type")
parser.add_argument("longitude")
parser.add_argument("latitude")
parser.add_argument('StartFrom',type = int, default = "0",location = 'args')
parser.add_argument('Limit',type = int, default = "1000",location = 'args')


@contextlib.contextmanager
def mysql(host='192.168.56.102', user='harold', passwd='123456', db='assignment'):
    conn = pymysql.connect(host=host, user=user, passwd=passwd, db=db)
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        yield cursor
    finally:
        conn.commit()
        cursor.close()
        conn.close()

def update_query(accident):
    query = []
    for key,value in accident.items():
        if value != None:
            query.append(key + '=' + "'{}'".format(value))
    query = ",".join(query)
    return query    

class TrafficAccidents(Resource):
    def get(self):
        arg = parser.parse_args()
        if (arg['StartFrom'] == 0):
            with mysql() as cursor:
                sql = """select * from traffic_accident where deleted = False and id < 100;"""
                cursor.execute(sql)
                accidents = cursor.fetchall()
            
            return make_response(jsonify(accidents))
        else:
            with mysql() as cursor:
                sql = """select * from traffic_accident where deleted = False and id >= {} limit {};"""
                print(arg['StartFrom'], arg['Limit'])
                sql = sql.format(arg['StartFrom'], arg['Limit'])
                print(sql)
                cursor.execute(sql)
                accidents = cursor.fetchall()
            
            return make_response(jsonify(accidents))
    
    def post(self):
        arg = parser.parse_args()
        accident = {
            "event_time": arg["event_time"],
            "event_location": arg["event_location"],
            "deaths": arg["deaths"],
            "injuries": arg["injuries"],
            "vehicle_type": arg["vehicle_type"],
            "longitude": arg["longitude"],
            "latitude": arg["latitude"]
        }

        with mysql() as cursor:
            sql = """insert into traffic_accident
            (event_time, event_location, deaths, injuries, vehicle_type, longitude, latitude)
            values('{}','{}',{},{},'{}','{}','{}');""".format(accident["event_time"],
                                                            accident["event_location"],
                                                            accident["deaths"],
                                                            accident["injuries"],
                                                            accident["vehicle_type"],
                                                            accident["longitude"],
                                                            accident["latitude"])
            print(sql)
            cursor.execute(sql)
            
        return make_response(jsonify({'result':True}))

class TrafficAccidentsCount(Resource):
    def get(self):
        with mysql() as cursor:
            sql = """SELECT COUNT(*), MIN(id), MAX(id) FROM traffic_accident where deleted = False;"""
            cursor.execute(sql)
            count = cursor.fetchall()
        
        return make_response(jsonify(count))

class TrafficAccident(Resource):
    def get(self, id):
        with mysql() as cursor:
            sql = """select * from traffic_accident where deleted = False and id = {};""".format(id)
            cursor.execute(sql)
            accidents = cursor.fetchall()
        
        return make_response(jsonify(accidents))

    def patch(self, id):
        with mysql() as cursor:
            arg = parser.parse_args()
            accident = {
                "event_time": arg["event_time"],
                "event_location": arg["event_location"],
                "deaths": arg["deaths"],
                "injuries": arg["injuries"],
                "vehicle_type": arg["vehicle_type"],
                "longitude": arg["longitude"],
                "latitude": arg["latitude"]
            }

            query = update_query(accident)
            sql = """UPDATE traffic_accident SET {} where id = '{}' and deleted = False""".format(query, id)
            cursor.execute(sql)

        return jsonify({'result': True})

    def delete(self, id):
        with mysql() as cursor:
            sql = """UPDATE traffic_accident set deleted = True where id = '{}' and deleted = False""".format(id)
            cursor.execute(sql)

        return jsonify({'result':True})
