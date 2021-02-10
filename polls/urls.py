from django.urls import path
from .apiviews import *

app_name = 'polls'
urlpatterns = [
    # Регистрация пользователя
    path("users/", UserCreate.as_view(), name="user_create"),
    # Получение токена пользователем
    path("login/", LoginView.as_view(), name="login"),
    # Создание опроса
    path('poll/create/', PollCreate.as_view(), name='poll_create'),
    # Просмотр всех опросов
    path('poll/view/', PollView.as_view(), name='polls_view'),
    # Обновление определенного опроса
    path('poll/update/<int:poll_id>/', PollUpdate.as_view(), name='poll_update'),
    # Отображение всех активных опросов
    path('poll/view/active/', PollView.as_view(), name='active_poll_view'),
]