import os
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, FavoriteCharacter, FavoritePlanet

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = db_url.replace("postgres://", "postgresql://") if db_url else "sqlite:////tmp/test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
Migrate(app, db)
CORS(app)
setup_admin(app)


@app.errorhandler(APIException)
def handle_exception(e):
    return jsonify(e.to_dict()), e.status_code


@app.route("/")
def sitemap():
    return generate_sitemap(app)


@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([u.serialize() for u in users]), 200


@app.route("/people", methods=["GET"])
def get_people():
    characters = Character.query.all()
    return jsonify([c.serialize() for c in characters]), 200


@app.route("/people/<int:people_id>", methods=["GET"])
def get_single_person(people_id):
    character = Character.query.get(people_id)
    if not character:
        return jsonify({"msg": "Character not found"}), 404
    return jsonify(character.serialize()), 200


@app.route("/planets", methods=["GET"])
def get_planets():
    planets = Planet.query.all()
    return jsonify([p.serialize() for p in planets]), 200


@app.route("/planets/<int:planet_id>", methods=["GET"])
def get_single_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"msg": "Planet not found"}), 404
    return jsonify(planet.serialize()), 200


@app.route("/users/favorites", methods=["GET"])
def get_user_favorites():
    user_id = 1
    fav_characters = FavoriteCharacter.query.filter_by(user_id=user_id).all()
    fav_planets = FavoritePlanet.query.filter_by(user_id=user_id).all()

    return jsonify({
        "characters": [f.character.serialize() for f in fav_characters],
        "planets": [f.planet.serialize() for f in fav_planets]
    }), 200


@app.route("/favorite/people/<int:people_id>", methods=["POST"])
def add_favorite_character(people_id):
    user_id = 1

    exists = FavoriteCharacter.query.filter_by(user_id=user_id, character_id=people_id).first()
    if exists:
        return jsonify({"msg": "Already in favorites"}), 400

    new_fav = FavoriteCharacter(user_id=user_id, character_id=people_id)
    db.session.add(new_fav)
    db.session.commit()

    return jsonify(new_fav.character.serialize()), 201


@app.route("/favorite/planet/<int:planet_id>", methods=["POST"])
def add_favorite_planet(planet_id):
    user_id = 1

    exists = FavoritePlanet.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if exists:
        return jsonify({"msg": "Already in favorites"}), 400

    new_fav = FavoritePlanet(user_id=user_id, planet_id=planet_id)
    db.session.add(new_fav)
    db.session.commit()

    return jsonify(new_fav.planet.serialize()), 201


@app.route("/favorite/people/<int:people_id>", methods=["DELETE"])
def delete_favorite_character(people_id):
    user_id = 1

    fav = FavoriteCharacter.query.filter_by(user_id=user_id, character_id=people_id).first()
    if not fav:
        return jsonify({"msg": "Favorite not found"}), 404

    db.session.delete(fav)
    db.session.commit()

    return jsonify({"msg": "Deleted"}), 200


@app.route("/favorite/planet/<int:planet_id>", methods=["DELETE"])
def delete_favorite_planet(planet_id):
    user_id = 1

    fav = FavoritePlanet.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if not fav:
        return jsonify({"msg": "Favorite not found"}), 404

    db.session.delete(fav)
    db.session.commit()

    return jsonify({"msg": "Deleted"}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port, debug=True)