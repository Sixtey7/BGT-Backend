from flask import Blueprint, abort, jsonify, request
import model.PlayerDB as PlayerDB

player_api = Blueprint('player_api', __name__)


@player_api.route('', methods=['GET'])
def get_all():
    """Returns all of the Players that exist in the database

    :return the result as a json array
    """
    return jsonify([player.to_obj() for player in PlayerDB.get_all()]), 200


@player_api.route('<string:player_id>', methods=['GET'])
def get(player_id):
    """Returns the Player specified by the provided player_id

    :param player_id: The id of the Player to return
    :return 200 and the specified Player object, or 404 if no Player was found with the specified id
    """
    player_obj = PlayerDB.get(player_id)
    if player_obj is None:
        abort(404, 'No Player found for given id!')

    return jsonify(player_obj.to_obj()), 200


@player_api.route('', methods=['POST'])
def create():
    """Used to create a new Player.

    Expects the details of the Player in JSON format as part of the request body
    If no id is provided, an Id will be generated as part of the Player creation

    :return 200 and the newly created Player or 400 if no request body was found
    """
    if not request.json:
        abort(400, 'No request body provided!')

    player = PlayerDB.create(request.json['name'])
    return jsonify(player.to_obj()), 200


@player_api.route('<string:player_id>', methods=['PUT'])
def update(player_id):
    """Updates the specified Player with the contents of the request body (in JSON)

    Expects "name" to be provided in the request body

    :param player_id: the id of the Player to be updated
    :return 200 and the updated Player, 400 if no request body has been provided
        404 if the specified Player cannot be found
    """
    if not request.json:
        abort(400, 'No request body provided')

    try:
        player = PlayerDB.update(player_id, request.json['name'] if 'name' in request.json else None)
        return jsonify(player.to_obj()), 200
    except ValueError:
        abort(404, 'Could not find Player with the provided id')


@player_api.route('<string:player_id>', methods=['DELETE'])
def delete(player_id):
    """Deletes the specified Player from the database

    :param player_id: The id of the Player to be deleted
    :return: 200 if the Player was successfully deleted, 404 if the Player cannot be found
    """
    try:
        status = PlayerDB.delete(player_id)
        if status:
            return '', 200
        else:
            return '', 500
    except ValueError:
        abort(404, 'Could not find Player with the provided id')
