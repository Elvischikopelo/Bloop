from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Song(models.Model):

    GENRE = (
        ('Rock','Rock'),
        ('Gospel','Gospel'),
        ('Rap','Rap')
    )

    name =  models.CharField(max_length=30)
    albulm = models.CharField(max_length=30)
    genre = models.CharField(max_length=30,choices=GENRE,default='Rap')
    song_img = models.FileField()
    year = models.DateTimeField()
    singer = models.CharField(max_length=40)
    song_file = models.FileField()

    def __str__(self):
        return self.name 



class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    playlist_name = models.CharField(max_length=40)
    song= models.ForeignKey(Song,on_delete=models.CASCADE)


class Favourite(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    song = models.ForeignKey(Song,models.CASCADE)
    is_fav = models.BooleanField(default=False)

class Recent(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    song = models.ForeignKey(Song,on_delete=models.CASCADE)

