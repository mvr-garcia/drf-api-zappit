from rest_framework import serializers
from posts.models import Post, Vote


class PostSerializer(serializers.ModelSerializer):
    # The 'poster' field contained the id, now will be replace by username
    poster = serializers.ReadOnlyField(source='poster.username')
    # Then the id will be shown on 'poster_id'
    poster_id = serializers.ReadOnlyField(source='poster.id')

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'url',
            'poster',
            'poster_id',
            'created'
        ]


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id']
