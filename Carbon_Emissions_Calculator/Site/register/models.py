from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    
    houses = (
        ('Bari', 'Bari'),
        ('Ikhaya', 'Ikhaya'),
        ('Ruka', 'Ruka'),
        ('Meraki', 'Meraki'),
        ('Baile', 'Baile'),
        ('Hogan', 'Hogan'),
        ('Heimat', 'Heimat'),
        ('Bandele', 'Bandele'),
        ('Bayt', 'Bayt'),
        ('Efie', 'Efie'),
        ('Ohana', 'Ohana'),
        ('Other', 'Other'),
    )

    accounts = (
        ('Resident', 'Resident'),
        ('Operator', 'Operator'),
        ('Administrator', 'Administrator'),
    )

    house = models.CharField(max_length=50, choices=houses)
    account_type = models.CharField(max_length=20, choices=accounts)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def delete(self, *args, **kwargs):
        # Add your custom logic here to handle related records before deletion
        super(Profile, self).delete()