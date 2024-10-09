from django.urls import path
from . import views

urlpatterns = [
    path('', views.top_page, name='top_page'),  # トップページ
    path('music_search/', views.get_recommendations, name='music_search'),  # 音楽検索ページ
    path('random_preview/', views.random_preview, name='random_preview'),  # ランダム再生ページ
    path('login/', views.login, name='login'),  # ログインページ
    path('callback/', views.callback, name='callback'),  # コールバックページ
    path('artist_news/', views.artist_news_view, name='artist_news'),  # アーティストニュースページの追加
]
