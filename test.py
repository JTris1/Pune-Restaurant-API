import json
import mimetypes
import re
from urllib import response
from colorama import Fore, Style
from pprint import pprint
from flask import Flask, render_template, request, Response, url_for, redirect, jsonify
from dotenv import dotenv_values
from pymongo import MongoClient
from bson.json_util import dumps

config = dotenv_values(".env")

app = Flask(__name__)

client = MongoClient(config["ATLAS_URI"]);
db = client.restaurant_api
print(Fore.GREEN + "Connected to 'restaurant_api' database")

restaurants = db.pune_restaurants
neighborhoods = db.pune_neighborhoods

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/restaurants')

# def queryRestaurants():
#     if 'name' in request.args:
#         cursor = restaurants.find_one({'Restaurant_Name': request.args['name']})
#         json_data = dumps(cursor)
#         resp = Response(json_data, status=200, mimetype="application/json")
#         return resp
#     elif 'known_for_food' in request.args:
#         cursor = restaurants.find({'Known_For_Food': request.args['known_for_food']})
#         json_data = dumps(cursor)
#         resp = Response(json_data, status=200, mimetype="application/json")
#         return resp
#     elif 'coordinates' in request.args:
#         latitude = request.args.getlist('coordinates')[0]
#         longitude = request.args.getlist('coordinates')[1]
#         print(latitude)
#         return Response(status=200)
#     else:
#         return Response(status=404)

def queryRestaurants():
    req_list = request.args.to_dict(flat=False);
    for key in req_list:
        if(key == 'name'):
            if(len(req_list['name']) > 1):
                print("MULTIPLE NAMES, IMPLEMENT CODE HERE")
            else:
                print(req_list['name'][0])
        # ADD CODE FOR ALL OTHER CONDITIONALS
    return Response(status=200)