from model.database import db
from model.models import Game
from uuid import uuid4


def get_all():
    """Returns all of the Game objects in the database

    :return A list of Game objects
    :rtype list
    """
    return Game.query.all()


def get(game_id):
    """Returns the Game object specified by the provided id

    :param game_id: The id of the Game to retrieve, nominally a uuid
    :return A single Game object
    :rtype Game
    """
    return Game.query.filter_by(id=game_id).first()


def create(name, scoring, game_id=None):
    """Creates a Game given the provided values

    :param name: The string name of the Game to create
    :param scoring: The scoring type to use for the Game
    :param game_id: The id to assign to the Game.  If not provided, a uuid will be generated
    :return The created Game object
    :rtype: Game
    """

    if game_id is None:
        game_id = str(uuid4())

    new_game = Game(id=game_id, name=name, scoring=scoring)

    db.session.add(new_game)
    db.session.commit()

    return new_game


def update(game_id, name=None, scoring=None):
    """Updates the specified Game with the provided values

    :param game_id: The id of the Game to be updated
    :param name: If provided, the name to set the specified Game to
    :param scoring: If provided, the scoring to set the specified Game to
    :return The updated Game object
    :rtype Game
    :raise ValueError if the Game could not be found
    """
    game_to_update = Game.query.filter_by(id=game_id).first()

    if game_to_update is None:
        raise ValueError("Could not find Game with id")

    if name is not None:
        game_to_update.name = name

    if scoring is not None:
        game_to_update.scoring = scoring

    db.session.commit()

    return game_to_update


def delete(game_id):
    """Deletes the Game specified by the provided game_id

    :param game_id: The id of the Game to be deleted
    :return True if the Game was successfully deleted
    :raise ValueError if the Game could not be found
    """

    game_to_delete = Game.query.filter_by(id=game_id).first()

    if game_to_delete is None:
        raise ValueError("Could not find Game with id")

    db.session.delete(game_to_delete)
    db.session.commit()

    return True
