#!/usr/bin/python3
"""places_amenities.py"""
from api.v1.views import app_views
from flask import abort, jsonify
from models import storage, storage_t
from models.amenity import Amenity
from models.place import Place


@app_views.route('/places/<string:place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_place_amenities(place_id):
    """get amenity information for a specified place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    amenities = []
    for amenity in place.amenities:
        amenities.append(amenity.to_dict())

    return jsonify(amenities)


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """deletes obj"""
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if place is None or amenity is None:
        abort(404)
    if amenity not in place.amenities:
        abort(404)
    if storage_t == "db":
        place.amenities.remove(amenity)
    else:
        place.amenity_ids.remove(amenity_id)

    place.save()
    return jsonify({})


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['POST'], strict_slashes=False)
def post_place_amenity(place_id, amenity_id):
    """adds an amenity object to a place"""
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if place is None or amenity is None:
        abort(404)
    if amenity in place.amenities:
        return jsonify(amenity.to_dict())
    if storage_t == "db":
        place.amenities.append(amenity)
    else:
        place.amenity_ids.append(amenity_id)
    place.save()
    return make_response(jsonify(amenity.to_dict()), 201)
