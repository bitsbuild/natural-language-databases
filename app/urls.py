from django.urls import path
from app.views import prompt_read
urlpatterns = [
    path('prompt-read/',prompt_read,name='prompt-read')
]
