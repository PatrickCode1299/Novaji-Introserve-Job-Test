from django.db import models
class RegisterUser(models.Model):  # Inherit from models.Model
    first_name = models.TextField()
    last_name = models.TextField()
    phone_number = models.CharField(max_length=11)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=8)
    date_of_birth = models.TextField()
