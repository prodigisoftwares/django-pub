from django.urls import path

from .views import ArticleListView, IndexView

app_name = "core"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("articles/", ArticleListView.as_view(), name="articles"),
]
