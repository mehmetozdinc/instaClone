from django.urls import include, path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('signin',views.signin,name='signin'),
    path('signout',views.signout,name='signout'),
    path('signup',views.signup,name='signup'),
    path('setting/<int:pk>',views.setting,name='setting'),
]
