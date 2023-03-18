from main import app
from unittest.mock import Mock
import pytest

       
@pytest.mark.parametrize('url, list_type', [
    ('?list_type=top_rated', 'top_rated'),
    ('?list_type=upcoming', 'upcoming'),
    ('?list_type=now_playing','now_playing')
])
def test_homepage(monkeypatch, url, list_type):
   api_mock = Mock(return_value={'results': []})
   monkeypatch.setattr("tmdb_client.call_tmdb_api", api_mock)
   with app.test_client() as client:
    response = client.get(f'/{url}')
    assert response.status_code == 200
    api_mock.assert_called_once_with(f"movie/{list_type}")
          