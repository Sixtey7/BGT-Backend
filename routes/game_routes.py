from flask import Blueprint, abort, jsonify, request
import model.GameDB as GameDB

game_api = Blueprint('game_api', __name__)


@game_api.route('', methods=['GET'])
def get_all():
    """Returns all of the Games that exist in the database

    :return the result as a json array
    """
    return jsonify([game.to_obj() for game in GameDB.get_all()]), 200


@game_api.route('<string:game_id>', methods=['GET'])
def get(game_id):
    """Returns the Game specified by the provided game_id

    :param game_id: The id of the Game to return
    :return 200 and the specified Game object, or 404 if no Game was found with the specified id
    """
    game_obj = GameDB.get(game_id)
    if game_obj is None:
        abort(404, 'No Game found for given id!')

    return jsonify(game_obj.to_obj()), 200


@game_api.route('', methods=['POST'])
def create():
    """Used to create a new Game.

    Expects the details of the Game in JSON format as part of the request body
    If no id is provided, an Id will be generated as part of the Game creation

    :return 200 and the newly created Game or 400 if no request body was found
    """
    if not request.json:
        abort(400, 'No request body provided!')

    game = GameDB.create(request.json['name'],
                         request.json['scoring'],
                         request.json['id'] if 'id' in request.json else None)

    return jsonify(game.to_obj()), 200


@game_api.route('<string:game_id>', methods=['PUT'])
def update(game_id):
    """Updates the specified Game with the contents of the request body (in JSON)

    Expects either (or both) of "name" and "scoring" to be provided in the request body

    :param game_id: the id of the Game to be updated
    :return 200 and the updated Game, 400 if no request body has been provided
        404 if the specified Game cannot be found
    """
    if not request.json:
        abort(400, 'No request body provided')

    try:
        game = GameDB.update(game_id,
                             request.json['name'] if 'name' in request.json else None,
                             request.json['scoring'] if 'scoring' in request.json else None)
        return jsonify(game.to_obj()), 200
    except ValueError:
        abort(404, 'Could not find Game with the provided id')


@game_api.route('<string:game_id>', methods=['DELETE'])
def delete(game_id):
    """Deletes the specified Game from the database

    :param game_id: The id of the Game to be deleted
    :return: 200 if the Game was successfully deleted, 404 if the Game cannot be found
    """
    try:
        status = GameDB.delete(game_id)
        if status:
            return '', 200
        else:
            return '', 500
    except ValueError:
        abort(404, 'Could not find Game with the provided id')
