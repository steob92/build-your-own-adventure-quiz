from django.urls import path
# from .views import question_function_1
from . import views


urlpatterns = [
    path('<str:question_name>/', views.question_detail, name='question_detail'),
    path('', views.view_all_questions, name='view_all_questions'),
]