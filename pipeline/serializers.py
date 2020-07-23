from rest_framework.validators import UniqueValidator
from rest_framework import serializers

from django.contrib.auth.models import User
from .models import Lead, Board, Pipeline

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required = True,
        validators = [UniqueValidator(queryset=User.objects.all())]
    )

    username = serializers.CharField(
        required = True,
        validators = [UniqueValidator(queryset=User.objects.all())] 
    )

    password = serializers.CharField(min_length = 8, write_only = True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']


class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = '__all__'


class CreateBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = '__all__'


class ViewBoardSerializer(serializers.ModelSerializer):
    leads = LeadSerializer(many=True)

    class Meta:
        model = Board
        fields = ['name', 'pipeline', 'leads', 'probabiltiy', 'rotting_in']


class CreatePipelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pipeline
        fields = ['name', 'deal_probability']

class ViewPipelineSerializer(serializers.ModelSerializer):
    boards = CreateBoardSerializer(many=True)

    class Meta:
        model = Pipeline
        fields = ['name', 'boards', 'deal_probability']