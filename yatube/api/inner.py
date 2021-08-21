from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)
app_name = 'api'

urlpatterns = [

    path('create/', TokenObtainPairView.as_view(), name='jwt_create'),
    path('refresh/', TokenRefreshView.as_view(), name='jwt_refresh'),
    path('verify/', TokenVerifyView.as_view(), name='jwt_verify')
]
