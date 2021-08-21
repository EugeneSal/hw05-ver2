from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from django.shortcuts import get_object_or_404
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated
)
from .permission import IsAuthorOrReadOnly
from .serializers import *
from posts.models import Post, Group, User


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comments


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    serializer_class = PostSerializer
    filterset_fields = ['author', 'group', 'pub_date']
    ordering_fields = ['author', 'pub_date', 'id']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    serializer_class = UserSerializer


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['=user__username', '=following__username']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.request.user.follower
