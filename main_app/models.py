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
    username = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.username

class Pet(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField()
    size = models.CharField(
        max_length=1,
        choices=SIZES,
        default=SIZES[2][0]
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDERS,
        default=GENDERS[0][0]
    )
    image = models.ImageField(blank=True, null=True, upload_to=make_unique_picture_filename)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Event(models.Model):
    name = models.CharField(max_length=50)
    time = models.CharField(max_length=50)
    date = models.DateField('Event date')
    description = models.TextField(max_length=250)
    location = models.CharField(max_length=150)
    attendees = models.ManyToManyField(Pet)
    lat = models.DecimalField('Latitude', max_digits=9, decimal_places=6)
    lng = models.DecimalField('Longitude', max_digits=9, decimal_places=6)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True, upload_to='images/')
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