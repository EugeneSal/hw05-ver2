from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q, F

User = get_user_model()


class Ip(models.Model):
    ip = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Айпишки'
        verbose_name = 'Афпишка'

    def __str__(self):
        return self.ip


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                verbose_name='Пользователь')
    date_of_birth = models.DateField(blank=True, null=True,
                                     verbose_name='дата рождения')
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True,
                              verbose_name='аватарка')
    city = models.CharField(max_length=20, verbose_name='Город',
                            blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Профайлы'
        verbose_name = 'Профайл'

    def __str__(self):
        return 'Profile for use {}'.format(self.user.username)


class Group(models.Model):
    title = models.CharField(verbose_name='Название группы', max_length=200)
    slug = models.SlugField(unique=True, default='', verbose_name='Слаг')
    description = models.TextField(verbose_name='Оприсание')

    class Meta:
        verbose_name_plural = 'Сообщества'
        verbose_name = 'Сообщество'
        ordering = ['title']

    def __str__(self) -> str:
        return self.title


class Image(models.Model):
    image = models.ImageField(upload_to='image/', blank=True, null=True,
                              verbose_name='картинка')


class Post(models.Model):
    text = models.TextField('')
    pub_date = models.DateTimeField('date published', auto_now_add=True,
                                    db_index=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='posts', verbose_name='автор')
    group = models.ForeignKey(Group, on_delete=models.SET_NULL,
                              related_name='posts',
                              blank=True, null=True, verbose_name='группа')
    image = models.ForeignKey(Image, blank=True, null=True,
                              on_delete=models.SET_NULL, related_name='posts')
    views = models.ManyToManyField(Ip, related_name='post_views', blank=True,
                                   verbose_name='просмотры')

    class Meta:
        ordering = ['-pub_date']
        verbose_name_plural = 'Посты'
        verbose_name = 'Пост'

    def __str__(self) -> str:
        return (f'текс поста: {self.text[:15]}, '
                f'автор - {self.author.username}, '
                f'группа поста - {self.group}, '
                f'опубликован -  {self.pub_date.date()}')

    def total_views(self):
        return self.views.count()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments',
                             verbose_name='пост')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='Автор',
                               related_name='comments')
    text = models.TextField('Текст', help_text='Текст нового комментария',
                            blank=False,)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    class Meta:
        ordering = ['-created']
        verbose_name = 'Коммент'
        verbose_name_plural = 'Комменты'


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower',
        verbose_name='Подписчик')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='following',
                               verbose_name='Автор')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(fields=('user', 'author'),
                                    name='unique_list'),
            models.CheckConstraint(
                check=~Q(user=F('author')), name='author'
            )
        ]
