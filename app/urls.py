from django.urls import path
from app.views import prompt_crud
urlpatterns = [
    path('prompt-crud/',prompt_crud,name='prompt-crud')
]
