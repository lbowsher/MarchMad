from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Users class has 3 values:
#   id is a primary key int
#   username is a string
#   teams is a collection of leagues that each user is 
#       in for the Leagues db
class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    #TODO: do teams
    #teams = db.relationship("Teams", cascade='delete')

    def __init__(self, **kwargs):
        self.username = kwargs.get("username")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            #"teams": [t.serialize() for l in self.teams]
        }

# create a class called Teams that stores the following values:
#  id is a primary key int
#  league id is a foreign key to the Leagues db
#  owner_id is a foreign key to the Users db
#  players is a collection of players that are in this team
class Teams(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    league_id = db.Column(db.Integer, db.ForeignKey("leagues.id"))
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    players = db.relationship("Players", cascade='delete')

    def __init__(self, **kwargs):
        self.league_id = kwargs.get("league_id")
        self.owner_id = kwargs.get("owner_id")

    def serialize(self):
        return {
            "id": self.id,
            "league_id": self.league_id,
            "owner_id": self.owner_id,
            "players": [p.serialize() for p in self.players]
        }

#TODO: Leagues db
# class Leagues(db.Model):
#     __tablename__ = 'leagues'
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
#     top_id = db.Column(db.Integer, nullable=False)
#     bottom_id = db.Column(db.Integer, nullable=False)

#     def __init__(self, **kwargs):
#         self.user_id = kwargs.get("user_id")
#         self.top_id = kwargs.get("top_id")
#         self.bottom_id = kwargs.get("bottom_id")

#     def serialize(self):
#         return {
#             "id": self.id,
#             "user_id": self.user_id,
#             "top_id": self.top_id,
#             "bottom_id": self.bottom_id
#         }

class Players(db.Model):
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key=True)
    # TODO: update to be list of points scored each game
    points = db.Column(db.Integer, nullable=False)
    eliminated = db.Column(db.Boolean, nullable=False) 
    # true when team has lost in march madness tourney

    def __init__(self, **kwargs):
        self.points = kwargs.get("points", __default=0)
        self.eliminated = kwargs.get("eliminated", __default=False)

    def serialize(self):
        return {
            "id": self.id,
            # TODO: update to be list of points scored each game
            "points": self.points,
            "eliminated": self.eliminated
        }
