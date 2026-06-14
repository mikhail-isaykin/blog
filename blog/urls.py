from django.urls import path

from .views import PostListView, post_comment, post_detail, post_search, post_share

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', post_detail, name='post_detail'),
    path('<int:pk>/share/', post_share, name='post_share'),
    path('<int:pk>/comment/', post_comment, name='post_comment'),
    path('tag/<slug:tag_slug>/', PostListView.as_view(), name='post_list_by_tag'),
    path('search/', post_search, name='post_search'),
]
