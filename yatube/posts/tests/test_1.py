import shutil
import tempfile

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from ..models import Group, Post, User

TEMP_MEDIA = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA)
class TaskCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create(username="AndreyG")
        cls.group = Group.objects.create(
            title="test_group",
            slug="test_slug",
        )
        cls.post = Post.objects.create(
            text="текст",
            author=cls.author,
        )

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TEMP_MEDIA, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.anonymous = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.author)

    def test_add_post(self):
        """Проверка что пост создан"""
        counter = Post.objects.count()
        small_gif = (
            b"\x47\x49\x46\x38\x39\x61\x02\x00"
            b"\x01\x00\x80\x00\x00\x00\x00\x00"
            b"\xFF\xFF\xFF\x21\xF9\x04\x00\x00"
            b"\x00\x00\x00\x2C\x00\x00\x00\x00"
            b"\x02\x00\x01\x00\x00\x02\x02\x0C"
            b"\x0A\x00\x3B"
        )
        uploaded = SimpleUploadedFile(
            name="small.gif", content=small_gif, content_type="image/gif"
        )
        form_data = {
            "text": "Тестовый текст",
            "group": self.group.id,
            "image": uploaded,
        }
        self.authorized_client.post(
            reverse("new_post"), data=form_data, follow=True
        )
        response = self.authorized_client.get(reverse("index"))
        self.assertTrue(
            Post.objects.filter(
                text="Тестовый текст",
                group=self.group,
                image="posts/small.gif",
            ).exists()
        )
        self.assertEqual(response.context["page"][0].text, "Тестовый текст")
        self.assertEqual(response.context["page"][0].author, self.author)
        self.assertEqual(response.context["page"][0].group, self.group)
        self.assertEqual(Post.objects.count(), counter + 1)
