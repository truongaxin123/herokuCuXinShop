from django.urls import path
from . import views

app_name = 'theblog'
urlpatterns = [
    path('detail_article/<str:slug>/', views.detail_article, name='detail_article'),
    path('detail_tag/<str:tag_name>/', views.detail_tag, name='detail_tag'),
    path('list_article/', views.list_article, name='list_article'),
    path('list_tag/', views.list_tag, name='list_tag'),
    path('list_article/with_tag/<str:tag_name>/', views.list_article_with_tag, name='list_article_with_tag'),
    path('joke/', views.joke, name='joke'),
    path('profile/', views.profile, name='profile'),
]
