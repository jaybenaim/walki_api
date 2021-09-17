from main_app.models import Event, Pet, Profile
from main_app.serializers import EventSerializer, GroupSerializer, PetSerializer, ProfileSerializer, UserSerializer
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

class ProfileViewSet(viewsets.ModelViewSet):
  """
  API - Profiles
  """
  queryset = Profile.objects.all().order_by('display_name')
  serializer_class = ProfileSerializer
  permission_classes = [permissions.IsAuthenticated]

class PetViewSet(viewsets.ModelViewSet):
  """
  API - Pets
  """
  queryset = Pet.objects.all().order_by('name')
  serializer_class = PetSerializer
  permission_classes = [permissions.IsAuthenticated]


class EventViewSet(viewsets.ModelViewSet):
  """
  API - Events
  """
  queryset = Event.objects.all().order_by('date')
  serializer_class = EventSerializer
  permission_classes = [permissions.IsAuthenticated]

