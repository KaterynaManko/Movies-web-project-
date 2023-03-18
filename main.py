from flask import Flask, render_template, request, url_for, redirect, flash
import tmdb_client
import datetime
from waitress import serve


app = Flask(__name__)
app.secret_key = b'my-secret'

FAVORITES = set()

@app.route('/')
def homepage(): 
    types = [{'type': "top_rated", 'name': "Top Rated"},
             {'type': "upcoming", 'name': "Upcoming"},
             {'type': "popular", 'name': "Popular"},
             {'type': "now_playing", 'name': "Now Playing"}]
    
    selected_list = request.args.get('list_type', "popular")
    movies = tmdb_client.get_movies(how_many=8, list_type=selected_list)
    return render_template("homepage.html", movies=movies, current_list=selected_list, types=types)
        
   
@app.context_processor 
def utility_processor():
    def tmdb_image_url(path, size): 
     return tmdb_client.get_poster_url(path, size)
    return {"tmdb_image_url": tmdb_image_url}

@app.route("/movie/<movie_id>")
def movie_details(movie_id):
    details = tmdb_client.get_single_movie(movie_id)
    cast = tmdb_client.get_actors(movie_id, how_many=8)
    return render_template("movie_details.html", movie=details, cast=cast)

@app.context_processor
def utility_processor():
    def tmdb_image_url_movie(path, size):
     return tmdb_client.get_poster_url_movie(path, size)
    return {"tmdb_image_url_movie": tmdb_image_url_movie}

@app.context_processor
def utility_processor():
    def tmdb_image_url_actor(path, size):
     return tmdb_client.get_poster_url_actor(path, size)
    return {"tmdb_image_url_actor": tmdb_image_url_actor}

@app.errorhandler(404)
def handle_exception(error):
    return homepage()

@app.route('/search')
def search():
    search_query = request.args.get("q", "")
    if search_query:
        movies = tmdb_client.search(search_query=search_query)
    else:
        movies = []
    return render_template("search.html", movies=movies, search_query=search_query)

@app.route('/today')
def today():
    movies = tmdb_client.get_airing_today()
    today = datetime.date.today()
    return render_template("today.html", movies=movies, today=today)

@app.route("/favorites/add", methods=['POST'])
def add_to_favorites():
    data = request.form
    movie_id = data.get('movie_id')
    movie_title = data.get('movie_title')
    if movie_id and movie_title:
        FAVORITES.add(movie_id)
        flash(f'Додано фільм {movie_title} до улюблених!')
    return redirect(url_for('homepage'))

@app.route("/favorites")
def show_favorites():
    if FAVORITES:
        movies = []
        for movie_id in FAVORITES:
            movie_details = tmdb_client.get_single_movie(movie_id)
            movies.append(movie_details)
    else:
        movies = []
    return render_template("homepage.html", movies=movies)
    
if __name__ == '__main__':
    serve(app, host='127.0.0.1', port=8080, threads=2)
    
