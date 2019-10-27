from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from math import pi as pi
from django.db import connection
from decimal import Decimal


class Address(models.Model):
    zip_code = models.TextField()
    country_sn = models.TextField()
    state_sn = models.TextField()
    city_sn = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    street_address = models.TextField(
    )  # street number and street name (ex: 123 Fake Street)
    street_address2 = models.TextField(
        null=True, blank=True)  # Apt/Blg number/etc CAN BE NULL

    def get_country(self):
        return self.country_sn

    def get_state(self):
        return self.state_sn

    def get_city(self):
        return self.city_sn

    def get_latitude(self):
        return self.latitude

    def get_longitude(self):
        return self.longitude

    def get_street_address(self):
        return self.street_address

    def get_zip_code(self):
        return self.zip_code

    def get_street_address_2(self):
        if (self.street_address2 == None):
            return ""
        return self.street_address2

    def __str__(self):
        return self.get_street_address() + " " + self.get_street_address_2() +\
            " " + self.get_city() + ", " + self.get_state() + ", " + self.get_country() + " " + self.get_zip_code()


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.OneToOneField(Address,
                                   on_delete=models.CASCADE,
                                   null=True)
    dob = models.DateField(null=False, blank=False)

    def get_city(self):
        if (self.address == None):
            return None
        return self.address.get_city()

    def get_state(self):
        if (self.address == None):
            return None
        return self.address.get_state()

    def get_country(self):
        if (self.address == None):
            return None
        return self.address.get_country()

    def get_street_address(self):
        if (self.address == None):
            return None
        return self.address.get_street_address()
    def get_full_address(self):
        if(self.address == None):
            return ""
        return self.address

    def get_full_name(self):
        return self.user.get_full_name()

    def get_email(self):
        return self.user.email

    def find_photographer_in_radius(self, radius):
        photographer_list = []
        lat = self.address.get_latitude() * Decimal(pi / 180)
        lng = self.address.get_longitude() * Decimal(pi / 180)
        data_dict = {
            'lat': lat,
            'lng': lng,
            'r': radius,
            'convert_radians': pi / 180
        }
        with connection.cursor() as cursor:
            cursor.execute('SELECT id FROM apeturProject_address WHERE acos(sin(%(lat)s) * \
                sin(latitude * %(convert_radians)s) + cos(%(lat)s) * cos(latitude * %(convert_radians)s) * \
                    cos(longitude * %(convert_radians)s - (%(lng)s))) * 6371 <= %(r)s',data_dict)
            row = cursor.fetchall()
        for address in row:
            current_address_id = address[0]
            if (current_address_id != self.address.id):
                photographer_list.append(Photographer.objects.all().filter(client__address__id=current_address_id))
        return photographer_list

    def __str__(self):
        return self.user.username


class Photographer(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE)
    bio = models.CharField(max_length=500)
    radius = models.PositiveIntegerField(default=25)
    tags = models.TextField()
    def get_address(self):
        return self.client.get_full_address()
    """ Test function """
    def get_tags(self):
        return ["Tag1","Tag2"]
    def get_full_name(self):
        return self.client.get_full_name()
    def get_bio(self):
        return self.bio
    def __str__(self):
        return self.client.user.username


""" Given a latitude, longitude, and radius (IN KM) we can find the surround addresses.
Using these addresses photographers can be found. """


def find_photographer_in_radius(input_lat, input_lng, radius):
    photographer_list = []
    #First convert lat and lng to radians
    lat = input_lat * Decimal(pi / 180)
    lng = input_lng * Decimal(pi / 180)
    data_dict = {
        'lat': lat,
        'lng': lng,
        'r': radius,
        'convert_radians': pi / 180
    }
    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT id FROM apeturProject_address WHERE acos(sin(%(lat)s) *\
             sin(latitude * %(convert_radians)s) + cos(%(lat)s) * cos(latitude *\
                 %(convert_radians)s) * cos(longitude * %(convert_radians)s - (%(lng)s))) * 6371 <= %(r)s',
            data_dict)
        row = cursor.fetchall()
    for current_address in row:
        current_address_id = current_address[0]
        query = Photographer.objects.all().filter(
            client__address__id=current_address_id).first()  # Query based on the addresds id
        if query != None:  #If a result exists (its possible the address belongs to a client, we do not want to return that)
            photographer_list.append(
                Photographer.objects.all().filter(
                    client__address__id=current_address_id).first()
            )  #will always be unique value since 1 to 1 relationship. we can just grab the first value
    return photographer_list