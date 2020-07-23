from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate

from rest_framework.authtoken.models import Token
from .serializers import UserSerializer, LeadSerializer, CreateBoardSerializer, ViewBoardSerializer, CreatePipelineSerializer, ViewPipelineSerializer
from django.contrib.auth.models import User
from .models import Lead, Board, Pipeline
# Create your views here.

class UserCreate(APIView):
    """
    Creates a new user.
    """

    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = Token.objects.create(user=user)
                json = serializer.data
                json['token'] = token.key
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    """
    Logins a user.
    """

    def post(self, request, format='json'):
        user = authenticate(request, username=request.data.get('username'), password=request.data.get('password'))
        if user:
            token = Token.objects.get(user=user)
            json = {'token': token.key}
            return Response(json, status=status.HTTP_200_OK)
        return Response("Invalid credentials", status=status.HTTP_400_BAD_REQUEST)


class Pipelines(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format='json'):
        pipelines = Pipeline.objects.filter(user=request.user)
        serializer = ViewPipelineSerializer(pipelines, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format='json'):
        serializer = CreatePipelineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['user'] = request.user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ViewPipeline(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format='json'):
        try:
            pipeline = Pipeline.objects.get(id=request.GET.get('id'))
            serializer = ViewPipelineSerializer(pipeline)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response("Invalid pipeline id", status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format='json'):
        try:
            pipeline = Pipeline.objects.get(id=request.data.get('id'))
            pipeline.name = request.data.get('name', pipeline.name)
            pipeline.deal_probability = request.data.get('deal_probability', pipeline.deal_probability)
            pipeline.save()
            serializer = ViewPipelineSerializer(pipeline)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response("Invalid pipeline id", status=status.HTTP_400_BAD_REQUEST)


class Boards(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format='json'):
        pipeline = Pipeline.objects.get(id=request.GET.get('id'))
        if pipeline.user == request.user:
            boards = Board.objects.filter(pipeline=pipeline)
            serializer = ViewBoardSerializer(boards, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response("You are not authorized to access this pipeline", status=status.HTTP_401_UNAUTHORIZED)