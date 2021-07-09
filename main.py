# importing libraries
from flask import Flask, request, Response, jsonify
from flask_sqlalchemy import SQLAlchemy
import json

# creating an instance of the flask app
app = Flask(__name__)

# Configure our Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initializing our database
db = SQLAlchemy(app)


# the class Movie will inherit the db.Model of SQLAlchemy
class Movie(db.Model):
    __tablename__ = 'movies'  # creating a table name
    id = db.Column(db.Integer, primary_key=True)  # this is the primary key
    title = db.Column(db.String(80), nullable=False)
    year = db.Column(db.String(80), nullable=False)
    genre = db.Column(db.String(80), nullable=False)

    def to_json(self):
        return {"id": self.id, "title": self.title, "year": self.year, "genre": self.genre}

@app.route('/', methods=['GET'])
def get_ini():
  return "Exemplo com api em flask"

# route to get all movies
@app.route('/movies', methods=['GET'])
def get_movies():
    '''Function to get all the movies in the database'''
    
    usuarios_objetos = Movie.query.all()
    movie_json = [movie.to_json() for movie in usuarios_objetos]
    return jsonify({"movies": movie_json})

# route to get movie by id
@app.route('/movies/<int:id>', methods=['GET'])
def get_movie_by_id(id):
 
  ind = Movie.query.filter_by(id=id).first()
  movie_json = ind.to_json()
  return jsonify({"movies":movie_json})

# route to add new movie
@app.route('/movies', methods=['POST'])
def add_movie():
    '''Function to add new movie to our database'''
    request_data = request.get_json()  # getting data from client
    try:
      movie = Movie(title=request_data["title"], year=request_data["year"],genre=request_data["genre"])
      db.session.add(movie)  # add new movie to database session
      db.session.commit() 
      response = Response("Movie added", 201,mimetype='application/json')
      return response
    except Exception as e:
      response = Response("erro", 400,mimetype='application/json')
      print("erro",e)
      return response
   
# route to update movie with PUT method
@app.route('/movies/<int:id>', methods=['PUT'])
def update_movie(id):
    '''Function to edit movie in our database using movie id'''

    movie_to_update = Movie.query.filter_by(id=id).first()
    request_data = request.get_json()

    movie_to_update.title = request_data['title']
    movie_to_update.year = request_data['year']
    movie_to_update.genre = request_data['genre']
    db.session.commit()
    response = Response("Movie Updated",status=200,mimetype='application/json')
    return response

# route to delete movie using the DELETE method
@app.route('/movies/<int:id>', methods=['DELETE'])
def remove_movie(id):
    '''Function to delete movie from our database'''
    Movie.query.filter_by(id=id).delete()
    db.session.commit()
    response = Response("Movie Deleted",status=200,mimetype='application/json')
    return response

app.run(debug=True, host='0.0.0.0', port='8080')
