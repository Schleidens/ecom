from django.urls import path

from .views import user_creation_view, user_login_view, user_logout_view

urlpatterns = [
    path('register/', user_creation_view.as_view(), name='register'),
    path('login/', user_login_view.as_view(), name="login"),
    path('logout/', user_logout_view.as_view(), name="logout"),
]