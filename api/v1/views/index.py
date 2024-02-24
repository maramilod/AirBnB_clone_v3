#!/usr/bin/python3
"""
one more time
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
    """return ok """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def stats():
    """ count """
    response = {}
    NAMES = {
            "Amenity": "amenities",
            "City": "cities",
            "Place": "places",
            "Review": "reviews",
            "State": "states",
            "User": "users"
            }
    for cls, key in NAMES.items():
        response[key] = storage.count(cls)
    return jsonify(response)
