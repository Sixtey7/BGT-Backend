from flask import Blueprint, abort, jsonify, request
import model.SessionPlayersDB as SessionPlayersDB

session_players_api = Blueprint('session_players_api', __name__)


@session_players_api.route('', methods=['GET'])
def get_all():
    """Returns all of the SessionPlayers that exist in the database

    :return the result as a json array
    """
    return jsonify([session_players.to_obj() for session_players in SessionPlayersDB.get_all()]), 200


@session_players_api.route('/<string:session_players_id>', methods=['GET'])
def get(session_players_id):
    """Returns the SessionPlayers specified by the provided session_players_id

    :param session_players_id: The id of the SessionPlayers to return
    :return 200 and the specified SessionPlayers object, or 404 if no SessionPlayers was found with the specified id
    """
    session_players_obj = SessionPlayersDB.get(session_players_id)
    if session_players_obj is None:
        abort(404, 'No SessionPlayers found for given id!')

    return jsonify(session_players_obj.to_obj()), 200


@session_players_api.route('', methods=['POST'])
def create():
    """Used to create a new SessionPlayers.

    Expects the details of the SessionPlayers in JSON format as part of the request body
    If no id is provided, an Id will be generated as part of the SessionPlayers creation

    :return 200 and the newly created SessionPlayers or 400 if no request body was found
    """
    if not request.json:
        abort(400, 'No request body provided!')

    session_players = SessionPlayersDB.create(request.json['session_id'],
                                              request.json['player_id'],
                                              request.json['score'],
                                              request.json['team'],
                                              request.json['winner'],
                                              request.json['id'] if 'id' in request.json else None)

    return jsonify(session_players.to_obj()), 200


@session_players_api.route('/<string:session_players_id>', methods=['PUT'])
def update(session_players_id):
    """Updates the specified SessionPlayers with the contents of the request body (in JSON)

    Expects either (or any combination) of "session_id", "player_id", "score",
        "team", "winner' to be provided in the request body

    :param session_players_id: the id of the SessionPlayers to be updated
    :return 200 and the updated SessionPlayers, 400 if no request body has been provided
        404 if the specified SessionPlayers cannot be found
    """
    if not request.json:
        abort(400, 'No request body provided')

    try:
        session_players = SessionPlayersDB.update(session_players_id,
                                                  request.json['session_id'] if 'session_id' in request.json else None,
                                                  request.json['player_id'] if 'player_id' in request.json else None,
                                                  request.json['score'] if 'score' in request.json else None,
                                                  request.json['team'] if 'team' in request.json else None,
                                                  request.json['winner'] if 'winner' in request.json else None)
        return jsonify(session_players.to_obj()), 200
    except ValueError:
        abort(404, 'Could not find SessionPlayers with the provided id')


@session_players_api.route('/<string:session_players_id>', methods=['DELETE'])
def delete(session_players_id):
    """Deletes the specified SessionPlayers from the database

    :param session_players_id: The id of the SessionPlayers to be deleted
    :return: 200 if the SessionPlayers was successfully deleted, 404 if the SessionPlayers cannot be found
    """
    try:
        status = SessionPlayersDB.delete(session_players_id)
        if status:
            return '', 200
        else:
            return '', 500
    except ValueError:
        abort(404, 'Could not find SessionPlayers with the provided id')
