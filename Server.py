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

def encode_actor(actor):
    if isinstance(actor, Actor):
        return(actor._name, actor._age, actor._moviegross)
    else:
        raise TypeError

def encode_movie(movie):
    if isinstance(movie, Movie):
        return(movie._name, movie._year, movie._gross)

@app.route('/api/actors/<actor_name>', methods=['GET'])
def get_actor(actor_name):
    printable = set(string.printable)
    namestr = filter(lambda x: x in printable, actor_name)
    actor = graph.getactor(namestr)
    coded = json.dumps(actor, default=encode_actor)
    return coded

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
    return coded


@app.route('/api/movies/<movie_name>', methods=['GET'])
def get_movie(movie_name):
    movie = graph.getmovie(movie_name)
    coded = json.dumps(movie, default=encode_movie)
    return coded

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
    return coded

@app.route('/api/update/actors/<actor_name>', methods=['PUT'])
def update_actor():
    

if __name__ == "__main__":
    app.run(debug=True)
