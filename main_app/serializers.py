from main_app.models import Event, Image, Pet, Profile
from django.contrib.auth.models import User, Group
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["id", "url", "username", "email", "groups"]
class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "url", "name"]

class ImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Image
        fields = ["id", "as_url", "as_file"]


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    avatar_url = ImageSerializer(many=False, read_only=True)
    class Meta:
        model = Profile
        fields = ["id", "user", "display_name", "avatar_url", "first_name", "last_name", "dob", "phone", "address1", "address2", "province", "postal", "country", "followers", "created_at", "updated_at"]

class PetSerializer(serializers.HyperlinkedModelSerializer):
    owner = UserSerializer(many=False, read_only=True)
    co_owners = UserSerializer(many=True, read_only=True)
    class Meta:
        model = Pet
        fields = ["id", "name", "owner", "breed", "description", "age", "size", "gender", "image", "co_owners", "created_at", "updated_at"]
class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"
