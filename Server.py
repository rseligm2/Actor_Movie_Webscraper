from flask import Flask, Response, request
from Graph import Graph
from Movie import Movie
from Actor import Actor
from GraphFromData import GraphFromData
import json
import string

app = Flask(__name__)

graph = Graph()
jsondata = GraphFromData("data.json")
graph = jsondata.createGraph()


# json encoder for Actor object
def encode_actor(actor):
    if isinstance(actor, Actor):
        return (actor._name, actor._age, actor._moviegross)

    else:
        raise TypeError


# json encoder for Movie object
def encode_movie(movie):
    if isinstance(movie, Movie):
        return (movie._name, movie._year, movie._gross)


# get api method for actor
@app.route('/api/actors/<actor_name>', methods=['GET'])
def get_actor(actor_name):
    printable = set(string.printable)
    namestr = filter(lambda x: x in printable, actor_name)
    actor = graph.getactor(namestr)
    coded = json.dumps(actor, default=encode_actor)
    return Response(coded, status=200, mimetype='application/json')


# get method to filter actors by attribute
@app.route('/api/get_filter_actors', methods=['GET'])
def get_filter_actors():
    namestr = request.args.get('name')
    age = request.args.get('age')
    actors = graph.getfilteractors(namestr, age)
    coded = ""
    if not actors:
        return Response("{400 Bad Request}", status=400, mimetype='application/json')
    for actor in actors:
        coded = coded + json.dumps(actor, default=encode_actor) + "\n"
    return Response(coded, status=200, mimetype='application/json')


# get method for singl movie
@app.route('/api/movies/<movie_name>', methods=['GET'])
def get_movie(movie_name):
    movie = graph.getmovie(movie_name)
    coded = json.dumps(movie, default=encode_movie)
    return Response(coded, status=200, mimetype='application/json')


# get method to filter movies by attribute
@app.route('/api/get_filter_movies', methods=['GET'])
def get_filter_movies():
    namestr = request.args.get('name')
    year = request.args.get('year')
    movies = graph.getfiltermovies(namestr, year)
    coded = ""
    if not movies:
        return Response("{400 Bad Request}", status=400, mimetype='application/json')
    for movie in movies:
        coded = coded + json.dumps(movie, default=encode_movie) + "\n"
    return Response(coded, status=200, mimetype='application/json')


# Actor put method to update attributes
@app.route('/api/update/actors/<actor_name>', methods=['PUT'])
def update_actor(actor_name):
    if request.headers['Content-Type'] == 'application/json':
        actor = graph.getactor(actor_name)
        updata = request.json
        updatethis = updata.keys()[0]
        newval = updata[updatethis]
        if updatethis == "age":
            actor._age = newval
            return Response("Successfully Updated", status=200, mimetype='application/json')
        elif updatethis == "total_gross":
            actor._moviegross = newval
            return Response("Successfully Updated", status=200, mimetype='application/json')
        else:
            return Response("{400 Bad Request}", status=400, mimetype='application/json')
    else:
        return Response("{400 Bad Request Content Type}", status=400, mimetype='application/json')


# movie put method to update attributes
@app.route('/api/update/movies/<movie_name>', methods=['PUT'])
def update_movie(movie_name):
    if request.headers['Content-Type'] == 'application/json':
        movie = graph.getmovie(movie_name)
        updata = request.json
        updatethis = updata.kys()[0]
        newval = updata[updatethis]
        if updatethis == "box_office":
            movie._gross = newval
            return Response("Successfully Updated", status=200, mimetype='application/json')
        elif updatethis == "year":
            movi._year = newval
            return Response("Successfully Updated", status=200, mimetype='application/json')
        else:
            return Response("{400 Bad Request}", status=400, mimetype='application/json')
    else:
        return Response("{400 Bad Request Content Type}", status=400, mimetype='application/json')


if __name__ == "__main__":
    app.run(debug=True)
