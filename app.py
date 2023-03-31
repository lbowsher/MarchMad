from db import db
from flask import Flask
from flask import request
import json

from db import Users
from db import Teams
#from db import Leagues
from db import Players

import os

app = Flask(__name__)
db_filename = "MarchMad.db"

#TODO change this to postgres
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()


#USERS routes
@app.route("/api/users/")
def get_users():
    return json.dumps({"users": [u.serialize() for u in Users.query.all()]}), 200


@app.route("/api/users/", methods=['POST'])
def post_users():
    body = json.loads(request.data)
    username = body.get("username", False)
    if not username:
        return json.dumps({"error": "Invalid fields"}), 400
    else:
        new_user = Users(username=username)
        db.session.add(new_user)
        db.session.commit()
        return json.dumps(new_user.serialize()), 201

@app.route("/api/users/<int:id>/")
def get_user_id(id):
    user = Users.query.filter_by(id=id).first()
    if user is None:
        return json.dumps({"error": "Invalid fields"}), 400
    return json.dumps(user.serialize()), 200

@app.route("/api/users/<int:id>/", methods=['DELETE'])
def del_user_id(id):
    user = Users.query.filter_by(id=id).first()
    if user is None:
        return json.dumps({"error": "Invalid fields"}), 400
    db.session.delete(user)
    db.session.commit()
    return json.dumps(user.serialize()), 200

# PLAYERS routes
@app.route("/api/players/")
def get_players():
    return json.dumps({"players": [p.serialize() for p in Players.query.all()]}), 200

@app.route("/api/players/", methods=['POST'])
def post_players():
    body = json.loads(request.data)
    points = body.get("points", False)
    eliminated = body.get("eliminated", False)
    new_player = Players(points=points, eliminated=eliminated)
    db.session.add(new_player)
    db.session.commit()
    return json.dumps(new_player.serialize()), 201

@app.route("/api/users/<int:id>/")
def get_player_id(id):
    player = Players.query.filter_by(id=id).first()
    if player is None:
        return json.dumps({"error": "Invalid fields"}), 400
    return json.dumps(player.serialize()), 200

@app.route("/api/users/<int:id>/", methods=['DELETE'])
def del_player_id(id):
    player = Players.query.filter_by(id=id).first()
    if player is None:
        return json.dumps({"error": "Invalid fields"}), 400
    db.session.delete(player)
    db.session.commit()
    return json.dumps(player.serialize()), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)