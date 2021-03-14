from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from posts.models import Post, Vote
from .serializers import PostSerializer, VoteSerializer


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # Allows only user authenticated to post through the API
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Runs immediately before create, sets the poster to the user that make the request.
    def perform_create(self, serializer):
        serializer.save(poster=self.request.user)


class VoteCreate(generics.CreateAPIView):
    serializer_class = VoteSerializer
    # Allows only user authenticated to access the API
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a current authenticated user
        and the post, to prepare to vote.
        """
        user = self.request.user
        post = Post.objects.get(id=self.kwargs['id'])
        return Vote.objects.filter(voter=user, post=post)

    # Runs immediately before create
    def perform_create(self, serializer):
        # A condition that verify if the user already vote
        if self.get_queryset().exists():
            # If True raise the exception and exit
            raise ValidationError('You have already voted for this post :)')

        serializer.save(voter=self.request.user, post=Post.objects.get(id=self.kwargs['id']))

# Aula 8 - API Auth
