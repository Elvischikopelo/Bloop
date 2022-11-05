from django.urls import path
from . import views
urlpatterns = [
    path('',views.indexPaige,name='index'),
    path('<int:song_id>/',views.detail,name='detail'),
    path('mymusic/',views.mymusic,name='mymusic'),
    path('playlist/',views.playlist,name='playlist'),
    path('playlist/<str:playlist_name>/',views.playlist_songs,name='playlistsongs'),
    path('favourite/',views.favourite,name='favourite'),
    path('recent/',views.recent,name='recent'),
    path('all_songs/',views.all_songs,name='all_songs'),
    path('play/<int:song_id>/',views.play_song,name='playsong'),
    path('play_song/<int:song_id>/',views.play_song_index,name='pay_song_index'),
    path('play_recent_song/<int:song_id>/',views.play_recent_song,name='play_recent_song')

]