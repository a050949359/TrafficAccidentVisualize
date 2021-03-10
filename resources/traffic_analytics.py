from flask import jsonify, make_response
from flask_restful import Resource, reqparse
import pymysql
import contextlib

parser = reqparse.RequestParser()
parser.add_argument("count")
parser.add_argument("event_location")
parser.add_argument("event_city")
parser.add_argument("deaths")
parser.add_argument("injuries")
parser.add_argument("vehicle_type")
parser.add_argument("month")
parser.add_argument("hours")
parser.add_argument("type")


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

class TrafficAnalytics(Resource):
    def get(self):
        arg = parser.parse_args()
        if (arg['type'] == "vehicle"):
            with mysql() as cursor:
                sql = """ select SUBSTRING_INDEX(vehicle_type, "-", -1) vehicle, count(*) count from event_vehicle_tmp group by SUBSTRING_INDEX(vehicle_type, "-", -1); """
                cursor.execute(sql)
                accidents = cursor.fetchall()
            
            return make_response(jsonify(accidents))
        elif (arg['type'] == "city"):
            with mysql() as cursor:
                sql = """ select event_city, count(*) count, sum(deaths) deaths, sum(injuries) injuries from assignment.traffic_accident group by event_city; """
                cursor.execute(sql)
                accidents = cursor.fetchall() 
                
                return make_response(jsonify(accidents))
             
            
        elif (arg['type'] == "month"):
            with mysql() as cursor:
                sql = """ SELECT MONTH(event_time) month, count(*) count, sum(deaths) deaths, sum(injuries) injuries FROM assignment.traffic_accident GROUP BY MONTH(event_time); """
                cursor.execute(sql)
                accidents = cursor.fetchall()
            
            return make_response(jsonify(accidents))
        elif (arg['type'] == "hours"):
            with mysql() as cursor:
                sql = """ SELECT HOUR(event_time) hours, count(*) count FROM assignment.traffic_accident GROUP BY HOUR(event_time) """
                cursor.execute(sql)
                accidents = cursor.fetchall()
            
            return make_response(jsonify(accidents))
        elif (arg['type'] == "most_location"):
            with mysql() as cursor:
                sql = """ select count(*) count, event_location from assignment.traffic_accident where event_city = '臺北市' group by event_location order by count desc limit 10; """
                cursor.execute(sql)
                accidents = cursor.fetchall()
            
            return make_response(jsonify(accidents))
    
 