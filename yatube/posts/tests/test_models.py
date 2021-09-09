from django.test import TestCase

from ..models import Group, Post, User


class PostsModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='testuser')
        cls.text = 'Тестовый текст больше 15 символов'
        cls.group = Group.objects.create(title='testgroup',
                                         slug='slug')
        cls.post = Post.objects.create(text=cls.text, author=cls.user,
                                       group=cls.group)

    def test_post_name_is_text_field(self):
        """В поле __str__  объекта Post записано первых 15 символов.............
        значение поля post.text"""
        expected_text = (f'текс поста: {self.text[:15]}, '
                         f'автор - {self.user.username}, '
                         f'группа поста - {self.group}, '
                         f'опубликован -  {self.post.pub_date.date()}')
        self.assertEqual(expected_text, str(self.post))

    def test_group_name_is_title_field(self):
        """В поле __str__  объекта Group записано значение поля group.title.....
        """
        expected_title = self.group.title
        self.assertEqual(expected_title, str(self.group))

    def test_sub_2_test_in_one(self):
        expect = {str(self.post): (f'текс поста: {self.text[:15]}, '
                                   f'автор - {self.user.username}, '
                                   f'группа поста - {self.group}, '
                                   f'опубликован -  '
                                   f'{self.post.pub_date.date()}'),
                  str(self.group): self.group.title}
        for key, value in expect.items():
            with self.subTest(value=value):
                self.assertEqual(key, value)
