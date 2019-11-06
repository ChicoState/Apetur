from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from math import pi as pi
import math
import simplejson as json
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
            " " + self.get_city() + ", " + self.get_state() + ", " + \
            self.get_country() + " " + self.get_zip_code()


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.OneToOneField(Address,
                                   on_delete=models.CASCADE,
                                   null=True)
    dob = models.DateField(null=False, blank=False)
    profile_pic = models.TextField(null=True, blank=True)

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
        if (self.address == None):
            return ""
        return self.address

    def get_full_name(self):
        return self.user.get_full_name()

    def get_email(self):
        return self.user.email

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
        return ["Tag1", "Tag2"]

    def get_full_name(self):
        return self.client.get_full_name()

    def get_bio(self):
        return self.bio

    def __str__(self):
        return self.client.user.username


class Event_Type(models.Model):
    name = models.CharField(max_length=255, unique=True)
    adult_content = models.BooleanField()

    def __str__(self):
        return self.name


class File(models.Model):
    photographer = models.ForeignKey(Photographer, on_delete=models.CASCADE)
    location = models.OneToOneField(Address, on_delete=models.CASCADE)
    path = models.CharField(max_length=500)
    is_featured = models.BooleanField()
    in_gallery = models.BooleanField()
    adult_content = models.BooleanField()
    upload_date = models.DateField(auto_now=True)
    likes = models.PositiveIntegerField(default=0)

class Schedule(models.Model):
    photographer_id = models.ForeignKey(Photographer, on_delete = models.CASCADE, null = True)
    date = models.DateField(null = False)
    time = models.TextField(null = False)
    fully_booked = models.BooleanField(null = False)
    
    def get_photographer_id(self):
        return self.photographer_id
    def get_date(self):
        return self.date
    def get_time(self):
        return self.time
    def get_fully_booked(self):
        return self.fully_booked


class Event(models.Model):
    event_type = models.TextField
    event_date = models.TextField   
    photographer_id = models.ForeignKey(Photographer, on_delete = models.CASCADE, null = True)
    client_id = models.ForeignKey(Client, on_delete = models.CASCADE, null = True)
    time = models.TextField

    def get_event_type(self):
        return self.event_type
    def get_event_date(self):
        return self.event_date
    def get_photographer_id(self):
        return self.photographer_id
    def get_client_id(self):
        return self.client_id
    def get_time(self):
        return self.time


""" Given a latitude, longitude, and radius (IN KM) we can find the surround addresses.
Using these addresses photographers can be found.
Return type is a tuple. The first element in the tuple will be a list of Photographer objects that were
found during the query. 
The second element in the tuple is a list of JSON serialized photographer data to alow for google map markers to be placed.
As of now it just contains latitude and longtitude, but may be changed the future.
 """


def find_photographer_in_radius(input_lat, input_lng, radius):
    MIN_LAT = math.radians(-90)
    MAX_LAT = math.radians(90)
    MIN_LNG = math.radians(-180)
    MAX_LNG = math.radians(180)

    photographer_list = []
    json_data = []
    radius_of_earth = 6371  # approximate in KM

    # First convert the input lat and lng to radians
    lat = input_lat * Decimal(math.pi / 180)
    lng = input_lng * Decimal(math.pi / 180)

    # Find lat_min & lat_max in order to optimize query (source: http://janmatuschek.de/LatitudeLongitudeBoundingCoordinates)
    r = Decimal(
        radius / radius_of_earth
    )  # angular radius of circle [this will also be used in the query]
    lat_min = lat - r
    lat_max = lat + r
    # Find lng_min & lng_max
    if lat_min > MIN_LAT and lat_max < MAX_LAT:
        lat_delta = Decimal(math.asin(math.sin(r) / math.cos(lat)))

        lng_min = lng - lat_delta
        if lng_min < MIN_LNG:
            lng_min += 2 * math.pi
        lng_max = lng + lat_delta
        if lng_max > MAX_LNG:
            lng_max -= 2 * math.pi
    else:
        lat_min = max(lat_min, MIN_LAT)
        lat_max = min(lat_max, MAX_LAT)
        lng_min = MIN_LNG
        lng_max = MAX_LNG

    data_dict = {
        'input_lat': lat,
        'input_lng': lng,
        'lat_min': lat_min,
        'lat_max': lat_max,
        'lng_min': lng_min,
        'lng_max': lng_max,
        'r': r,  # angular radius of the circle
        'rad_earth': radius_of_earth,
        'convert_radians': math.pi / 180
    }
    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT id FROM apeturProject_address WHERE\
                 (latitude * %(convert_radians)s >= %(lat_min)s AND latitude * %(convert_radians)s <= %(lat_max)s)\
                 AND (longitude * %(convert_radians)s >= %(lng_min)s AND longitude * %(convert_radians)s <= %(lng_max)s)\
            AND\
                acos(sin(%(input_lat)s) * sin(latitude * %(convert_radians)s) + cos(%(input_lat)s) * \
                    cos(latitude * %(convert_radians)s) * cos(longitude * %(convert_radians)s - (%(input_lng)s))) <= %(r)s',
            data_dict)
        row = cursor.fetchall()
    for current_address in row:
        current_address_id = current_address[0]
        query = Photographer.objects.all().filter(
            client__address__id=current_address_id).first(
        )  # Query based on the addresss id
        # If a result exists (its possible the address belongs to a client, we do not want to return that)
        if query != None:
            photographer_list.append(
                Photographer.objects.all().filter(
                    client__address__id=current_address_id).first()
            )  # will always be unique value since 1 to 1 relationship. we can just grab the first value

            # Now that we have the photographer object, we need to create the JSON data
            photographer_data = {
                "name": photographer_list[-1].get_full_name(),
                "lat": photographer_list[-1].client.address.get_latitude(),
                "lng": photographer_list[-1].client.address.get_longitude()
            }
            json_data.append(photographer_data)
    # print(json.dumps(json_data))
    return (photographer_list, json.dumps(json_data))


""" Given a photograpgers id (p_id), create an array containing data objects storing the data in YEAR-MONTH-DAY format
as well as the boolen determining whether or not that date is fully booked for the given photographer """
def retrieve_photographers_schedules(p_id):
    if p_id == False:  # Error checking. If p_id is False (meaning there was no p_id grabbed from GET) return empty string
        return []
    json_data = []
    schedules = Schedule.objects.filter(photographer_id=p_id)  # this returns a list of schedule objects associated with the photograpger id
    for entry in schedules:
        data = {
            "date": str(entry.date),
            "fully_booked" : entry.fully_booked
        }
        json_data.append(data)
    return json.dumps(json_data)
