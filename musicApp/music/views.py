from django.shortcuts import render,redirect,get_object_or_404
from .models import Recent,Song,Favourite,Playlist
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q 

# Create your views here.



def indexPaige(request):
    # display recent music

    if not request.user.is_anonymous:
        recent = list(Recent.objects.filter(user=request.user).values('song_id').order_by('-id'))
        recent_id = [each['song_id'] for each in recent][:5]
        recent_songs_unsorted = Song.objects.filter(id__in=recent_id,recent__user=request.user)
        recent_songs = list()

        for id in recent_id:
            recent_songs.append(recent_songs_unsorted.get(id=id))
    else:
        recent = None 
        recent_songs = None
    first_time = False

    #last played song

    if not request.user.is_anonymous:
            last_played_list = list(Recent.objects.filter(user=request.user).values('song_id').order_by('-id'))
            if last_played_list:
                last_played_id = last_played_list[0]['song_id']
                last_played_song =Song.objects.get(id=last_played_id)
            else:
                first_time =True
                last_played_song = Song.objects.get(id=2)
    else:
        first_time = True
        last_played_song = Song.objects.get(id=2)

#DISPLAY ALL THE SONGS
    songs = Song.objects.all()

# display songs on the home page
    songs_all = list(Song.objects.all().values('id').order_by('?'))
    slided_ids = [each['id'] for each in songs_all ][:5]
    indexpage_Songs = Song.objects.filter(id__in=slided_ids)

    # display Rap Songs 
    songs_Rap = list(Song.objects.filter(genre='Rap').values('id'))
    slided_ids = [each['id'] for each in songs_Rap][:5]
    indexpaige_Rap_songs = Song.objects.filter(id__in=slided_ids)

    # display Gospel Songs 
    songs_Gospel = list(Song.objects.filter(genre='Gospel').values('id'))
    slided_ids = [each['id'] for each in songs_Gospel][:5]
    indexpaige_Gospel_songs = Song.objects.filter(id__in=slided_ids)


    # display Rock Songs 


    songs_Rock = list(Song.objects.filter(genre='Rock').values('id'))
    slided_ids = [each['id'] for each in songs_Rap][:5]
    indexpaige_Rock_songs = Song.objects.filter(id__in=slided_ids)

    if len(request.GET)>0:
        search_query = request.GET.get('q')
        filtered_songs = songs.filter(Q(name__icontains=search_query)).distinct()
        context ={
            'allsongs':filtered_songs,'last_played':last_played_song,'query_search':True
        }
        return render(request,'music/index.html',context=context) 
    
    context ={
          'all_songs':indexpage_Songs,
          'recent_songs':recent_songs,
          'rap_songs':indexpaige_Rap_songs,
          'gospel_songs':indexpaige_Gospel_songs,
          'rock_songs':indexpaige_Rock_songs,
          'last_palyed':last_played_song,
          'first_time':first_time,
          'query_search':False
    }

    return render(request,'music/index.html',context=context) 


def gospel_song(request):
    gospel_songs  = Song.objects.filter(genre='Gospel')

    last_played_list = list(Recent.objects.values('song_id').order_by('-id'))
    if last_played_list:
        last_played_id = last_played_list[0]['song_id']
        last_played_song = Song.objects.get(id=last_played_id)
    else:
        last_played_id_song = Song.objects.get(id=2)
    
    query = request.GET.get('q')

    if query:
        gospel_songs = Song.objects.filter(Q(name__icontains=query)).distinct()
        context = {
            'gospel_songs':gospel_songs

        }
        return render(request,music/rap_songs.html,context=context)
    
    context ={ 'gospel_songs':gospel_songs,'last_played':last_played_id_song}

    return render(request,music/rap_songs.html,context=context)

def rock_song(request):
    rock_songs  = Song.objects.filter(genre='Rock')

    last_played_list = list(Recent.objects.values('song_id').order_by('-id'))
    if last_played_list:
        last_played_id = last_played_list[0]['song_id']
        last_played_song = Song.objects.get(id=last_played_id)
    else:
        last_played_id_song = Song.objects.get(id=2)
    
    query = request.GET.get('q')

    if query:
        rap_songs = Song.objects.filter(Q(name__icontains=query)).distinct()
        context = {
            'rock_songs':rock_songs

        }
        return render(request,music/rap_songs.html,context=context)
    
    context ={ 'rock_songs':rock_songs,'last_played':last_played_id_song}

    return render(request,music/rap_songs.html,context=context)

