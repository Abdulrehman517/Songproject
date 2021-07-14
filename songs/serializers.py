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
        fields = ['id', 'album_name', 'artist', 'tracks']

    def create(self, validated_data):
        tracks_data = validated_data.pop('tracks')
        album = Album.objects.create(**validated_data)
        for track_data in tracks_data:
            Track.objects.create(album=album, **track_data)
        return album
    #
    # def update(self, instance, validated_data):
    #     instance.album_name = validated_data.get('album_name', instance.album_name)
    #     instance.artist = validated_data.get('artist', instance.artist)
    #     instance.tracks.order = validated_data.get('order', instance.tracks.order)
    #     instance.tracks.title = validated_data.get('title', instance.tracks.title)
    #     instance.tracks.description = validated_data.get('description', instance.tracks.description)
    #
    #     instance.save()
    #     return instance

    def update(self, instance, validated_data):
        track_data_list = validated_data.pop('tracks')
        instance.album_name = validated_data.get('album_name', instance.album_name)
        instance.artist = validated_data.get('artist', instance.artist)
        instance.save()

        tracks_with_same_album_instance = Track.objects.filter(album=instance.pk).values_list('id', flat=True)
        tracks_id_pool = []
        for track in track_data_list:
            if "id" in track.keys():
                if Track.objects.filter(id=track['id'].exists()):
                    track_instance = Track.objects.get(id=track['id'])
                    track.order = track.get('order', track_instance.order)
                    track.title = track.get('title', track_instance.title)
                    track.description = track.get('description', track_instance.description)
                    track_instance.save()
                    tracks_id_pool.append(track_instance.id)
                else:
                    continue
            else:
                tracks_instance = Track.objects.create(album=instance, **track)
                tracks_id_pool.append(tracks_instance.id)

        for track_id in tracks_with_same_album_instance:
            if track_id not in tracks_id_pool:
                Track.objects.filter(pk=track_id).delete()

        return instance
