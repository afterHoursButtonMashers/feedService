""" This allows people to create/view posts"""
from pprint import pprint
from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
from pymongo import MongoClient
from bson  import json_util
import configparser
import dateutil
import json

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('body', type=str)
parser.add_argument('date', type=str)
parser.add_argument('user', type=str)

#GLOBALS
DB_URL = ''
DB_PORT = ''
DB_CLIENT = MongoClient()

class Comment:
    """Post objects we want to show off"""
    user = ''
    date = ''
    body = ''
    def __init__(self, user, date, body):
        self.user = user
        self.date = date
        self.body = body

    def toJson(self):
        return json.dumps(self)


class Post(Resource):
    """Get posts from a user"""

    def get(self, user):
        db = DB_CLIENT.feed
        posts  = db.post.find({"user": user})

        p = []
        for i in posts:
            p.append({'user': i['user'], 'date': i['date'], 'body': i['body']})

        response = jsonify({ 
            'user': user,
            'result': p,
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    def post(self):
        db = DB_CLIENT.feed
        args = parser.parse_args()
        date = args["date"]
        body = args["body"]
        user = args["user"]
        new_post = {
            "date": date,
            "body": body,
            "user": user
            }
        db.post.insert_one(new_post)
        return new_post

api.add_resource(Post, '/post/<user>', '/post')

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.sections()
    config.read('config.ini')
    DB_URL = config['Database']['url']
    DB_PORT = config['Database']['port']
    DB_CLIENT = MongoClient(DB_URL, int(DB_PORT)) 

    APP_HOST = config['Server']['host']
    APP_PORT = config['Server']['port']
    APP_DEBUG = config['Server']['debug']
    app.run(debug=APP_DEBUG,host=APP_HOST,port=int(APP_PORT))
