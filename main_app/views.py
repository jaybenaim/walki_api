import json
from django.db.models.query_utils import Q
from django.http.response import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.generic.base import View
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.generics import UpdateAPIView
from rest_framework.views import APIView
from main_app.models import Event, Pet, Profile
from main_app.serializers import EventSerializer, GroupSerializer, PetSerializer, ProfileSerializer, UserSerializer
from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import status, viewsets, permissions
from django.core import serializers
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.views.decorators.http import require_http_methods
# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
  """
  API - Users
  """
  queryset = User.objects.all().order_by('-date_joined')
  serializer_class = UserSerializer
  permission_classes = [permissions.IsAuthenticated]

  def create(self, request, *args, **kwargs):
    """Create a user and profile in the django db and return the User"""
    # print(request.data)
    # is_login = request.data['is_login']
    email = request.data['email']
    # Get or Create the user
    user = User.objects.get_or_create(email=email)[0]

    # If no username exists on the user assign the email address
    if not user.username:
      user.username = email
      user.save()

    # Get or Create the profile
    new_profile = Profile.objects.get_or_create(user_id=user.id)[0]

    if not new_profile.display_name:
      new_profile.display_name = email
      new_profile.save()

    return JsonResponse({
      "id": user.id,
      "email": user.email,
      "username": user.username
    })

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
  queryset = Profile.objects.all()
  serializer_class = ProfileSerializer
  permission_classes = [permissions.IsAuthenticated]

  def get_queryset(self):
    """Get Profiles by user id"""
    query_param = self.request.query_params.get('user')

    print(query_param)
    if query_param:
      return Profile.objects.filter(user__id=query_param)
    else:
      return Profile.objects.all().order_by('-updated_at')[:20]


class EventViewSet(viewsets.ModelViewSet):
  """
  API - Events
  """
  queryset = Event.objects.all().order_by('date')
  serializer_class = EventSerializer
  permission_classes = [permissions.IsAuthenticated]

class PetViewSet(viewsets.ModelViewSet):
  """
  API - Pets
  """
  queryset = Pet.objects.all().order_by('name')
  serializer_class = PetSerializer
  permission_classes = [permissions.IsAuthenticated]


  def get_queryset(self):
    """Get the pets for 1 owner"""
    id = self.request.GET.get('owner')
    pets = Pet.objects.filter(Q(owner__id=id) | Q(co_owners__id=id))

    if id:
      return pets

    return Pet.objects.all()

  def create(self, request, *args, **kwargs):
    json_data = request.data
    if json_data['search'] == True:
      owners = json_data['owners']
      pets = Pet.objects.filter(Q(owner__id__in=owners) | Q(co_owners__id__in=owners))
      serializer_context = {
          'request': request,
      }
      serializer = PetSerializer(pets, many=True, context={'request': request})
      return Response(serializer.data)

# @require_http_methods(["GET", "POST"])
# @api_view(['GET', 'POST', 'DELETE'])
# class GetBulkPetsView(APIView):
#   queryset = Pet.objects.all().order_by('name')
#   serializer_class = PetSerializer
#   permission_classes = [permissions.IsAuthenticated]
#   # authentication_classes = [authentication.TokenAuthentication]
#   # permission_classes = (permissions.AllowAny,)

#   def get_queryset(self):
#     return Pet.objects.all()

#   def post(self):
#     if self.request.method == 'POST':
#       json_data = json.loads(self.request.body)
#       owners = json_data['owners']
#       return Pet.objects.filter(Q(owner__id__in=owners) | Q(co_owners__id__in=owners))

# @api_view(['GET', 'POST'])
# def GetBulkPetsView(request):
#     if request.method == 'POST':
#       json_data = json.loads(request.body)
#       owners = json_data['owners']
#       return json.dumps(Pet.objects.filter(Q(owner__id__in=owners) | Q(co_owners__id__in=owners)))

#     pets = []

#     for pet in Pet.objects.all():

#       serializer = PetSerializer(pet)
#       pets.append(serializer.data)

#     return JsonResponse({
#       "pets": pets
#     }, safe=False)
# class GetBulkPetsView(viewsets.ModelViewSet):
#   """
#   API - Pets
#   """
#   queryset = Pet.objects.all().order_by('name')
#   serializer_class = PetSerializer
#   permission_classes = [permissions.IsAuthenticated]


#   def get_queryset(self, request):
#     """Get the pets for 1 owner"""
#     id = self.request.GET.get('owner')
#     pets = Pet.objects.filter(Q(owner__id=id) | Q(co_owners__id=id))

#     if id:
#       return pets

#     return Pet.objects.all()