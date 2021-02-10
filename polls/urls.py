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
    # Обновление конкретного опроса
    path('poll/update/<int:poll_id>/', PollUpdate.as_view(), name='poll_update'),
    # Удаление конкретного опроса
    path('poll/delete/<int:poll_id>/', PollDelete.as_view(), name='poll_delete'),
    # Просмотр всех опросов
    path('poll/view/', PollView.as_view(), name='polls_view'),
    # Отображение только активных опросов
    path('poll/view/active/', PollActiveView.as_view(), name='active_poll_view'),
    # Создание вопроса
    path('question/create/', QuestionCreate.as_view(), name='question_create'),
    # Обновление конкретного вопроса
    path('question/update/<int:question_id>/', QuestionUpdate.as_view(), name='question_update'),
    # Удаление конкретного вопроса
    path('question/delete/<int:question_id>/', QuestionDelete.as_view(), name='poll_delete'),
    # Создание варианта ответа
    path('choice/create/', ChoiceCreate.as_view(), name='choice_create'),

    path('choice/update/<int:choice_id>/', ChoiceCreate.as_view(), name='choice_update'),
]