from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Group, Post, User, Follow


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Group


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ['post']


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username')
    publication_date = serializers.SerializerMethodField(source='pub_date')

    class Meta:
        exclude = ('pub_date',)
        model = Post

    def get_publication_date(self, obj):
        return obj.pub_date.date()


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.SlugRelatedField(slug_field='id',
                                         many=True, read_only=True)

    class Meta:
        fields = ('id', 'username', 'posts')
        model = User


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault())
    author = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all())

    class Meta:
        fields = ('user', 'author')
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'author'],
            )
        ]

    def validate_author(self, value):
        user = self.context['request'].user
        if user == value:
            raise serializers.ValidationError('На себя нельзя подписываться')
        return value
