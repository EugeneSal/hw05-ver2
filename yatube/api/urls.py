from django.conf.urls import url
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework import routers

from .views import *

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet,
                basename='posts')
router.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet,
                basename='comments')
router.register(r'groups', GroupViewSet, basename='groups')
router.register(r'follow', FollowViewSet, basename='follow')

router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/jwt/', include('api.inner', namespace='api')),
    path('v1/', include(router.urls)),

]

schema_view = get_schema_view(
    openapi.Info(
        title="Post API",
        default_version='v1',
        description="Документация для приложения api проекта Hw05",
        # terms_of_service="URL страницы с пользовательским соглашением",
        contact=openapi.Contact(email="umbra-mortis@mail.ru"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    url(r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'),
]
