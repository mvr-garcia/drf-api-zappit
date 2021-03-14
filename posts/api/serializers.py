from rest_framework import serializers
from posts.models import Post, Vote


class PostSerializer(serializers.ModelSerializer):
    # The 'poster' field contained the id, now will be replace by username
    poster = serializers.ReadOnlyField(source='poster.username')
    # Then the id will be shown on 'poster_id'
    poster_id = serializers.ReadOnlyField(source='poster.id')
    votes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'url',
            'poster',
            'poster_id',
            'created',
            'votes',
        ]

    def get_votes(self, post):
        """
        :param post: The post (attribute of Vote model) who will count the votes
        :return: Quantity of votes
        """
        return Vote.objects.filter(post=post).count()


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id']
