from flask import Flask, request
from flask_restful import Resource, Api
from flask_swagger_ui import get_swaggerui_blueprint

from pymongo import MongoClient, TEXT

# FLASK APP
app = Flask(__name__)
# RESTFULL API __init__
api = Api(app)

ALLOWED_HOSTS = ['*']
# SWAGGER CONFIG
SWAGGER_URL = ''
API_URL = '/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Swagger-GET-DATA"
    },
)

# REGISTER SWAGGER
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


# MONGO DB CONNECTION AND CONFIGURATION.
client = MongoClient('mongodb+srv://jenishdhameliya20:sUoK0NLWKhjlpMs2@cluster0.c0t6ocv.mongodb.net/?retryWrites=true'
                     '&w=majority')
db = client['Billing']
collection = db['billing_report']
collection.create_index([("text", TEXT)])


# API CODE.
class ListItems(Resource):

    def get(self):
        ClusterName = request.args.get('ClusterName')
        month = request.args.get('month')
        Year = request.args.get('Year')
        col = request.args.get('col')

        filter_criteria = {
            '$and': [
            {'Cluster Name': ClusterName},
            {'Month': month},
            {'Year': Year},
            ],
        }
        projection = {}
        if col == 'all':
            projection = {}

        else:
            if col:
                columns = [x.strip() for x in col.split(',') if x.strip() != ""]
                for column in columns:
                    projection[column] = 1
            else:
                return {"message": "please enter a column name"}, 404

        results = collection.find(filter_criteria, projection)
        json_results = []
        for result in results:
            _id = result.pop('_id')
            json_results.append(result)
        return json_results


api.add_resource(ListItems, '/get-data')