from rest_framework import serializers
from .models import Album, Track


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ['id', 'order', 'title', 'duration']


class AlbumSerializer(serializers.ModelSerializer):
    tracks = TrackSerializer(many=True)

    class Meta:
        model = Album
        fields = ['id','album_name', 'artist', 'tracks']

    def create(self, validated_data):
        tracks_data = validated_data.pop('tracks')
        album = Album.objects.create(**validated_data)
        for track_data in tracks_data:
            Track.objects.create(album=album, **track_data)
        return album

    def update(self, instance, validated_data):
        instance.album_name = validated_data.get('album_name', instance.album_name)
        instance.artist = validated_data.get('artist', instance.artist)
        instance.tracks.order = validated_data.get('order', instance.tracks.order)
        instance.tracks.title = validated_data.get('title', instance.tracks.title)
        instance.tracks.description = validated_data.get('description', instance.tracks.description)

        instance.save()
        return instance
