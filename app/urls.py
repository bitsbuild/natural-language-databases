from django.urls import path
from app.views import prompt
urlpatterns = [
    path('prompt/',prompt,name='prompt')
]
