from django.contrib.auth import views as auth_views
from django.urls import include, path

from .views import ChangePasswordView, CustomLoginView, SignUpView, profile

app_name = 'accounts'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('password_change/', ChangePasswordView.as_view(), name='password_change_form.html'),
    path('', include('django.contrib.auth.urls')),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', profile, name='profile'),
]
