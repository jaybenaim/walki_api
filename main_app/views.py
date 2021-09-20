from django.http.response import  JsonResponse
from rest_framework.response import Response
from main_app.models import Event, Pet, Profile
from main_app.serializers import EventSerializer, GroupSerializer, PetSerializer, ProfileSerializer, UserSerializer
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
  permission_classes = [permissions.IsAuthenticatedOrReadOnly]


  def get_queryset(self):
    """Get the pets for 1 owner"""
    id = self.request.GET.get('owner')
    pets = Pet.objects.filter(Q(owner__id=id) | Q(co_owners__id=id))

    if id:
      return pets

    return Pet.objects.all()

  def create(self, request, *args, **kwargs):
    json_data = request.data

    # Search by list of user ids
    if 'search' in json_data.keys() and json_data['search'] == True:
      owners = json_data['owners']
      pets = Pet.objects.filter(Q(owner__id__in=owners) | Q(co_owners__id__in=owners))

      serializer = PetSerializer(pets, many=True, context={'request': request})
      return Response(serializer.data)

    # Regular create
    json_data['owner'] = User.objects.get(pk=json_data['owner'])
    new_pet = Pet(**json_data)
    new_pet.save()

    serializer = PetSerializer(new_pet, many=False, context={'request': request})
    return Response(serializer.data)
