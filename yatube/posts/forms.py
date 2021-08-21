from django import forms

from .models import Comment, Post, User, Profile, Group


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group', 'image')
        help_texts = {'text': 'Введите текст записи',
                      'group': 'Выберите группу',
                      'image': 'Загрузите изображение'}
        labels = {'text': 'Текст', 'group': 'Группа', 'image': 'изображение'}
        widgets = {'text': forms.Textarea()}


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('title', 'slug', 'description')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')
        help_texts = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Электронная почта',
            'username': 'Никнэйм - латинскими буквами'
        }


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo', 'city')
        help_texts = {
            'city': 'Ваш город',
            'date_of_birth': 'введите дату в формате: ДД.ММ.ГГГГ',
            'image': 'Аватарка'}
