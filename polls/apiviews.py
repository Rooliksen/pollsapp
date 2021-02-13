from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import authentication, permissions

from .models import *
from .serializers import *

from rest_framework import status
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK

class UserCreate(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer

class LoginView(APIView):
    permission_classes = ()

    def post(self, request,):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            return Response({"token": user.auth_token.key})
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)

class PollView(generics.ListAPIView):
    serializer_class = PollSerializer

    def get_queryset(self):
        queryset = Poll.objects.all()
        return queryset

class PollCreate(generics.CreateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PollSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            poll = serializer.save()
            return Response(PollSerializer(poll).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PollUpdate(generics.RetrieveUpdateAPIView):

    def update(self, request, poll_id, **kwargs):
        poll = get_object_or_404(Poll, pk=poll_id)
        serializer = PollSerializer(poll, data=request.data, partial=True)
        if serializer.is_valid():
            poll = serializer.save()
            return Response(PollSerializer(poll).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PollDelete(generics.DestroyAPIView):

    def delete(self, request, poll_id, **kwargs):
        poll = get_object_or_404(Poll, pk=poll_id)
        poll.delete()
        return Response("Poll deleted", status=status.HTTP_204_NO_CONTENT)

class PollActiveView(generics.ListAPIView):
    serializer_class = PollSerializer

    def get_queryset(self):
        active_polls = Poll.objects.filter(end_date__gte=timezone.now()).filter(pub_date__lte=timezone.now())
        return active_polls

class QuestionCreate(generics.CreateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = QuestionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            question = serializer.save()
            return Response(QuestionSerializer(question).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QuestionUpdate(generics.RetrieveUpdateAPIView):

    def update(self, request, question_id, **kwargs):
        question = get_object_or_404(Question, pk=question_id)
        serializer = QuestionSerializer(question, data=request.data, partial=True)
        if serializer.is_valid():
            question = serializer.save()
            return Response(QuestionSerializer(question).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QuestionDelete(generics.DestroyAPIView):

    def delete(self, request, question_id, **kwargs):
        question = get_object_or_404(Question, pk=question_id)
        question.delete()
        return Response("Question deleted", status=status.HTTP_204_NO_CONTENT)

class ChoiceCreate(generics.CreateAPIView):
    serializer_class = ChoiceSerializer

    def post(self, request):
        serializer = ChoiceSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            choice = serializer.save()
            return Response(ChoiceSerializer(choice).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChoiceUpdate(generics.RetrieveUpdateAPIView):

    def update(self, request, choice_id, **kwargs):
        choice = get_object_or_404(Choice, pk=choice_id)
        serializer = ChoiceSerializer(choice, data=request.data, partial=True)
        if serializer.is_valid():
            choice = serializer.save()
            return Response(ChoiceSerializer(choice).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChoiceDelete(generics.DestroyAPIView):

    def delete(self, request, choice_id, **kwargs):
        choice = get_object_or_404(Choice, pk=choice_id)
        choice.delete()
        return Response("Choice deleted", status=status.HTTP_204_NO_CONTENT)

class AnswerCreate(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = AnswerSerializer(data=request.data, context={'request': request})
        if request.user.is_anonymous is True and serializer.is_valid():
            user = None
            answer = serializer.save()
            return Response(AnswerSerializer(answer).data, status=status.HTTP_201_CREATED)
        elif serializer.is_valid():
            answer = serializer.save(user=self.request.user)
            answer = serializer.save()
            return Response(AnswerSerializer(answer).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)