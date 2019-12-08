from model.database import db
from model.models import SessionPlayers
from uuid import uuid4


def get_all():
    """Returns all of the SessionPlayers objects in the database

    :return A list of SessionPlayers objects
    :rtype list
    """
    return SessionPlayers.query.all()


def get(session_players_id):
    """Returns the SessionPlayers object specified by the provided id

    :param session_players_id: The id of the SessionPlayers to retrieve, nominally a uuid
    :return A single SessionPlayers object
    :rtype SessionPlayers
    """
    return SessionPlayers.query.filter_by(id=session_players_id).first()


def create(session_id, player_id, score, team, winner, session_players_id=None):
    """Creates a SessionPlayers given the provided values

    :param session_id: The id of the session that the SessionPlayers object belongs to
    :param player_id: The id of the player that the SessionPlayers object belongs to
    :param score: The score of the SessionPlayers object
    :param team: The team of the SessionPlayers object
    :param winner: Boolean to store if this SessionPlayers object was a winner
    :param session_players_id: The id to assign to the SessionPlayers.  If not provided, a uuid will be generated
    :return The created SessionPlayers object
    :rtype: SessionPlayers
    """

    if session_players_id is None:
        session_players_id = str(uuid4())

    new_session_players = SessionPlayers(id=session_players_id,
                                         session_id=session_id,
                                         player_id=player_id,
                                         score=score,
                                         team=team,
                                         winner=winner)

    db.session.add(new_session_players)
    db.session.commit()

    return new_session_players


def update(session_players_id, session_id=None, player_id=None, score=None, team=None, winner=None):
    """Updates the specified SessionPlayers with the provided values

    :param session_players_id: The id of the SessionPlayers to be updated
    :param session_id: If provided, the session_id to set the specified SessionPlayers to
    :param player_id: If provided, the player_id to set the specified SessionPlayers to
    :param score: If provided, the score to set the specified SessionPlayers to
    :param team: If provided, the team to set the specified SessionPlayers to
    :param winner: If provided, the winner to set the specified SessionPlayers to
    :return The updated SessionPlayers object
    :rtype SessionPlayers
    :raise ValueError if the SessionPlayers could not be found
    """
    session_players_to_update = SessionPlayers.query.filter_by(id=session_players_id).first()

    if session_players_to_update is None:
        raise ValueError("Could not find SessionPlayers with id")

    if session_id is not None:
        session_players_to_update.session_id = session_id

    if player_id is not None:
        session_players_to_update.player_id = player_id

    if score is not None:
        session_players_to_update.score = score

    if team is not None:
        session_players_to_update.team = team

    if winner is not None:
        session_players_to_update.winner = winner

    db.session.commit()

    return session_players_to_update


def merge(session_id, player_id, score, team, winner, session_players_id=None):
    """Creates or Updates a SessionPlayers given the provided values

    :param session_id: The id of the session that the SessionPlayers object belongs to
    :param player_id: The id of the player that the SessionPlayers object belongs to
    :param score: The score of the SessionPlayers object
    :param team: The team of the SessionPlayers object
    :param winner: Boolean to store if this SessionPlayers object was a winner
    :param session_players_id: The id to assign to the SessionPlayers.  If not provided, a uuid will be generated
    :return The created SessionPlayers object
    :rtype: SessionPlayers
    """

    if session_players_id is None:
        session_players_id = str(uuid4())

    new_session_players = SessionPlayers(id=session_players_id,
                                         session_id=session_id,
                                         player_id=player_id,
                                         score=score,
                                         team=team,
                                         winner=winner)

    db.session.merge(new_session_players)
    db.session.commit()

    return new_session_players


def merge_all(session_id, session_player_list):
    """Creates or updates all of the SessionPlayers in the provided list

    :param session_id: The id of the session to add the session players to
    :param session_player_list: A list of session player entries to be merged
    :return a list of all of the added/modified session players
    :raise ValueError if a required value is not provided
    """

    if session_player_list is None:
        raise ValueError("session_list is required")

    print('length of array was %d' % len(session_player_list))

    return_vals = []

    for session_player in session_player_list:
        return_vals.append(merge(session_id,
                                 session_player.player_id,
                                 session_player.score,
                                 session_player.team,
                                 session_player.winner,
                                 session_player.id))

    return return_vals


def delete(session_players_id):
    """Deletes the SessionPlayers specified by the provided session_players_id

    :param session_players_id: The id of the SessionPlayers to be deleted
    :return True if the SessionPlayers was successfully deleted
    :raise ValueError if the SessionPlayers could not be found
    """

    session_players_to_delete = SessionPlayers.query.filter_by(id=session_players_id).first()

    if session_players_to_delete is None:
        raise ValueError("Could not find SessionPlayers with id")

    db.session.delete(session_players_to_delete)
    db.session.commit()

    return True
