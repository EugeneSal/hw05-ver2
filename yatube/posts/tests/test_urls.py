from http import HTTPStatus

from django.core.cache import cache
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post, User, Profile


class PostsURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username='Testuser')
        # cls.author_profile = Profile.objects.create(user=cls.author)
        cls.not_author = User.objects.create_user(username='Notauthoruser')
        cls.post = Post.objects.create(
            author=cls.author, text='Тестовый текст')
        cls.group = Group.objects.create(title='testgroup', slug='test_slug',
                                         description='test descriptions')
        cls.templates_url_names = {
            'posts/index.html': '/',
            'posts/group.html': f'/group/{cls.group.slug}/',
            'posts/create.html': '/create/',
            'posts/profile.html': f'/profile/{cls.author.username}/',
            'posts/post_detail.html': f'/posts/{cls.post.id}/',
            'posts/comments.html': f'/posts/'
                                   f'{cls.post.id}/comment/'}

    def setUp(self):
        self.anonim_user = Client()

        self.authorized_user = Client()
        self.authorized_user.force_login(self.author)

        self.not_author_user = Client()
        self.not_author_user.force_login(self.not_author)

    def test_urls_anonim(self):
        """URL-адрес доступность для анонимного пользователя....................
        и проверка перенаправления"""
        for template, reverse_name in self.templates_url_names.items():
            with self.subTest(reverse_name=reverse_name):
                if reverse_name == reverse('post_create'):
                    response = self.anonim_user.get(reverse_name)
                    self.assertEqual(response.status_code, HTTPStatus.FOUND)
                    self.assertRedirects(response, '/auth/login/?next=/create/')
                elif reverse_name == reverse(
                        'add_comment', kwargs={'post_id': self.post.id}):
                    response = self.anonim_user.get(reverse_name)
                    self.assertEqual(response.status_code, HTTPStatus.FOUND)
                    self.assertRedirects(response,
                                         f'/auth/login/?next='
                                         f'/posts/'
                                         f'{self.post.id}/comment/')
                else:
                    response = self.anonim_user.get(reverse_name)
                    self.assertEqual(response.status_code, HTTPStatus.OK)
        response = self.anonim_user.get(f'/posts/'
                                        f'{self.post.id}/edit/')
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_urls_author(self):
        """URL-адрес доступен автору поста......................................
        """
        for template, reverse_name in self.templates_url_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_user.get(reverse_name)
                self.assertEqual(response.status_code, HTTPStatus.OK)
        response = self.authorized_user.get(
            f'/posts/{self.post.id}/edit/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_not_author(self):
        """URL-адрес доступен не автору поста...................................
        """
        for template, reverse_name in self.templates_url_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.not_author_user.get(reverse_name)
                self.assertEqual(response.status_code, HTTPStatus.OK)
        response = self.not_author_user.get(f'/posts/'
                                            f'{ self.post.id }/edit/')
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_pages_use_correct_template(self):
        """URL-адрес использует соответствующий шаблон..........................
        """
        cache.clear()
        for template, reverse_name in self.templates_url_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_user.get(reverse_name)
                self.assertTemplateUsed(response, template)
        response = self.authorized_user.get(
            f'/posts/{self.post.id}/edit/')
        self.assertTemplateUsed(response, 'posts/create.html')
