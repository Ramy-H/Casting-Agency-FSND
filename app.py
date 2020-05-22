import os
from flask import Flask, request, abort, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from models import setup_db, Movie, Actor
from auth import AuthError, requires_auth

MOVIES_PER_PAGE = 10


def paginate(request, data):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * MOVIES_PER_PAGE
    end = start + MOVIES_PER_PAGE
    data = data[start:end]
    return data


def formatt(data):
    data = [datum.format() for datum in data]
    return data


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app)
    setup_db(app)

    # Set up cors and allow '*' for origins
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Use the after_request decorator to set Access-Control-Allow
    @app.after_request
    def add_cors_headers(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, PUT, POST, DELETE, OPTIONS')
        return response

    @app.route('/')
    def index():
        return jsonify({'message': 'Hello'})

# GET all available movies.
    @app.route('/movies')
    @requires_auth("get:movies_details")
    def get_movies(token):
        movies = Movie.query.all()
        if len(movies) == 0:
            abort(404)
        try:
            movies = paginate(request, movies)
            movies = formatt(movies)
            return jsonify({
                'success': True,
                'movies': movies
                }), 200
        except:
            abort(400)

# GET all available actors.
    @app.route('/actors')
    @requires_auth("get:actors_details")
    def get_actors(token):
        # movies = Movie.query.order_by(Movie.id).all()
        actors = Actor.query.all()

        if len(actors) == 0:
            abort(404)
        try:
            actors = formatt(actors)
            data = paginate(request, actors)

            if len(actors) < 1:
                abort(404)
            else:
                return jsonify({
                    'total_actors': len(actors),
                    'actors': data,
                    'success': True
                    }), 200
        except:
            abort(400)

# POST a new movie#
    @app.route('/post_movie', methods=['POST'])
    @requires_auth("post:movies")
    def post_movie(token):
        try:
            body = request.get_json()
            title = body.get('title', None)
            date = body.get('date', None)
            movie = Movie(title=title, date=date)
            movie.insert()
            return jsonify({
                'success': True
                }), 200
        except:
            abort(422)

# POST a new actor#
    @app.route('/post_actor', methods=['POST'])
    @requires_auth("post:actors")
    def post_actor(token):
        try:
            body = request.get_json()
            name = body.get('name', None)
            age = body.get('age', None)
            gender = body.get('gender', None)
            actor = Actor(name=name, age=age, gender=gender)
            actor.insert()
            return jsonify({
                'success': True
                }), 200
        except:
            abort(422)

# DELETE movie.
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth("delete:movies")
    def delete_movie(token, movie_id):
        movie = Movie.query.filter_by(id=movie_id).one_or_none()
        if not movie:
            abort(404)
        try:
            movie.delete()
            return jsonify({
                'success': True
                }), 200
        except:
            abort(422)

# DELETE actor.
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth("delete:actors")
    def delete_actor(token, actor_id):
        actor = Actor.query.filter_by(id=actor_id).one_or_none()
        if not actor:
            abort(404)
        try:
            actor.delete()
            return jsonify({
                'success': True
                }), 200
        except:
            abort(422)

# Edit Movie
    @app.route("/movies/<movie_id>", methods=['PATCH'])
    @requires_auth("patch:movies")
    def edit_movies(token, movie_id):
        try:
            movie = Movie.query.filter_by(id=movie_id).one_or_none()
            body = request.get_json()
            edit_title = body.get('title', None)
            edited_date = body.get('date', None)

            if edit_title is None and edited_date is None:
                abort(400)

            if edit_title:
                movie.title = edit_title
            if edited_date:
                movie.date = edited_date

            movie.update()
            return jsonify({
                "success": True
                }), 200
        except:
            abort(404)

# Edit Actor
    @app.route("/actors/<actor_id>", methods=['PATCH'])
    @requires_auth("patch:actors")
    def edit_actor(token, actor_id):
        body = request.get_json()
        edit_name = body.get('name', None)
        edit_age = body.get('age', None)
        edit_gender = body.get('gender', None)

        if edit_name is None and edit_age is None and edit_gender is None:
            abort(422)

        try:
            actor = Actor.query.filter_by(id=actor_id).one_or_none()

            if edit_name:
                actor.name = edit_name
            if edit_age:
                actor.age = edit_age
            if edit_gender:
                actor.gender = edit_gender

            actor.update()
            return jsonify({
                "success": True
                }), 200
        except:
            abort(404)


# Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource not found"
            }), 404

    @app.errorhandler(422)
    def not_processed(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Request cannot be processed"
            }), 422

    @app.errorhandler(400)
    def not_successful(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Request failed"
            }), 400

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
            }), error.status_code

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
