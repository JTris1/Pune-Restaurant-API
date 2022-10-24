import json
import mimetypes
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

def queryRestaurants():
    if 'name' in request.args:
        cursor = restaurants.find_one({'Restaurant_Name': request.args['name']})
        list_cur = list(cursor)
        json_data = dumps(list_cur)
        resp = Response(json_data, status=200, mimetype="application/json")
        return resp
    # else:
    #     cursor = restaurants.find()
    #     list_cur = list(cursor)
    #     json_data = dumps(list_cur)
    #     resp = Response(json_data, status=200, mimetype="application/json")
    #     return resp