def rap_song(request):
    rap_songs  = Song.objects.filter(genre='Rap')

    last_played_list = list(Recent.objects.values('song_id').order_by('-id'))
    if last_played_list:
        last_played_id = last_played_list[0]['song_id']
        last_played_song = Song.objects.get(id=last_played_id)
    else:
        last_played_id_song = Song.objects.get(id=2)
    
    query = request.GET.get('q')

    if query:
        rap_songs = Song.objects.filter(Q(name__icontains=query)).distinct()
        context = {
            'rap_songs':rap_songs

        }
        return render(request,music/rap_songs.html,context=context)
    
    context ={ 'rap_songs':rap_songs,'last_played':last_played_id_song}

    return render(request,music/rap_songs.html,context=context)

@login_required(login_url='login')
def play_song(request,song_id):
    songs = Song.objects.filter(id=song_id).first()

    #add this data to the recent dataabase
    if list(Recent.objects.filter(song=songs,user=request.user).values()):
        data = Recent.objects.filter(song=songs,user=request.user)
        data.delete()
    data = Recent(song=songs,user=request.user)
    data.save()
    return redirect('all_songs')

@login_required(login_url='login')
def play_song_index(request,song_id):
    songs = Song.objects.filter(id=song_id).first()

    if list(Recent.objects.filter(song=songs,user=request.user).values()):
        data = Recent.objects.filter(song=songs,user=request.user)
        data.delete()
    data = Recent(song=songs,user=request.user)
    data.save()
    return redirect('index')


@login_required(login_url='login')
def play_recent_song(request,song_id):
    songs = Song.objects.filter(id=song_id).first()

    #add this data to the recent dataabase
    if list(Recent.objects.filter(song=songs,user=request.user).values()):
        data = Recent.objects.filter(song=songs,user=request.user)
        data.delete()
    data = Recent(song=songs,user=request.user)
    data.save()
    return redirect('recent')


def all_songs(request):
    songs = Song.objects.all()

    first_time = False

    if not request.user.is_anonymous:
        last_played_list = list(Recent.objects.filter(user=request.user).values('song_id').order_by(['-id']))
        if last_played_list:
            last_played_id =  last_played_list[0]['song_id']
            last_played_song = Song.objects.get(id=last_played_id)
    else:
        first_time= True
        last_played_song = Song.objects.get(id='2')
    
        ######## APPLYING THE SEARCH FILTERS
        qs_singers = Song.objects.values_list('singer').all()
        s_list =[s.split(',') for singer in qs_singers for s in singers]
        all_singers = sorted(list(set([s.strip() for singer in  s_list for s in singer])))

        qs_genres = Song.objects.values_list('genre').all()
        all_genres = sorted(list(set([l.strip() for genr in qs_genres for g in genr])))

        if len(request.GET)>0:
            search_query = request.GET.get('q')
            search_singer = request.GET.get('singers') or ""
            search_genre = request.GET.get('genres') or ''
            filtered_Songs =songs.filter(Q(name__icontains=search_query)).filter(Q(genre__icontains=search_genre)).filter(Q(singer__icontains=search_singer)).distinct()

            context = {
                'songs':filtered_Songs,
                'last_played':last_played_song,
                'all_singers':all_singers,
                'all_genres': all_genres,
                'query_search':True,
            }

            return render(request, 'music/all_songs.html',context)


        context = {
            'songs':filtered_Songs,
            'last_played':last_played_song,
            'first_time':first_time,
            'all_singers':all_singers,
            'all_genres': all_genres,
            'query_search':False,
        }
        return render(request, 'music/all_songs.html',context)


