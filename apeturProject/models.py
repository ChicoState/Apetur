from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from math import pi as pi
import math
import simplejson as json
from django.db import connection
from decimal import Decimal


class Address(models.Model):
    zip_code = models.TextField(default='')
    country_sn = models.TextField(default='')
    state_sn = models.TextField(default='')
    city_sn = models.TextField(default='')
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    # street number and street name (ex: 123 Fake Street)
    street_address = models.TextField(default='')
    street_address2 = models.TextField(
        null=True, default='', blank=True)  # Apt/Blg number/etc CAN BE NULL

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
    profile_pic = models.TextField(null=True, default='', blank=True)

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
    bio = models.CharField(max_length=500, null=True)
    radius = models.PositiveIntegerField(default=25, null=True)
    tags = models.TextField(null=True)

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
    name = models.CharField(max_length=255, default='', unique=True)
    adult_content = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# store photographer taken/uploaded photos and videos
class Photographer_File(models.Model):
    photographer = models.ForeignKey(Photographer, on_delete=models.CASCADE)
    location = models.OneToOneField(Address, on_delete=models.CASCADE)
    event_type = models.OneToOneField(
        Event_Type, on_delete=models.DO_NOTHING, default='')
    path = models.CharField(max_length=500, default='')
    is_featured = models.BooleanField(default=False)
    in_gallery = models.BooleanField(default=False)
    upload_date = models.DateField(auto_now=True)
    likes = models.PositiveIntegerField()

    def __str__(self):
        return self.photographer.client.user.username


# enum table for file types used for File table, such as profile pci and profile banner
class File_Type(models.Model):
    type_name = models.CharField(max_length=255, default='', unique=True)

    def __str__(self):
        return self.type_name


# store all other file, such as profile pic and profile banner
class File(models.Model):
    file_type = models.ForeignKey(
        File_Type, on_delete=models.CASCADE, default=None)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, default=None)
    path = models.CharField(max_length=500, default='')

    def __str__(self):
        return self.client.user.username


class Schedule(models.Model):
    photographer_id = models.ForeignKey(Photographer,
                                        on_delete=models.CASCADE,
                                        null=True)
    date = models.DateField(null=False)
    time = models.TextField(null=False)  # JSON representation of time fields
    fully_booked = models.BooleanField(null=False)
    max_bookings = models.IntegerField(null=False)
    # Can be derived from the amount of events
    cur_num_of_bookings = models.IntegerField(default=0, null=False)
    is_confirmed = models.BooleanField(null=False)

    def get_photographer_id(self):
        return self.photographer_id

    def get_date(self):
        return self.date

    def get_time(self):
        return self.time

    def get_fully_booked(self):
        return self.fully_booked


class Event(models.Model):
    event_type = models.ForeignKey(
        Event_Type, on_delete=models.CASCADE, null=True)
    schedule_id = models.ForeignKey(
        Schedule, on_delete=models.CASCADE, null=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=False)
    start_time = models.TimeField(null=False)
    end_time = models.TimeField(null=False)
    confirmed = models.BooleanField(null=False)

    def __str__(self):
        return self.event_type.name

  #  def get_event_type(self):
   #     return self.event_type

    def get_photographer_id(self):
        return self.photographer_id

    def get_client_id(self):
        return self.client_id

    def get_client_name(self):
        return self.client.get_full_name()

    def get_start_time(self):
        return self.start_time

    def get_end_time(self):
        return self.end_time

    def is_confirmed(self):
        return self.confirmed


class Message(models.Model):
    sender = models.OneToOneField(User, on_delete=models.CASCADE)
    sent_data = models.DateTimeField
    message = models.TextField()


class Message_Group(models.Model):
    user_list = models.TextField()  # Comma seperated list of user ids
    # Comma seprated list of 1's/0's that are related to user_list by index
    active_list = models.TextField()


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
    return (photographer_list, json.dumps(json_data))


""" Given a photograpgers id (p_id), create an array containing data objects storing the data in YEAR-MONTH-DAY format
as well as the boolen determining whether or not that date is fully booked for the given photographer """


def retrieve_photographers_schedules(p_id):
    # Error checking. If p_id is False (meaning there was no p_id grabbed from GET) return empty string
    if p_id == False:
        return []
    json_data = []
    schedules = Schedule.objects.filter(
        photographer_id=p_id
    )  # this returns a list of schedule objects associated with the photograpger id
    for entry in schedules:
        data = {
            "date": str(entry.date)
        }
        json_data.append(data)
    return json.dumps(json_data)


def retrieve_photographers_events_and_schedule(p_id):
    events = {}  # Dictionary of lists
    schedule_map = {}
    json_schedule_data = []
    photographers_schedules = Schedule.objects.filter(
        photographer_id=p_id
    )  # Returns a list of schedules for a photographer by day
    for schedule in photographers_schedules:
        schedule_data = {
            "date": str(schedule.date),
            "num_bookings": 0,
            "max_bookings": schedule.max_bookings,
            "fully_booked": schedule.fully_booked
        }
        schedule_map[str(schedule.date)] = schedule_data
        json_schedule_data.append(schedule_data)
        day_list = []
        events_on_day = Event.objects.filter(
            schedule_id=schedule.id
        )
        for event in events_on_day:
            # Turn into "json-able" data to allow access in JS
            event_object = {
                "client_name": event.get_client_name(),
                "start_time": str(event.get_start_time()),
                "end_time": str(event.get_end_time()),
                "id": event.id,
                "confirmed": event.is_confirmed()
            }
            # Increment event counter for schedule data
            if(event.is_confirmed()):
                schedule_data["num_bookings"] = schedule_data["num_bookings"] + 1
            day_list.append(event_object)
        if day_list:  # If list is NOT empty
            events[str(schedule.date)] = day_list
    return (json.dumps(events), json.dumps(json_schedule_data))


def is_photographer(user_id):
    # Grab client object related to user_id
    # OneToOne relationship, just grab first result (it should only be one result)
    client = Client.objects.filter(user=user_id).first()
    # Check if there exists a photograper object related to that client
    # OneToOne relationship, just grab first result (it should only be one result)
    query_set = Photographer.objects.filter(client=client)

    if query_set:  # If not empty
        return True
    else:  # If empty
        return False


def get_photographer_id_from_user_id(user_id):
    client = Client.objects.filter(user=user_id).first()
    p_id = Photographer.objects.filter(client=client).first().id
    return p_id
