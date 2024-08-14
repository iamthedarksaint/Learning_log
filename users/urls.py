from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
  # path('login/', views.login, name='login'),
  path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
  # path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
  path('logout/', views.logout_view, name='logout'),
  path('signup', views.signup, name='signup'),
]