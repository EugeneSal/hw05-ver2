from django.urls import path

from . import views

urlpatterns = [
    path('group_list/', views.group_list, name='group_list'),
    path('500/', views.page500, name='page500'),
    path('', views.index, name='index'),
    path('group/<slug:slug>/', views.group_posts, name='group'),
    path('new_group/', views.group_create, name='group_create'),

    path('edit/', views.edit, name='edit'),
    path('new/', views.new_post, name='new_post'),
    path('follow/', views.follow_index, name='follow_index'),
    path('<str:username>/', views.profile, name='profile'),
    path('<str:username>/<int:post_id>/', views.post_view, name='post'),
    path('<str:username>/<int:post_id>/edit/', views.post_edit,
         name='post_edit'),
    path('<str:username>/<int:post_id>/comment/', views.add_comment,
         name='add_comment'),
    path('<str:username>/follow/', views.profile_follow,
         name='profile_follow'),
    path('<str:username>/unfollow/', views.profile_unfollow,
         name='profile_unfollow'),
    path('<int:id>/comment_delete/', views.comment_delete,
         name='comment_delete'),
    path('<int:id>/post_delete/', views.post_delete,
         name='post_delete'),

]
