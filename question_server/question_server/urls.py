from django.urls import path
from .views import question_function_1

urlpatterns = [
    path('api/question1/', question_function_1, name='question_function_1'),
]