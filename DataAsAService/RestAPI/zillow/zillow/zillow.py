# @author Hongwei
import boto3, json
from geopy.distance import vincenty
from pandas import DataFrame
import pandas as pd
from flask import Flask, request, render_template, g
app = Flask(__name__)  # create the application instance :)


@app.route('/')
def index():
    result = {};
    # default to point to LA
    return render_template('cloud.html', latitude=34, longitude=-118, result=result)


@app.route('/map', methods=['GET', 'POST'])
def cloud():
    data = get_result()
    latitude = request.form['latitude']
    longitude = request.form['longitude']
    if latitude and longitude:
        closest = find_closest(latitude, longitude)
        return render_template('cloud.html', latitude=latitude, longitude=longitude, result=closest)
    else:
        # Point to LA
        return render_template('cloud.html', latitude=34, longitude=-118)


@app.route('/2')
def index2():
    result = {};
    # default to point to LA
    return render_template('local.html', latitude=34, longitude=-118, result=result)


@app.route('/local', methods=['GET', 'POST'])
def local():
    latitude = request.form['latitude']
    longitude = request.form['longitude']
    if latitude and longitude:
        closest = find_closest(latitude, longitude, local=True)
        return render_template('local.html', latitude=latitude, longitude=longitude, result=closest)
    else:
        # default point to LA
        return render_template('local.html', latitude=34, longitude=-118)


def connect_sdb():
    with app.open_resource('static/config.json') as globalSettings:
        config = json.load(globalSettings)

    # Loading Global settings
    ACCESS_KEY = str(config['AWSAccess'])
    SECRET_KEY = str(config['AWSSecret'])
    region = str(config['region'])
    g._domain = str(config['name'])

    Session = boto3.Session(
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        region_name=region
    )
    sdb = Session.client('sdb')
    return sdb


def get_db():
    db = getattr(g, '_db', None)
    if db is None:
        db = g._database = connect_sdb()
    return db


@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_db', None)
    if db is not None:
        db.close()


def get_result():
    result = getattr(g, '_result', None)
    if result is None:
        result = g._result = get_db().select(
            SelectExpression="select * from ZillowData limit 1000"
        )
    return result


def get_items():
    items = getattr(g, '_items', None)
    if items is None:
        data = pd.read_csv('zillow/static/ZillowData.csv', usecols=['parcelid', 'latitude', 'longitude'], sep=',')
        items = g._items = data.dropna()
    return items


def find_closest(latitude, longitude, local=False):
    curLoc = (latitude, longitude)
    id = []
    distance = []
    latitudes = []
    longitudes = []

    if local:
        items = get_items()
        for item in items.itertuples():
            lat = item[2] / 1000000
            long = item[3] / 1000000
            dis = vincenty(curLoc, (lat, long)).miles
            id.append(item[1])
            distance.append(dis)
            latitudes.append(lat)
            longitudes.append(long)

    else:
        items = get_result()['Items']
        for attr in items:
            lat = float(attr['Attributes'][0]['Value']) / 1000000
            long = float(attr['Attributes'][1]['Value']) / 1000000
            dis = vincenty(curLoc, (lat, long)).miles
            id.append(attr['Name'])
            distance.append(dis)
            latitudes.append(lat)
            longitudes.append(long)

    data = DataFrame({'id': id, 'latitude': latitudes, 'longitude': longitudes, 'distance': distance})
    closest = data.sort_values(by=['distance'], ascending=True)[0:10]
    print(latitude + '-' + longitude)
    print(closest)

    return closest.to_json(orient='records')