def recent(request):

    ### last played songs 
    last_played_list =  list(Recent.objects.values('song_id').order_by('-id'))

    if last_played_list:
        last_played_id = last_played_list[0]['song_id']
        last_played_song = Song.objects.get(id=last_played_id)
    else:
        last_played_song = Song.objects.get(id=2)

        ### Display the recent songs 
    recent = list(Recent.objects.filter(user=request.user).values('song_id').order_by(-id))
    if recent and not request.user.is_anonymous:
        recent_id = [each['song_id'] for each in recent]
        recent_songs_unsorted = Song.objects.filter(id__in=recent_id,recent__user=request.user)
        recent_songs = list()

        for id in recent_id:
            recent_songs.append(recent_songs_unsorted.get(id=id))
    else:
        recent_songs= None 

    
    if len(request.GET)>0:
        search_query = request.GET.get('q')
        filtered_songs = recent_songs_unsorted.filter(Q(name__icontains=search_query)).distinct()
        context = {
            'recent_songs':filtered_songs,'lastplayed':last_played_song, 'query_search':True

        }
        return render(request, 'music/recent.html',context)

    context = {
            'recent_songs':filtered_songs,'lastplayed':last_played_song, 'query_search':False

    }

    return render(request, 'music/recent.html',context)


@login_required(login_url='login')
def detail(request,song_id):
    song = Song.objects.filter(id=song_id).first()

    ## add data to the recent database

    if list(Recent.objects.filter(song=songs,user=request.user).values()):
        data = Recent.objects.filter(song=songs,user=request.user)
        data.delete()
    data = Recent(song=songs,user=request.user)
    data.save()


    # last played song 
    last_played_list = list(Recent.objects.values('song_id').order_by('-id'))
    if last_play_list:
        last_played_id = last_played_list[0]['song_id']
        last_played_song = Song.objects.get(id=last_played_id)
    else:
        last_played_song = Song.objects.get(id=2)
    
    playlists = Playlist.objects.filter(user=request.user).values('playlist_name').distinct()
    is_favourite = Favourite.objects.filter(user=request.user).filter(song=song_id).values('is_fav')


    if request.method =='POST':
        if 'playlist' in request.POST:
            playlist_name =  request.POST['playlist']
            q = Playlist(user=request.user,song=songs,playlist_name=playlist_name)
            q.save()
            messages.success(request,'Song added to playlist')
        elif 'add-fav' in request.POST:
            is_fav = True
            query = Favourite(user=request.user,song=songs,is_fav=is_fav)
            query.save()
            messages.success(request,'Added to favourite')
            return rediect('detail',song_id=song_id)
        elif 'rm-fav' in request.POST:
            is_fav = True
            query = Favourite.objects.filter(user=request.user,song=songs,is_fav=is_fav)
            query.delete()
            messages.success(request,'Removed from favourites')
            return redirec('detail',song_id=song_id)
    context ={ 'songs':songs,'playlists':playlists,'is_favourite':is_favourite, 'last_played_song':last_played_song}

    return render(request,'music/detail.html',context=context)





def mymusic(request):
    return render(request,'music/mymusic.html')


def playlist(request):
    playlists =Playlists.objects.filter(user=request.user).values('playlist_name').distinct
    context = {
        'playlists':playlists
    }
    return render(request,'music/playlist.html',context=context)


def playlist_songs(request,playlist_name):
    songs = Song.objects.filter(playlist__playlist_name=playlist_name,song__id = song_id,user=request.user).distinct()

    if request.method == "POST":
        song_id = list(request.POST.keys())[1]
        favourite_song = Favourite.objects.filter(user=request.user,song__id = song_id,is_fav=True)
        playlist_song.delete()
        messages.success(request,"Song Removed from playlist")

        context ={
            'playlist_name':playlist_name,
            'songs':songs
        }
    return render(request,'music/playlist_song.html',context=content)




def favourite(request):
    songs = Song.objects.filter(favourite_user=request.user,favourite__is_fav=True).distinct()
    
    if request.method == "POST":
        song_id = list(request.POST.keys())[1]
        favourite_song = Favourite.objects.filter(user=request.user,song__id = song_id,is_fav=True)
        favourite_song.delete()
        messages.success(request,"Removed from favourite")
    context ={
        'songs':songs

    }
    return render(request,'music/favourite.html',context=context)


