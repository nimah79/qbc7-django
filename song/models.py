from django.contrib.auth.models import User
from django.db import models


class Artist(models.Model):
    name = models.CharField(max_length=255)
    about = models.TextField()
    birthdate = models.DateTimeField(null=True)


class Album(models.Model):
    name = models.CharField(max_length=255)


class Category(models.Model):
    name = models.CharField(max_length=255)


class Song(models.Model):
    album = models.ForeignKey(
        Album,
        null=True,
        on_delete=models.CASCADE,
        related_name='songs',
    )
    artists = models.ManyToManyField(Artist)
    categories = models.ManyToManyField(Category)
    name = models.CharField(max_length=255)
    duration = models.IntegerField()
    song_url = models.URLField(max_length=2048)
    cover_url = models.URLField(max_length=2048)
    lyrics = models.TextField(blank=True, null=True)


class Playlist(models.Model):
    user = models.ForeignKey(
        User,
        related_name='playlists',
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255)
    artists = models.ManyToManyField(Artist)
    songs = models.ManyToManyField(Song)
    albums = models.ManyToManyField(Album)
