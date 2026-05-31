from django.urls import path
from django.views.generic import TemplateView
from blog import views


app_name = 'blog'

urlpatterns = [
    path(
        '',
        views.index,
        name='home'
    ),
    path(
        'about/',
        TemplateView.as_view(
            template_name='blog/about.html',
            extra_context={'site': 'mysite.com'}
        ),
        name='about'
    ),
    path(
        'contact/',
        views.contact,
        name='contact'
    ),
]
