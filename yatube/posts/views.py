from http import HTTPStatus

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm, UserEditForm, PostForm, ProfileEditForm, \
    GroupForm, ImageForm
from .models import Comment, Follow, Group, Post, User, Profile, Ip, Image


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def index(request):
    post_list = Post.objects.select_related('group').all()
    paginator = Paginator(post_list, settings.PAGINATOR_COUNT)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'posts/index.html', {
        'page_obj': page, 'paginator': paginator})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    paginator = Paginator(post_list, settings.PAGINATOR_COUNT)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'posts/group.html', {
        'group': group, 'page_obj': page, 'paginator': paginator})


def group_list(request):
    group_lists = Group.objects.all()
    paginator = Paginator(group_lists, settings.PAGINATOR_COUNT)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'posts/group_list.html', {
        'group_list': group_lists, 'page': page, 'paginator': paginator})


@login_required
def group_create(request):
    form = GroupForm(request.POST or None)
    if request.method == 'GET' or not form.is_valid():
        return render(request, 'posts/new_group.html',
                      {'form': form})
    group = form.save(commit=False)
    group.save()
    return redirect('group_list')


def profile(request, username):
    author = get_object_or_404(User, username=username)
    try:
        profile_data = get_object_or_404(Profile, user=author)
    except Exception:
        profile_data = None
    post_list = author.posts.all()
    paginator = Paginator(post_list, settings.PAGINATOR_COUNT)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    following = request.user.is_authenticated and (
        Follow.objects.filter(user=request.user, author=author).exists())
    return render(request, 'posts/profile.html', {
        'author': author, 'following': following,
        'page_obj': page, 'paginator': paginator, 'profile': True,
        'data': profile_data})


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    try:
        profile_data = get_object_or_404(Profile, user=post.author)
    except Exception:
        profile_data = None
    ip = get_client_ip(request)
    if Ip.objects.filter(ip=ip).exists():
        # # print(dir(Ip.objects.filter(ip=ip)))
        # # print(Ip.objects.filter(ip=ip).values())
        # # print(Ip.objects.filter(ip=ip).values()[0])
        # # print(post.views.values()[0]['ip'])
        # # print(post.views)
        # # print(post.views.all())
        # # j = Post.objects.get(id=54)
        # for m in post.views.all():
        #     print(m.ip)

        post.views.add(Ip.objects.get(ip=ip))

    else:
        Ip.objects.create(ip=ip)
        post.views.add(Ip.objects.get(ip=ip))
    comments = post.comments.all()
    form = CommentForm()
    return render(request, 'posts/post_detail.html', {
        'author': post.author,
        'post': post,
        'form': form,
        'comments': comments,
        'data': profile_data})


@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    form_image = ImageForm(request.POST or None, files=request.FILES or None)
    if request.method == 'GET' or not (form.is_valid()
                                       and form_image.is_valid()):
        return render(request, 'posts/create.html',
                      {'form': form, 'form_image': form_image,
                       'mode': 'create'})
    post = form.save(commit=False)
    form_image.save()
    image_odj = Image.objects.last()
    post.image = image_odj
    post.author = request.user
    post.save()
    return redirect('profile', post.author)


@login_required
def post_edit(request, post_id):
    post_object = get_object_or_404(Post, id=post_id)
    if request.user != post_object.author:
        return redirect('post_detail', post_id=post_id)
    form = PostForm(request.POST or None, files=request.FILES or None,
                    instance=post_object)
    form_image = ImageForm(request.POST or None, files=request.FILES or None)
    if form.is_valid() and form_image.is_valid():
        form.save()
        form_image.save()
        return redirect('post_detail', post_id=post_id)
    return render(request, 'posts/create.html', {
        'form': form, 'form_image': form_image,
        'mode': 'edit', 'post': post_object})


def page404(request, exception=None):
    return render(request, 'misc/404.html', {'path': request.path},
                  status=HTTPStatus.NOT_FOUND)


def csrf_failure(request, reason=''):
    return render(request, 'misc/403.html')


def page500(request):
    return render(request, 'misc/500.html',
                  status=HTTPStatus.INTERNAL_SERVER_ERROR)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        return redirect('post_detail', post_id=post_id)
    return render(request, 'posts/comments.html', {
        'form': form,
        'post': post,
        'author': post.author,
        'comments': comments})


@login_required
def follow_index(request):
    post_list = Post.objects.filter(author__following__user=request.user)
    paginator = Paginator(post_list, settings.PAGINATOR_COUNT)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'posts/follow.html', {
        'page_obj': page, 'paginator': paginator})


@login_required
def profile_follow(request, username):
    follower = request.user
    following = get_object_or_404(User, username=username)
    if follower != following:
        Follow.objects.get_or_create(user=follower, author=following)
    return redirect('profile', username=username)


@login_required
def profile_unfollow(request, username):
    follower = request.user
    following = get_object_or_404(User, username=username)
    Follow.objects.filter(user=follower, author=following).delete()
    return redirect('profile', username=username)


@login_required
def comment_delete(request, id):
    comment = get_object_or_404(Comment, id=id)
    if request.user == comment.author or request.user == comment.post.author:
        comment.delete()
    return redirect('post_detail', post_id=comment.post.id)


@login_required
def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    if request.user == post.author:
        post.delete()
        return redirect('profile', username=request.user)


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(data=request.POST, instance=request.user)
        profile_form = ProfileEditForm(data=request.POST,
                                       instance=request.user.profile,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile', username=request.user.username)
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'posts/edit.html', {
        'user_form': user_form, 'profile_form': profile_form})


def image(request, id):
    print(id)
    # post = get_object_or_404(Post, id=id)
    image_obj = get_object_or_404(Image, id=id)
    print(image_obj)
    return render(request, 'posts/image.html', {
        'image': image_obj})
