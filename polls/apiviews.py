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

class PollCreate(generics.CreateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PollSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            poll = serializer.save()
            return Response(PollSerializer(poll).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PollView(generics.ListAPIView):
    serializer_class = PollSerializer

    def get_queryset(self):
        queryset = Poll.objects.all()
        return queryset

class PollUpdate(generics.RetrieveUpdateAPIView):

    def update(self, request, poll_id, **kwargs):
        poll = get_object_or_404(Poll, pk=poll_id)
        if request.method == 'PATCH':
            serializer = PollSerializer(poll, data=request.data, partial=True)
            if serializer.is_valid():
                poll = serializer.save()
                return Response(PollSerializer(poll).data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
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