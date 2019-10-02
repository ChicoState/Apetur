from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    cityID = models.IntegerField()
    stateID = models.IntegerField()
    countryID = models.IntegerField()
    def getFullName(self):
        return self.user.first_name + " " + self.user.last_name
    
    def getCity(self):
        if self.cityID == 1:
            return 'Chico'
        return '' 
    def getState(self):
        if self.stateID == 1:
            return 'CA'
        return ''  

    def getCountry(self):
        if self.countryID == 1:
            return 'US'
        return ''
    def getLocation(self):
        return self.getCity() + ', ' + self.getState()

    def getEmail(self):
        return self.user.email
        
    def __str__(self):
        return self.user.username



class Photographer(models.Model):
        client = models.OneToOneField(Client, on_delete = models.CASCADE)
        bio = models.CharField(max_length = 500)
        radius = models.PositiveIntegerField(default = 25)
        tags = models.TextField()

        def __str__(self):
            return self.client.user.username