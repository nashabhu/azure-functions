import azure.functions as func
import logging
from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.json_util import loads, dumps
from bson.objectid import ObjectId 

from dotenv import load_dotenv, find_dotenv
import os
import pprint


app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)
logger= logging.getLogger(__name__)

#connect MongoDB
MONGO_URI = os.environ.get("MONGO_URI")

# Initialize MongoDB client
client = MongoClient(MONGO_URI)

# Select database
db = client.get_database("Survey_data")

# Select collection
collection = db.get_collection("user_demographics")




@app.route("/")
def index():
    logger.info("Received request to index endpoint.")
    return (
        "HI\n"
        "This is API for Survey Data\n"
          )

# route to get all documents
@app.route('/read', methods=['GET'])
def get_all_documents():
    documents = list(collection.find())
   # return jsonify(documents), 200
    return dumps(documents) , 200


# Route to create a new document
@app.route('/add', methods=['POST'])
def create_document():
    data = request.json
    if data:
        # Insert document into collection
        
        if isinstance(data, list) and len(data) > 1:
            result = collection.insert_many(data)
        else :
            result = collection.insert_one(data)
          # Get request data
        # req_data = request.get_json()
        # result = collection.insert_many(data)
    
   
        if result:
            return jsonify({"message": "Document created successfully"}), 201
        else:
            return jsonify({"message": "Failed to create document"}), 500
    else:
        return jsonify({"message": "No data provided"}), 400



# Route to delete a document
@app.route('/delete/<id>', methods=['DELETE'])
def delete_document(id):
    result = collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count > 0:
        return jsonify({"message": "Document deleted successfully"}), 200
    else:
        return jsonify({"message": "Failed to delete document"}), 500

# Route to update a document
@app.route('/update/<id>', methods=['PATCH'])
def update_document(id):
    data = request.json
    if data:
        result = collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        if result.modified_count > 0:
            return jsonify({"message": "Document updated successfully"}), 200
        else:
            return jsonify({"message": "Failed to update document"}), 500
    else:
        return jsonify({"message": "No data provided"}), 400








# Create an Azure Function which serves the above routes in our WSGI runtime (Gunicorn)
app = func.WsgiFunctionApp(app=app.wsgi_app, http_auth_level=func.AuthLevel.ANONYMOUS)






