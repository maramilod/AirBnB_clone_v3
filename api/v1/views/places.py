#!/usr/bin/python3
"""hey"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<string:city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """get cities info in a specified state"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = []
    for place in city.places:
        places.append(place.to_dict())
    return jsonify(places)


@app_views.route('/places/<string:place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """get place information for specified place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<string:place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """deletes a place based on its place_id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    """200 by default we dont need to write it"""
    return (jsonify({}), 200)


@app_views.route('/cities/<string:city_id>/places/', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """create"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.is_json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'user_id' not in request.get_json():
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    dic = request.get_json()
    if not storage.get(User, dic.get("user_id")):
        abort(404)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    dic['city_id'] = city_id
    place = Place(**dic)
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<string:place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """update"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.is_json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'user_id', 'created_at', 'updated_at']:
            setattr(place, attr, val)
    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'],
                 strict_slashes=False)
def places_search():
    """create"""
    if not request.is_json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    dic = request.get_json()
    all_places = storage.all(Place).values()
    places = []
    states = dic.get("states")
    cities = dic.get("cities")
    amenities = dic.get("amenities")
    if amenities and len(amenities) != 0:
        for place in all_places:
            ids = [o.id for o in place.amenities]
            if all(id in ids for id in amenities):
                del place.amenities
                places.append(place)
    else:
        places = all_places
    all_places, places = places, []
    if cities and len(cities) != 0:
        for place in all_places:
            if place.city_id in cities:
                places.append(place)
    else:
        places = all_places
    all_places, places = places, []

    if states and len(states) != 0:
        for place in all_places:
            city = storage.get(City, place.city_id)
            if city.state_id in states:
                places.append(place)
    else:
        places = all_places
    all_places, places = places, []

    for place in all_places:
        places.append(place.to_dict())

    return make_response(jsonify(places), 200)
