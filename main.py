""" This allows people to create/view posts"""
from pprint import pprint
from flask import Flask, jsonify
from flask_restful import Resource, Api
from pymongo import MongoClient
import configparser
import dateutil
import json

app = Flask(__name__)
api = Api(app)

#GLOBALS
DB_URL = ''
DB_PORT = ''
DB_CLIENT = MongoClient()

class Post:
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



class Feed(Resource):
    """Get posts from a user"""

    def get(self, user):
        db = DB_CLIENT.test
        posts  = db.testcollection.find({"User": user})

        p = []
        for i in posts:
            p.append({'user': i['User'], 'date': i['date'], 'body': i['body']})

        #status = str(serverStatusResult)
        status = 'alls good'
        response = jsonify({ 
            'USER': user,
            'result_count': p,
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

api.add_resource(Feed, '/<user>')

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.sections()
    config.sections()
    config.read('config.ini')
    DB_URL = config['Database']['url']
    DB_PORT = config['Database']['port']
    DB_CLIENT = MongoClient(DB_URL, int(DB_PORT)) 

#post = {'User': 'bob', 'date': 'today', 'body': 'this is a post'}
        #post_id = db.testcollection.insert_one(post).inserted_id
        #print(post_id, 'this is the tihgn')


    app.run(debug=True)
