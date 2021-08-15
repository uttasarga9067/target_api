import markdown
import os
import json
import requests


from flask import Flask, g,jsonify
from flask_restful import Resource, Api, reqparse, request
from product_registry.test_db import create_db
# Create an instance of Flask
app = Flask(__name__)
# engine = create_engine("postgresql+psycopg2://postgres:uttasarga@localhost:5433/target_api")
connection = create_db
# Create the API

api = Api(app)

@app.route('/processjson', methods=['GET'])

# """THIS GET METHOD IS JUST A DEMO FOR MAKING SURE THAT I CAN PROCESS THE JSON AS PER MY REQUIREMENT"""

# """UTTASARGA SINGH 08/08/2021"""
def processjson():
    uri = "https://redsky.target.com/v3/pdp/tcin/13860428?excludes=taxonomy,price,promotion,bulk_ship,rating_and_review_reviews,rating_and_review_statistics,question_answer_statistics&key=candidate#_blank"
    try:
        uResponse = requests.get(uri)
    except requests.ConnectionError:
        return "Connection Error"
    Jresponse = uResponse.text
    data = json.loads(Jresponse)
    product_id = data['product']['available_to_promise_network']['product_id']
    name = data['product']['item']['product_description']['title']
    # reputation = data['items'][0]['reputation']
    # return Jresponse
    return json.dumps({'ID': product_id, 'NAME': name})


    # name = json.dumps(data[0])
    # return json.dumps({'result': 'Success', 'displayName': displayName})

@app.route("/")
def index():
    # """PRESENT THE CODE DOCUMENTATION"""

    # """UTTASARGA SINGH 08/08/2021"""

    # Open the README file
    with open(os.path.dirname(app.root_path) + '/README.md', 'r') as markdown_file:

        # Read the content of the file
        content = markdown_file.read()

        # Convert to HTML
        return markdown.markdown(content)



class Prices(Resource):
    def get(self):
        price = connection.execute("SELECT * FROM prices ")
        return {price}, 200

class Device(Resource):

    # """THIS METHOD GETS A PRODUCT ID AS A INPUT FROM THE USER AND HELPS TO RETRIEVE THE DATA POINTS WITH REGARDS TO THE DATA"""

    # """UTTASARGA SINGH 08/08/2021"""
    def get(self, identifier):
        uri = "https://redsky.target.com/v3/pdp/tcin/13860428?excludes=taxonomy,price,promotion,bulk_ship,rating_and_review_reviews,rating_and_review_statistics,question_answer_statistics&key=candidate#_blank"
        try:
            uResponse = requests.get(uri)
        except requests.ConnectionError:
            return "Connection Error"
        Jresponse = uResponse.text
        data = json.loads(Jresponse)
        # If the key does not exist in the data store, return a 404 error.
        if identifier not in data['product']['available_to_promise_network']['product_id']:
            return {'message': 'Product not found', 'data': {}}, 404
        else:
            return {'message': 'PRODUCT FOUND',
                    'PRODUCT_ID': data['product']['available_to_promise_network']['product_id'],
                    'PRODUCT_NAME': data['product']['item']['product_description']['title']}, 200


# api.add_resource(DeviceList, '/devices')
api.add_resource(Device, '/device/<string:identifier>')
api.add_resource(Prices, '/prices')
# if __name__ == '__main__':
#     db.create_all()
#     app.run()