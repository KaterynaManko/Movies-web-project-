import tmdb_client
from tmdb_client import get_single_movie_cast
import unittest
from unittest.mock import Mock
import responses

def test_get_poster_url_movie_uses_default_size():
   backdrop_path = "some-poster-path"
   expected_default_size = 'w780'
   backdrop_url = tmdb_client.get_poster_url_movie(backdrop_path=backdrop_path)
   assert expected_default_size in backdrop_url
   
def test_get_poster_url_movie():
   backdrop_path = "some-poster-path"
   expected_default_size = 'w780'
   backdrop_url = tmdb_client.get_poster_url_movie(backdrop_path=backdrop_path)
   assert backdrop_url == "https://image.tmdb.org/t/p/w780/some-poster-path"
   
def test_get_single_movie(monkeypatch):
   mock_single_movie = ['Movie 1']
   requests_mock = Mock()
   response = requests_mock.return_value
   response.json.return_value = mock_single_movie
   monkeypatch.setattr("tmdb_client.requests.get", requests_mock)
   single_movie = tmdb_client.get_single_movie(movie_id='315162')
   assert single_movie == mock_single_movie

class TestGetSingleMovieCast(unittest.TestCase):
   @responses.activate
   def test_get_single_movie_cast(self):
      responses.get(
         url="https://api.themoviedb.org/3/movie/631842/credits",
         json={'cast': 'actor'}
      )
      self.assertEqual(get_single_movie_cast(631842), 'actor')  