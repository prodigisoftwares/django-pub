from django.urls import path

from .views import test_ollama

app_name = "llm"

urlpatterns = [
    path("test-ollama/", test_ollama, name="test_ollama"),
]
