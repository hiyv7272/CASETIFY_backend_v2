from django.urls import path 
from .views import KakaologinView
from .views import UserViewSet

urlpatterns = [
    path('/signup', UserViewSet.as_view({
        'post': 'sign_up'
    })),
    path('/signin', UserViewSet.as_view({
        'post': 'sign_in'
    })),
    path('/myprofile', UserViewSet.as_view({
        'get': 'get_user_profile',
        'post': 'update_user_profile',
    })),
    path('/myshippinginfo', UserViewSet.as_view({
        'get': 'get_user_shippinginfo',
        'post': 'update_user_shippinginfo',
    })),
    path('/kakaologin', KakaologinView.as_view()),
]