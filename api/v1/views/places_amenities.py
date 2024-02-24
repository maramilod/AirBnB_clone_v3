#!/usr/bin/python3
"""hey"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.place import Place
from models.amenity import Amenity
from models.user import User

db = type(storage).__name__ == "DBStorage"


@app_views.route('/places/<string:place_id>/amenities',
                 methods=['GET'], strict_slashes=False)
def get_places_amenities(place_id):
    """get amenities info for a specified place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenities = []
    for amenity in place.amenities:
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_places_amenity(place_id, amenity_id):
    """deletes a amenity based on its amenity_id"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)
    if amenity not in place.amenities:
        abort(404)
    if db:
        place.amenities.remove(amenity)
    else:
        place.amenity_ids.remove(amenity_id)
    amenity.save()
    """200 by default we dont need to write it"""
    return (jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def post_places_amenity(place_id, amenity_id):
    """create"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)
    if amenity in place.amenities:
        return make_response(jsonify(amenity.to_dict()), 200)
    if db:
        place.amenities.append(amenity)
    else:
        place.amenity_ids.append(amenity_id)
    place.save()
    return make_response(jsonify(amenity.to_dict()), 201)
