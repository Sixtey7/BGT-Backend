from model.database import db
from model.models import Player
from uuid import uuid4


def get_all():
    """Returns all of the Player objects in the database

    :return A list of Player objects
    :rtype list
    """
    return Player.query.all()


def get(player_id):
    """Returns the Player object specified by the provided id

    :param player_id: The id of the Player to retrieve, nominally a uuid
    :return A single Player object
    :rtype Player
    """
    return Player.query.filter_by(id=player_id).first()


def create(name, player_id=None):
    """Creates a Player given the provided values

    :param name: The string name of the Player to create
    :param player_id: The id to assign to the Player.  If not provided, a uuid will be generated
    :return The created Player object
    :rtype: Player
    """

    if player_id is None:
        player_id = str(uuid4())

    new_player = Player(id=player_id, name=name)

    db.session.add(new_player)
    db.session.commit()

    return new_player


def update(player_id, name=None):
    """Updates the specified Player with the provided values

    :param player_id: The id of the Player to be updated
    :param name: If provided, the name to set the specified Player to
    :return The updated Player object
    :rtype Player
    :raise ValueError if the Player could not be found
    """
    player_to_update = Player.query.filter_by(id=player_id).first()

    if player_to_update is None:
        raise ValueError("Could not find Player with id")

    if name is not None:
        player_to_update.name = name

    db.session.commit()

    return player_to_update


def delete(player_id):
    """Deletes the Player specified by the provided player_id

    :param player_id: The id of the Player to be deleted
    :return True if the Player was successfully deleted
    :raise ValueError if the Player could not be found
    """

    player_to_delete = Player.query.filter_by(id=player_id).first()

    if player_to_delete is None:
        raise ValueError("Could not find Player with id")

    db.session.delete(player_to_delete)
    db.session.commit()

    return True
