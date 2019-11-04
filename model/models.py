from model.database import db
from sqlalchemy import Column, String, Integer, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship


class Game(db.Model):
    """Model class used to store Game objects in the database
    """
    __tablename__ = 'game'
    id = Column(String, primary_key=True)
    name = Column(String)
    scoring = Column(String)

    def __repr__(self):
        return "<Game(id='%s', name='%s', scoring='%s')>" % \
               (self.id, self.name, self.scoring)

    def to_obj(self):
        """Returns the object in JSON format

        :return: String representation of the object
        """

        return {
            'id': self.id,
            'name': self.name,
            'scoring': self.scoring
        }


class Player(db.Model):
    """Model class used to store Player objects in the database
    """
    __tablename__ = 'player'
    id = Column(String, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return "<Player(id='%s', name='%s')>" % (self.id, self.name)

    def to_obj(self):
        """Returns the object in JSON format

        :return: String representation of the object
        """

        return {
            'id': self.id,
            'name': self.name
        }


class SessionPlayers(db.Model):
    """Model class used to store the Players that participated in a Session
    """
    __tablename__ = 'session-players'
    id = Column(String, primary_key=True)
    session_id = Column(String, ForeignKey('session.id'))
    player_id = Column(String, ForeignKey('player.id'))
    score = Column(Integer)
    team = Column(Integer)
    winner = Column(Boolean)
    session = relationship("Session", back_populates="players")

    def __repr__(self):
        return "<SessionPlayers(id='%s', session_id='%s', player_id='%s', score='%d', team='%d', winner='%s')>" % \
               (self.id, self.session_id, self.player_id, self.score, self.team, self.winner)

    def to_obj(self):
        """Returns the object in JSON format

        :return: String representation of the object
        """

        return {
            'id': self.id,
            'session_id':  self.session_id,
            'player_id': self.player_id,
            'score': self.score,
            'team': self.team,
            'winner': self.winner
        }


class Session(db.Model):
    """Model class used to store the Session information
    """
    __tablename__ = 'session'
    id = Column(String, primary_key=True)
    date = Column(Date)
    game = Column(String, ForeignKey('game.id'))
    players = relationship("SessionPlayers", back_populates="session")

    def __repr(self):
        return "<Session(id='%s', date='%s', game='%s')" % (self.id, self.date, self.game.id)

    def to_obj(self):
        """Returns the object in JSON format

        :return String representation of the object
        """

        return {
            'id': self.id,
            'date': self.date,
            'game_id': self.game,
            'players': [player.to_obj() for player in self.players]
        }
