#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Movie(db.Model):
    __tablename__ = 'movie'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)

    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")

    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")


class MovieSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()


class Director(db.Model):
    __tablename__ = 'director'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class DirectorSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


class Genre(db.Model):
    __tablename__ = 'genre'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class GenreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)

genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)

api = Api(app=app, title="SkyPro: Sergei Levchuk__Home Work 17", )
movie_ns = api.namespace("movies")
director_ns = api.namespace("directors")
genre_ns = api.namespace("genres")


@movie_ns.route('/')
class MoviesView(Resource):
    """
    Запрос всех фильмов. При запросе с параметром
    :parameter- `/movies` — возвращает список всех фильмов, разделенный по страницам;
    :parameter- `/movies/<id>` — возвращает подробную информацию о фильме.

    Организован поиск по режиссерам и жанрам
    :parameter - /movies/?director_id=1
    выводит список фильмов по ID режиссером
    :parameter - /movies/?genre_id=4
    выводит список всех фильмов по ID жанров
    :parameter - /movies/?director_id=2&genre_id=4
    выводит список фильмов по ID режиссера и жанра
    """
    def get(self):
        director = request.args.get("director_id")
        genre = request.args.get("genre_id")

        if director and genre is not None:
            all_movies = Movie.query.filter(Movie.director_id == director).filter(Movie.genre_id == genre)
            return movies_schema.dump(all_movies), 200

        if genre is not None:
            all_movies = Movie.query.filter(Movie.genre_id == genre)
            return movies_schema.dump(all_movies), 200

        if director is None:
            all_movies = db.session.query(Movie).all()
        else:
            all_movies = Movie.query.filter(Movie.director_id == director)
        return movies_schema.dump(all_movies), 200

    def post(self):
        req_json = request.json
        new_movie = Movie(**req_json)

        with db.session.begin():
            db.session.add(new_movie)
        return "", 201


@movie_ns.route('/<int:mid>')
class MoviesView(Resource):
    """
    Реализованы все методы
    :parameter- `/movies` — возвращает список всех фильмов, разделенный по страницам;
    :parameter- `/movies/<id>` — возвращает подробную информацию о фильме.

    :parameter- `POST /movies/` —  добавляет кино в фильмотеку,
    :parameter- `PUT /movies/<id>` —  обновляет кино,
    :parameter- `DELETE /movies/<id>` —  удаляет кино.
    """
    def get(self, mid: int):
        try:
            movie = db.session.query(Movie).filter(Movie.id == mid).one()
            return movie_schema.dump(movie), 200
        except Exception as e:
            return str(e), 404

    def put(self, mid):
        movie = db.session.query(Movie).get(mid)
        req_json = request.json

        movie.title = req_json.get("title")
        movie.description = req_json.get("description")
        movie.trailer = req_json.get("trailer")
        movie.year = req_json.get("year")
        movie.rating = req_json.get("rating")
        movie.genre_id = req_json.get("genre_id")
        movie.director_id = req_json.get("director_id")

        db.session.add(movie)
        db.session.commit()

        return "", 204

    def patch(self, mid):
        movie = db.session.query(Movie).get(mid)
        req_json = request.json

        if "title" in req_json:
            movie.title = req_json.get("title")
        if "description" in req_json:
            movie.description = req_json.get("description")
        if "trailer" in req_json:
            movie.trailer = req_json.get("trailer")
        if "year" in req_json:
            movie.year = req_json.get("year")
        if "rating" in req_json:
            movie.rating = req_json.get("rating")
        if "genre_id" in req_json:
            movie.genre_id = req_json.get("genre_id")
        if "director_id" in req_json:
            movie.director_id = req_json.get("director_id")

        db.session.add(movie)
        db.session.commit()

        return "", 204

    def delete(self, mid):
        movie = db.session.query(Movie).get(mid)

        db.session.delete(movie)
        db.session.commit()

        return "", 204


