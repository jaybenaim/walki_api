from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
import uuid


# Generate unique filename for images
def make_unique_picture_filename(instance, filename):
    return uuid.uuid4().hex[:6] + filename[filename.rfind('.'):]

GENDERS = (
    ('M', 'MALE'),
    ('F', 'FEMALE')
)

SIZES = (
    ('T', 'TINY'),
    ('S', 'SMALL'),
    ('M', 'MEDIUM'),
    ('L', 'LARGE'),
    ('X', 'EXTRA LARGE')
)

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=30, unique=True, blank=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    dob = models.DateField('Date of Birth', null=True)
    phone = models.CharField(max_length=20, blank=True)
    address1 = models.TextField(max_length=300, blank=True)
    address2 = models.TextField(max_length=300, blank=True)
    province = models.CharField(max_length=255, blank=True)
    postal = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)
    followers = models.ManyToManyField(User, blank=True,related_name="followers")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['first_name']

    def __str__(self):
        return self.display_name

class Pet(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    breed = models.CharField(max_length=100, blank=True)
    description = models.TextField(max_length=250, blank=True)
    age = models.IntegerField(blank=True, null=True)
    size = models.CharField(
        max_length=1,
        choices=SIZES,
        default=SIZES[2][0],
        blank=True
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDERS,
        default=GENDERS[0][0],
        blank=True
    )
    image = models.ImageField(blank=True, null=True, upload_to=make_unique_picture_filename)
    co_owners = models.ManyToManyField(User, related_name="co_owners", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Event(models.Model):
    name = models.CharField(max_length=50, unique=True)
    date = models.DateTimeField('Event date')
    description = models.TextField()
    location = models.CharField(max_length=150)
    lat = models.DecimalField('Latitude', max_digits=9, decimal_places=6)
    lng = models.DecimalField('Longitude', max_digits=9, decimal_places=6)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    attendees = models.ManyToManyField(Pet, blank=True)
    image = models.ImageField(blank=True, null=True, upload_to='images/')
    likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-date']

class Image(models.Model):
  url = models.TextField(max_length=250)

  def __str__(self):
    return self.name