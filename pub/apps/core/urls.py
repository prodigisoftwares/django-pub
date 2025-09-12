from django.urls import path

from .views import ArticleListView, ArticleView, IndexView

app_name = "core"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("article/<slug:slug>/", ArticleView.as_view(), name="article"),
    path("articles/", ArticleListView.as_view(), name="articles"),
]
