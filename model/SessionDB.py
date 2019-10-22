from model.database import db
from model.models import Session
from uuid import uuid4


def get_all():
    """Returns all of the Session objects in the database

    :return A list of Session objects
    :rtype list
    """
    return Session.query.all()


def get(session_id):
    """Returns the Session object specified by the provided id

    :param session_id: The id of the Session to retrieve, nominally a uuid
    :return A single Session object
    :rtype Session
    """
    return Session.query.filter_by(id=session_id).first()


def create(date, game_id, session_id=None):
    """Creates a Session given the provided values

    :param date: The date of the session
    :param game_id: The id of the game the session belongs to
    :param session_id: The id to assign to the Session.  If not provided, a uuid will be generated
    :return The created Session object
    :rtype: Session
    """

    if session_id is None:
        session_id = str(uuid4())

    new_session = Session(id=session_id, date=date, game=game_id)

    db.session.add(new_session)
    db.session.commit()

    return new_session


def update(session_id, date=None, game_id=None):
    """Updates the specified Session with the provided values

    :param session_id: The id of the Session to be updated
    :param date: If provided, the date to set the specified Session to
    :param game_id: If provided, the game id to set the specified Session to
    :return The updated Session object
    :rtype Session
    :raise ValueError if the Session could not be found
    """
    session_to_update = Session.query.filter_by(id=session_id).first()

    if session_to_update is None:
        raise ValueError("Could not find Session with id")

    if date is not None:
        session_to_update.date = date

    if game_id is not None:
        session_to_update.game_id = game_id

    db.session.commit()

    return session_to_update


def delete(session_id):
    """Deletes the Session specified by the provided session_id

    :param session_id: The id of the Session to be deleted
    :return True if the Session was successfully deleted
    :raise ValueError if the Session could not be found
    """

    session_to_delete = Session.query.filter_by(id=session_id).first()

    if session_to_delete is None:
        raise ValueError("Could not find Session with id")

    db.session.delete(session_to_delete)
    db.session.commit()

    return True
