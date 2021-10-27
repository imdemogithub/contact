from django.db import models
from django.db.models.deletion import CASCADE

# Master Table
class Master(models.Model):
    Email = models.EmailField(unique=True)
    Password = models.CharField(max_length=12)
    IsActive = models.BooleanField(default=False)

    class Meta:
        db_table = 'master'

    def __str__(self):
        return self.Email

# User Profile
class UserProfile(models.Model):
    Master = models.ForeignKey(Master, on_delete=models.CASCADE)
    ProfileImage = models.FileField(default="default.png", upload_to="users/")
    FullName = models.CharField(max_length=50, default='')
    Mobile = models.CharField(max_length=10, default='', null=True)
    Country = models.CharField(max_length=25, default='', null=True)
    Pincode = models.CharField(max_length=6, default='', null=True)
    Address = models.TextField(max_length=100, default='', null=True)

    class Meta:
        db_table = 'userprofile'

    # def __str__(self):
    #     return self.Master.Email

# category choices
categories = (
    ('fm', 'Family'),
    ('bs', 'Business'),
    ('fr', 'Friends'),
)
countries = (
    ('in', 'India'),
    ('us', 'United States'),
    ('uk', 'United Kingdom'),
)

# Contact Model
class Contact(models.Model):
    UserProfile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    
    Category = models.CharField(max_length=10, choices=categories)
    
    ContactImage = models.FileField(default="default.png", upload_to="users/contact_images/")
    FullName = models.CharField(max_length=50, default='')
    Email = models.EmailField(unique=True, blank=True, null=True)
    Mobile = models.CharField(max_length=10, default='', null=True)
    Country = models.CharField(max_length=20, choices=countries)
    Pincode = models.CharField(max_length=6, default='', null=True)
    Address = models.TextField(max_length=100, default='', null=True)

    class Meta:
        db_table = "contact"