from rest_framework import generics, permissions, mixins
from rest_framework.exceptions import ValidationError, status
from rest_framework.response import Response
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


class PostRetrieveDestroy(generics.RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # Allows only user authenticated to post through the API
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Delete the post if the user is the owner
    def delete(self, request, *args, **kwargs):
        post = Post.objects.filter(pk=kwargs['pk'], poster=self.request.user)
        if post.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError('This isn\'t your post to delete, Bro!')


class VoteCreate(generics.CreateAPIView, mixins.DestroyModelMixin):
    serializer_class = VoteSerializer
    # Allows only user authenticated to access the Vote API
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a current authenticated user
        and the post, to prepare to vote.
        """
        user = self.request.user
        post = Post.objects.get(pk=self.kwargs['pk'])
        return Vote.objects.filter(voter=user, post=post)

    # Runs immediately before create
    def perform_create(self, serializer):
        # A condition that verify if the user already vote
        if self.get_queryset().exists():
            # If True raise the exception and exit
            raise ValidationError('You have already voted for this post :)')
        serializer.save(voter=self.request.user, post=Post.objects.get(pk=self.kwargs['pk']))

    # Delete the vote if the user had already voted
    def delete(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError('You never voted for this post..silly!')
