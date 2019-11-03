from flask import Flask
from model.database import db
from routes.game_routes import game_api
from routes.player_routes import player_api
from routes.session_routes import session_api
from routes.session_players_routes import session_players_api
from flask_cors import CORS

# create the flask app
app = Flask(__name__)
# add in CORS support
CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})
    
app.register_blueprint(game_api, url_prefix="/games/")
app.register_blueprint(player_api, url_prefix="/players")
app.register_blueprint(session_api, url_prefix="/sessions/")
app.register_blueprint(session_players_api, url_prefix="/session-players")


# SQLAlchemy config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///model/bgt-backend.db'
app.config['SQLALCHEMY_ECHO'] = True
db.init_app(app)

db.app = app

# Create all of the tables
# Note: The below line comes back as not used, but I believe I need
# to make sure the tables get created
import model.models
db.create_all()

app.run(port=5000, debug=True)