@director_ns.route('/')
class DirectorView(Resource):
    """
    :parameter- `/directors/` — возвращает всех режиссеров,
    :parameter- `/directors/<id>` — возвращает подробную информацию о режиссере,

    :parameter- `POST /directors/` —  добавляет режиссера,
    :parameter- `PUT /directors/<id>` —  обновляет режиссера,
    :parameter- `DELETE /directors/<id>` —  удаляет режиссера.
    """
    def get(self):
        all_directors = db.session.query(Director).all()
        return directors_schema.dump(all_directors), 200

    def post(self):
        req_json = request.json
        new_director = Director(**req_json)

        with db.session.begin():
            db.session.add(new_director)
        return "", 201


@director_ns.route('/<int:did>')
class DirectorView(Resource):
    """
    :parameter- `/directors/` — возвращает всех режиссеров,
    :parameter- `/directors/<id>` — возвращает подробную информацию о режиссере,

    :parameter- `POST /directors/` —  добавляет режиссера,
    :parameter- `PUT /directors/<id>` —  обновляет режиссера,
    :parameter- `DELETE /directors/<id>` —  удаляет режиссера.
    """
    def get(self, did: int):
        try:
            director = db.session.query(Director).filter(Director.id == did).one()
            return director_schema.dump(director), 200
        except Exception as e:
            return str(e), 404

    def put(self, did):
        director = db.session.query(Director).get(did)
        req_json = request.json

        director.name = req_json.get("name")

        db.session.add(director)
        db.session.commit()

        return "", 204

    def patch(self, did):
        director = db.session.query(Director).get(did)
        req_json = request.json

        if "name" in req_json:
            director.name = req_json.get("name")

        db.session.add(director)
        db.session.commit()

        return "", 204

    def delete(self, did):
        director = db.session.query(Director).get(did)

        db.session.delete(director)
        db.session.commit()

        return "", 204


@genre_ns.route('/')
class GenreView(Resource):
    """
    :parameter- `/genres/` —  возвращает все жанры,
    :parameter- `/genres/<id>` — возвращает информацию о жанре с перечислением списка фильмов по жанру,

    :parameter- `POST /genres/` —  добавляет жанр,
    :parameter- `PUT /genres/<id>` —  обновляет жанр,
    :parameter- `DELETE /genres/<id>` —  удаляет жанр.
    """
    def get(self):
        all_genres = db.session.query(Genre).all()
        return genres_schema.dump(all_genres), 200

    def post(self):
        req_json = request.json
        new_genre = Genre(**req_json)

        with db.session.begin():
            db.session.add(new_genre)
        return "", 201


@genre_ns.route('/<int:gid>')
class GenreView(Resource):
    """
    :parameter- `/genres/` —  возвращает все жанры,
    :parameter- `/genres/<id>` — возвращает информацию о жанре с перечислением списка фильмов по жанру,

    :parameter- `POST /genres/` —  добавляет жанр,
    :parameter- `PUT /genres/<id>` —  обновляет жанр,
    :parameter- `DELETE /genres/<id>` —  удаляет жанр.
    """
    def get(self, gid: int):
        try:
            genre = db.session.query(Genre).filter(Genre.id == gid).one()
            return genre_schema.dump(genre), 200
        except Exception as e:
            return str(e), 404

    def put(self, gid):
        genre = db.session.query(Genre).get(gid)
        req_json = request.json

        genre.name = req_json.get("name")

        db.session.add(genre)
        db.session.commit()

        return "", 204

    def patch(self, gid):
        genre = db.session.query(Genre).get(gid)
        req_json = request.json

        if "name" in req_json:
            genre.name = req_json.get("name")

        db.session.add(genre)
        db.session.commit()

        return "", 204

    def delete(self, gid):
        genre = db.session.query(Genre).get(gid)

        db.session.delete(genre)
        db.session.commit()

        return "", 204


if __name__ == '__main__':
    app.run(debug=True)
