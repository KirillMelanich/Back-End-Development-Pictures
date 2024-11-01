from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################

@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################

@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500

######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    """Returns all pictures as a JSON array."""
    return jsonify(data), 200

######################################################################
# GET A PICTURE BY ID
######################################################################
@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """Returns a single picture by its ID."""
    # Find picture by ID
    picture = next((item for item in data if item["id"] == id), None)
    if picture:
        return jsonify(picture), 200
    else:
        return {"error": "Picture not found"}, 404

######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    """Create a new picture entry"""
    picture = request.get_json()  # Get JSON data from the request body

    # Check if a picture with the same ID already exists
    for pic in data:
        if pic["id"] == picture["id"]:
            return jsonify({"Message": f"picture with id {picture['id']} already present"}), 302

    # Append the new picture data to the list
    data.append(picture)
    return jsonify(picture), 201  # Return the created picture and HTTP 201 Created status

######################################################################
# UPDATE A PICTURE
######################################################################
@app.route('/picture/<int:id>', methods=['PUT'])
def update_picture(id):
    # Get the new picture data from the request
    updated_data = request.get_json()
    
    # Find the picture with the given ID
    for picture in data:
        if picture['id'] == id:
            # Update picture details
            picture.update(updated_data)
            return jsonify(picture), 200  # Return updated picture data

    # If picture not found, return a 404 response
    return jsonify({"message": "picture not found"}), 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route('/picture/<int:id>', methods=['DELETE'])
def delete_picture(id):
    global data
    # Find the picture by ID
    picture_to_delete = next((pic for pic in data if pic['id'] == id), None)
    
    if picture_to_delete:
        data.remove(picture_to_delete)  # Remove the picture from the list
        return '', 204  # No Content response
    else:
        return jsonify({"message": "picture not found"}), 404  # Not Found response

