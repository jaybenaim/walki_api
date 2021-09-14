from main_app.models import Pet
from main_app.serializers import GroupSerializer, PetSerializer, UserSerializer
from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
  """
  API - Users
  """
  queryset = User.objects.all().order_by('-date_joined')
  serializer_class = UserSerializer
  permission_classes = [permissions.IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
  """
  API - Groups
  """
  queryset = Group.objects.all().order_by('name')
  serializer_class = GroupSerializer
  permission_classes = [permissions.IsAuthenticated]

class PetViewSet(viewsets.ModelViewSet):
  """
  API - Pets
  """
  queryset = Pet.objects.all().order_by('name')
  serializer_class = PetSerializer
  permission_classes = [permissions.IsAuthenticated]


