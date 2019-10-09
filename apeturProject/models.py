from django.db import models
from django.contrib.auth.models import User

class Address(models.Model):
    country_sn = models.TextField()
    state_sn = models.TextField()
    city_sn = models.TextField()
    latitude = models.DecimalField(max_digits = 9, decimal_places = 6)
    longitude = models.DecimalField(max_digits = 9, decimal_places = 6)
    def __str__(self):
        return self.city_sn + ", " + self.state_sn + ", " + self.country_sn
    
class Client(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    address = models.ForeignKey(Address, on_delete = models.CASCADE, null = True)
    
    def getCity(self):
        return
        
    def getState(self):
        return

    def getCountry(self):
        return

    def getLocation(self): 
        return
        
    def get_email(self):
        return self.user.email
    def __str__(self):
        return self.user.username


class Photographer(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE)
    bio = models.CharField(max_length=500)
    radius = models.PositiveIntegerField(default=25)
    tags = models.TextField()
    def __str__(self):
        return self.client.user.username
