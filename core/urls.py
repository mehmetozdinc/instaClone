from django.urls import include, path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('signin',views.signin,name='signin'),
    path('signout',views.signout,name='signout'),
    path('signup',views.signup,name='signup'),
    path('like/<str:pk>',views.like,name='like'),
    path('setting/<int:pk>',views.setting,name='setting'),
    path('profile/<str:pk>',views.profile,name='profile'),
]
