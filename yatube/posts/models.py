from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

User = get_user_model()

#
# class Like(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL,
#                              related_name='likes',
#                              on_delete=models.CASCADE)
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     object_id = models.PositiveIntegerField()
#     content_object = GenericForeignKey('content_type', 'object_id')


class Ip(models.Model):
    ip = models.CharField(max_length=100)

    def __str__(self):
        return self.ip


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)

    def __str__(self):
        return 'Profile for use {}'.format(self.user.username)


class Group(models.Model):
    title = models.CharField(verbose_name='Название группы', max_length=200)
    slug = models.SlugField(unique=True, default='')
    description = models.TextField()

    class Meta:
        verbose_name_plural = 'Название групп'

    def __str__(self) -> str:
        return self.title


class Post(models.Model):
    text = models.TextField('')
    pub_date = models.DateTimeField('date published', auto_now_add=True,
                                    db_index=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='posts')
    group = models.ForeignKey(Group, on_delete=models.SET_NULL,
                              related_name='posts',
                              blank=True, null=True)
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    views = models.ManyToManyField(Ip, related_name='post_views', blank=True)
    #likes = GenericRelation(Like)

    class Meta:
        ordering = ['-pub_date']
        verbose_name_plural = 'Посты'
        verbose_name = 'Пост'

    def __str__(self) -> str:
        return self.text[:15]

    def total_views(self):
        return self.views.count()
    #
    # @property
    # def total_likes(self):
    #     return self.likes.count()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='post_comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='Автор',
                               related_name='author_comment')
    text = models.TextField(blank=False, verbose_name='Текст комментария')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='following')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('user', 'author'),
                                    name='unique_list')
        ]
