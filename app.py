import json
import mimetypes
import re
from colorama import Fore, Style
from pprint import pprint
from flask import Flask, render_template, request, Response, url_for, redirect, jsonify
from dotenv import dotenv_values
from pymongo import MongoClient
from shapely.geometry import Point, Polygon
from bson.json_util import dumps

config = dotenv_values(".env")

app = Flask(__name__)

client = MongoClient(config["ATLAS_URI"]);
db = client.restaurant_api

print(Fore.GREEN + "Connected to 'restaurant_api' database")

# Assign database prefixes to variable
restaurants = db.pune_restaurants
neighborhoods = db.pune_neighborhoods

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/restaurants')
def get():
    # Assings request args to a dictionary
    req_list = request.args.to_dict(flat=False);
    filter_list = {}

    for key in req_list:
        if(key == 'name'):
            # Make name case insensitive
            re_name = re.compile(req_list['name'][0], re.IGNORECASE)
            # Multiple Names specified
            if(len(req_list['name']) > 1):
                print("MULTIPLE NAMES, IMPLEMENT CODE HERE")
                # TRY TO ITERATE THROUGH LIST OF NAMES
                # Got an error about cannot set expression in for loop
            else:
                filter_list['Restaurant_Name'] = re_name
        elif(key == 'category'):
            re_category = re.compile(req_list['category'][0], re.IGNORECASE)
            filter_list['Category'] = re_category
        elif(key == 'location'):
            # Split 'location' comma-seperated query into a list from a string 
            lat_long = str(req_list['location'][0]).split(',')
            filter_list['Latitude'] = float(lat_long[0])
            filter_list['Longitude'] = float(lat_long[1])
        elif(key == 'locality'):
            neighborhood = req_list['locality'][0]
            filter_list['Locality'] = re.compile(neighborhood, re.IGNORECASE)

    # IF filter_list IS EMPTY, RESPOND WITH 404
    if(filter_list == {}):
        return Response(status=404)

    # Query data with filter list
    cursor = restaurants.find(filter_list)
    json_data = dumps(cursor)
    resp = Response(json_data, status=200, mimetype="application/json")
    return resp

@app.route('/restaurants/near')
def getNear():
    # Assings request args to a dictionary
    req_list = request.args.to_dict(flat=False);

    # Return 400 if no arguments are supplied (400: Bad Request)
    if(len(req_list) == 0):
        return Response(status=400)

    longitude = float(req_list['longitude'][0])
    latitude = float(req_list['latitude'][0])
    maxDistance = int(req_list['max-distance'][0])

    cursor = restaurants.find({
        'Location': {
            '$near': {
                '$geometry': {
                    'type': 'Point',
                    'coordinates': [longitude, latitude]
                },
                '$maxDistance': maxDistance
            }
        }
    })

    json_data = dumps(cursor)
    resp = Response(json_data, status=200, mimetype="application/json")
    return resp

@app.route('/restaurants/within')
def getWithin():
    req_list = request.args.to_dict(flat=False)

    if(len(req_list) == 0):
        return Response(status=400)
    
    req_neighborhood = req_list['neighborhood'][0]

    # Returns all 'coordinates' for supplied neighborhood from queryString (forms the boundary)
    boundary = neighborhoods.find_one(
        {
            'properties': {
                'name': req_neighborhood
            }
        },
        {
            '_id': 0,
            'geometry': {
                'coordinates': 1
            }
        })
    
    neighborhood_boundary = boundary['geometry']['coordinates']
    print(neighborhood_boundary)
    
    # print(cursor['geometry']['coordinates'])

    cursor = restaurants.find({
        'Location': {
            '$geoWithin': {
                '$geometry': {
                    'type': 'Polygon',
                    'coordinates': neighborhood_boundary
                }
            }
        }
    })

    json_data = dumps(cursor)
    resp = Response(json_data, status=200, mimetype="application/json")
    return resp