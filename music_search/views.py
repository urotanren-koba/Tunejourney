import os
import requests
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponseRedirect
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyException
import random
import string
from dotenv import load_dotenv

# .envファイルからAPIキーをロード
load_dotenv()
NEWS_API_KEY = os.getenv('NEWS_API_KEY')

def top_page(request):
    return render(request, 'music_search/top.html')

def get_recommendations(request):
    query = request.GET.get('query', 'Jazz')
    search_type = request.GET.get('type', 'track')

    sp = Spotify(auth_manager=SpotifyOAuth(
        client_id=settings.SPOTIPY_CLIENT_ID,
        client_secret=settings.SPOTIPY_CLIENT_SECRET,
        redirect_uri=settings.SPOTIPY_REDIRECT_URI,
        scope="user-library-read"
    ))

    try:
        results = sp.search(q=query, type=search_type, limit=50)
        tracks = results['tracks']['items'] if search_type == 'track' else []
    except SpotifyException as e:
        print(f"Spotify API error: {e}")
        tracks = []

    return render(request, 'music_search/index.html', {'tracks': tracks})

def random_preview(request):
    sp = Spotify(auth_manager=SpotifyOAuth(
        client_id=settings.SPOTIPY_CLIENT_ID,
        client_secret=settings.SPOTIPY_CLIENT_SECRET,
        redirect_uri=settings.SPOTIPY_REDIRECT_URI,
        scope="user-library-read"
    ))

    random_letter = random.choice(string.ascii_lowercase)
    
    try:
        results = sp.search(q=random_letter, type='track', limit=50)
        tracks = [track for track in results['tracks']['items'] if track['preview_url']]
    except SpotifyException as e:
        print(f"Spotify API error: {e}")
        tracks = []

    return render(request, 'music_search/random_preview.html', {'tracks': tracks})

def login(request):
    sp_oauth = SpotifyOAuth(
        client_id=settings.SPOTIPY_CLIENT_ID,
        client_secret=settings.SPOTIPY_CLIENT_SECRET,
        redirect_uri=settings.SPOTIPY_REDIRECT_URI,
        scope="user-library-read"
    )
    auth_url = sp_oauth.get_authorize_url()
    return HttpResponseRedirect(auth_url)

def callback(request):
    sp_oauth = SpotifyOAuth(
        client_id=settings.SPOTIPY_CLIENT_ID,
        client_secret=settings.SPOTIPY_CLIENT_SECRET,
        redirect_uri=settings.SPOTIPY_REDIRECT_URI,
        scope="user-library-read"
    )
    code = request.GET.get('code')
    token_info = sp_oauth.get_access_token(code)
    request.session['token_info'] = token_info
    return HttpResponseRedirect('/')

def get_artist_news(artist_name):
    """NewsAPIを使用してアーティストに関連するニュースを取得"""
    url = f"https://newsapi.org/v2/everything?q={artist_name}&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('articles', [])
    else:
        return None

def artist_news_view(request):
    """アーティスト名に関連するニュースを表示"""
    artist_name = request.GET.get('artist_name', '')
    news_data = []
    
    if artist_name:
        news_articles = get_artist_news(artist_name)
        
        if news_articles:
            for article in news_articles:
                news_data.append({
                    'title': article['title'],
                    'summary': article['description'],  # 記事の説明を使う
                    'url': article['url']
                })
        else:
            news_data = None
    return render(request, 'music_search/artist_news.html', {'news_data': news_data, 'artist_name': artist_name})
