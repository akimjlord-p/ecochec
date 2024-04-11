from flask import Flask, request
from db_func import set_data_to_device

app = Flask(__name__)


@app.route("/")
def main():
    print('hello')
    return "<h1 style='color:blue'> ecochec api :) </h1>"


@app.route('/device')
def get_data_from_device():
    print('device')
    device_id = request.args.get('deviceid')
    temperature = request.args.get('temperature')
    noise = request.args.get('noise')
    city_id = request.args.get('cityid')
    longitude = request.args.get('longitude')
    latitude = request.args.get('latitude')
    res = set_data_to_device(device_id, temperature, noise, city_id, longitude, latitude)
    if res == 'OK':
        return "<h1 style='color:green'> OK </h1>"
    else:
        return "<h1 style='color:red'> ERROR </h1>"


if __name__ == "__main__":
    app.run(host='147.45.106.124')
