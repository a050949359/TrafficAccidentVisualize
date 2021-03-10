import flask
import os
from flask import render_template
from flask_restful import Api, Resource
from resources.traffic_accident import TrafficAccidents, TrafficAccidentsCount, TrafficAccident
from resources.traffic_analytics import TrafficAnalytics
from resources.traffic_form import TrafficForm
from flask_wtf.csrf import CSRFProtect, CSRFError
from flask_bootstrap import Bootstrap

app = flask.Flask(__name__)
app.config["DEBUG"] = True
# app.config['SECRET_KEY'] = os.urandom(24)
app.config['SECRET_KEY'] = "SECRET_KEY"
csrf = CSRFProtect(app)
bootstrap = Bootstrap(app)

api = Api(app, decorators=[csrf.exempt])
api.add_resource(TrafficAccidents, '/traffic_accidents/')
api.add_resource(TrafficAnalytics, '/traffic_analytics/')
api.add_resource(TrafficAccidentsCount, '/traffic_accidents/status')
api.add_resource(TrafficAccident, '/traffic_accident/<id>')
# api.add_resource(TrafficAccident, '/traffic_accident/<id>')

# @app.errorhandler(CSRFError)
# def handle_csrf_error(e):
#     return render_template('csrf_error.html', reason=e.description), 400

# @app.errorhandler(Exception)
# def handle_error(error):
#     status_code = 500
#     if type(error).__name__ == 'NotFound':
#         status_code = 404
#     else:
#         pass
#     return {"msg":type(error).__name__ }, status_code

@app.route('/', methods = ["GET"])
def home():
    return render_template('index.html')

@app.route('/traffic_accident/append', methods=['GET','POST'])
def traffic_form():
    form = TrafficForm()
    return render_template('traffic_form.html', form=form)

@app.route('/traffic_accident/map', methods=['GET'])
def traffic_map():
    return render_template('traffic_map.html')

@app.route('/traffic_analytics/city', methods=['GET'])
def traffic_city():
    return render_template('traffic_analytics_city.html')

@app.route('/traffic_analytics/hours', methods=['GET'])
def traffic_hours():
    return render_template('traffic_analytics_hours.html')

@app.route('/traffic_analytics/month', methods=['GET'])
def traffic_month():
    return render_template('traffic_analytics_month.html')

@app.route('/traffic_analytics/most_location', methods=['GET'])
def traffic_most_location():
    return render_template('traffic_analytics_most_location.html')

@app.route('/traffic_analytics/vehicle', methods=['GET'])
def traffic_vehicle():
    return render_template('traffic_analytics_vehicle.html')
    

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

