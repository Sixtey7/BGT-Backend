from flask import Blueprint, abort, jsonify, request
import model.SessionDB as SessionDB

session_api = Blueprint('session_api', __name__)


@session_api.route('', methods=['GET'])
def get_all():
    """Returns all of the Sessions that exist in the database

    :return the result as a json array
    """
    return jsonify([session.to_obj() for session in SessionDB.get_all()]), 200


@session_api.route('<string:session_id>', methods=['GET'])
def get(session_id):
    """Returns the Session specified by the provided session_id

    :param session_id: The id of the Session to return
    :return 200 and the specified Session object, or 404 if no Session was found with the specified id
    """
    session_obj = SessionDB.get(session_id)
    if session_obj is None:
        abort(404, 'No Session found for given id!')

    return jsonify(session_obj.to_obj()), 200


@session_api.route('', methods=['POST'])
def create():
    """Used to create a new Session.

    Expects the details of the Session in JSON format as part of the request body
    If no id is provided, an Id will be generated as part of the Session creation

    :return 200 and the newly created Session or 400 if no request body was found
    """
    if not request.json:
        abort(400, 'No request body provided!')

    session = SessionDB.create(request.json['date'],
                               request.json['game_id'],
                               request.json['id'] if 'id' in request.json else None)

    return jsonify(session.to_obj()), 200


@session_api.route('<string:session_id>', methods=['PUT'])
def update(session_id):
    """Updates the specified Session with the contents of the request body (in JSON)

    Expects either (or both) of "date" and "game_id" to be provided in the request body

    :param session_id: the id of the Session to be updated
    :return 200 and the updated Session, 400 if no request body has been provided
        404 if the specified Session cannot be found
    """
    if not request.json:
        abort(400, 'No request body provided')

    try:
        session = SessionDB.update(session_id,
                                   request.json['date'] if 'date' in request.json else None,
                                   request.json['game_id'] if 'game_id' in request.json else None)
        return jsonify(session.to_obj()), 200
    except ValueError:
        abort(404, 'Could not find Session with the provided id')


@session_api.route('<string:session_id>', methods=['DELETE'])
def delete(session_id):
    """Deletes the specified Session from the database

    :param session_id: The id of the Session to be deleted
    :return: 200 if the Session was successfully deleted, 404 if the Session cannot be found
    """
    try:
        status = SessionDB.delete(session_id)
        if status:
            return '', 200
        else:
            return '', 500
    except ValueError:
        abort(404, 'Could not find Session with the provided id')
