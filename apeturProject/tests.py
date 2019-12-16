from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from .models import *
from decimal import Decimal
from datetime import *

class BasicTest(TestCase):

    # Address model testing
    def test_address(self):
        #create test address as Address
        address = Address(zip_code='93121',
        country_sn='USA',
        state_sn='CA',
        city_sn='Chico',
        latitude=Decimal(10),
        longitude=Decimal(20),
        street_address = 'testing 123 street')
        address.save()

        record = Address.objects.filter(id = address.id).first()
        self.assertEqual(record, address)

    def test_address_get_country(self):
        #create test address
        address = Address(zip_code='91323',
        country_sn='USA',
        city_sn='Fake city',
        state_sn = "CA",
        latitude=Decimal(30),
        longitude=Decimal(20),
        street_address = "fake street 123"
        )
        address.save()
        record = Address.objects.filter(id = address.id).first()
        self.assertEqual(record.get_country(), 'USA')
    def test_address_get_state(self):
        #create test address
        address = Address(zip_code='91323',
        country_sn='USA',
        city_sn='Fake city',
        state_sn = "OR",
        latitude=Decimal(10),
        longitude=Decimal(50),
        street_address = "extra fake street 123"
        )
        address.save()
        record = Address.objects.filter(id = address.id).first()
        self.assertEqual(record.get_state(), 'OR')

    def test_address_get_city(self):
        #create test address
        address = Address(zip_code='91323',
        country_sn='USA',
        city_sn='Fake city',
        state_sn = "OR",
        latitude=Decimal(10),
        longitude=Decimal(50),
        street_address = "extra fake street 123"
        )
        address.save()
        record = Address.objects.filter(id = address.id).first()
        self.assertEqual(record.get_city(), 'Fake city')

    def test_address_get_latitude(self):
        #create test address
        address = Address(zip_code='91323',
        country_sn='USA',
        city_sn='Fake city',
        latitude=Decimal(30),
        longitude=Decimal(20),
        street_address = "fake street 123"
        )
        address.save()
        record = Address.objects.filter(id = address.id).first()
        self.assertEqual(record.get_latitude(), Decimal(30))
    
    def test_address_get_longitude(self):
        #create test address
        address = Address(zip_code='91323',
        country_sn='USA',
        city_sn='Fake city',
        latitude=Decimal(30),
        longitude=Decimal(20),
        street_address = "fake street 123"
        )
        address.save()
        record = Address.objects.filter(id = address.id).first()
        self.assertEqual(record.get_longitude(), Decimal(20))
    
    def test_address_get_zip_code(self):
        #create test address
        address = Address(zip_code='91323',
        country_sn='USA',
        city_sn='Fake city',
        latitude=Decimal(30),
        longitude=Decimal(20),
        street_address = "fake street 123"
        )
        address.save()
        record = Address.objects.filter(id = address.id).first()
        self.assertEqual(record.get_zip_code(), '91323')
    
    def test_address_get_street_address_2(self):
        #create test address
        address = Address(zip_code='91323',
        country_sn='USA',
        city_sn='Fake city',
        latitude=Decimal(30),
        longitude=Decimal(20),
        street_address="fake street 123",
        street_address2 = "Apt 2"
        )
        address.save()
        record = Address.objects.filter(id = address.id).first()
        self.assertEqual(record.get_street_address_2(), 'Apt 2')
    
    def test_address_to_string(self):
        #create test address
        address = Address(zip_code='91323',
        country_sn='USA',
        city_sn='Fake city',
        latitude=Decimal(30),
        longitude=Decimal(20),
        street_address="fake street 123",
        street_address2 = "Apt 2"
        )
        address.save()
        stringify = address.get_street_address() + " " + address.get_street_address_2() +\
            " " + address.get_city() + ", " + address.get_state() + ", " + \
            address.get_country() + " " + address.get_zip_code()
        record = Address.objects.filter(id = address.id).first()
        self.assertEqual(str(record), stringify)


    
##################Client model testing###############################
    def test_client_get_city_with_address(self):
        address = Address(zip_code='91323',
        country_sn='USA',
        city_sn='Fake city',
        latitude=Decimal(30),
        longitude=Decimal(20),
        street_address="fake street 123",
        street_address2 = "Apt 2"
        )
        address.save()
        user=User.objects.create_user('username', password='userpassword')
        user.is_superuser = False
        user.is_staff = False
        user.save()
        client = Client(
            user=user,
            address = address,
            dob=datetime.now(),
            profile_pic=""
        )
        #create client
        client.save()
        record = Client.objects.filter(id=client.id).first()
        
        self.assertEqual(record.get_city(), "Fake city")

    def test_client_get_city_without_address(self):
        user=User.objects.create_user('username', password='userpassword')
        user.is_superuser = False
        user.is_staff = False
        user.save()
        client = Client(
            user=user,
            dob=datetime.now(),
            profile_pic=""
        )
        #create client
        client.save()
        record = Client.objects.filter(id=client.id).first()
        
        self.assertEqual(record.get_city(), None)

    def test_client_get_state_with_address(self):
        address = Address(zip_code='91323',
        country_sn='USA',
        state_sn = 'CA',
        city_sn='Fake city',
        latitude=Decimal(30),
        longitude=Decimal(20),
        street_address="fake street 123",
        street_address2 = "Apt 2"
        )
        address.save()
        user=User.objects.create_user('username', password='userpassword')
        user.is_superuser = False
        user.is_staff = False
        user.save()
        client = Client(
            user=user,
            address = address,
            dob=datetime.now(),
            profile_pic=""
        )
        #create client
        client.save()
        record = Client.objects.filter(id=client.id).first()
        
        self.assertEqual(record.get_state(), "CA")

    def test_client_get_state_without_address(self):
        user=User.objects.create_user('username', password='userpassword')
        user.is_superuser = False
        user.is_staff = False
        user.save()
        client = Client(
            user=user,
            dob=datetime.now(),
            profile_pic=""
        )
        #create client
        client.save()
        record = Client.objects.filter(id=client.id).first()
        
        self.assertEqual(record.get_state(), None)
        
    def test_client_get_country_with_address(self):
        address = Address(zip_code='91323',
        country_sn='USA',
        state_sn = 'CA',
        city_sn='Fake city',
        latitude=Decimal(30),
        longitude=Decimal(20),
        street_address="fake street 123",
        street_address2 = "Apt 2"
        )
        address.save()
        user=User.objects.create_user('username', password='userpassword')
        user.is_superuser = False
        user.is_staff = False
        user.save()
        client = Client(
            user=user,
            address = address,
            dob=datetime.now(),
            profile_pic=""
        )
        #create client
        client.save()
        record = Client.objects.filter(id=client.id).first()
        
        self.assertEqual(record.get_country(), "USA")

    def test_client_get_country_without_address(self):
        user=User.objects.create_user('username', password='userpassword')
        user.is_superuser = False
        user.is_staff = False
        user.save()
        client = Client(
            user=user,
            dob=datetime.now(),
            profile_pic=""
        )
        #create client
        client.save()
        record = Client.objects.filter(id=client.id).first()
        
        self.assertEqual(record.get_country(), None)

    def test_client_get_street_address_with_address(self):
        address = Address(zip_code='91323',
        country_sn='USA',
        state_sn = 'CA',
        city_sn='Fake city',
        latitude=Decimal(30),
        longitude=Decimal(20),
        street_address="fake street 123",
        street_address2 = "Apt 2"
        )
        address.save()
        user=User.objects.create_user('username', password='userpassword')
        user.is_superuser = False
        user.is_staff = False
        user.save()
        client = Client(
            user=user,
            address = address,
            dob=datetime.now(),
            profile_pic=""
        )
        #create client
        client.save()
        record = Client.objects.filter(id=client.id).first()
        
        self.assertEqual(record.get_street_address(), "fake street 123")

    def test_client_get_street_address_without_address(self):
        user=User.objects.create_user('username', password='userpassword')
        user.is_superuser = False
        user.is_staff = False
        user.save()
        client = Client(
            user=user,
            dob=datetime.now(),
            profile_pic=""
        )
        #create client
        client.save()
        record = Client.objects.filter(id=client.id).first()
        
        self.assertEqual(record.get_street_address(), None)
    

    def test_client_get_full_address_with_address(self):
        address = Address(zip_code='91323',
        country_sn='USA',
        state_sn = 'CA',
        city_sn='Fake city',
        latitude=Decimal(30),
        longitude=Decimal(20),
        street_address="fake street 123",
        street_address2 = "Apt 2"
        )
        address.save()
        user=User.objects.create_user('username', password='userpassword')
        user.is_superuser = False
        user.is_staff = False
        user.save()
        client = Client(
            user=user,
            address = address,
            dob=datetime.now(),
            profile_pic=""
        )
        #create client
        client.save()
        record = Client.objects.filter(id=client.id).first()
        
        self.assertEqual(record.get_full_address(), address)

    def test_client_get_full_address_without_address(self):
        user=User.objects.create_user('username', password='userpassword')
        user.is_superuser = False
        user.is_staff = False
        user.save()
        client = Client(
            user=user,
            dob=datetime.now(),
            profile_pic=""
        )
        #create client
        client.save()
        record = Client.objects.filter(id=client.id).first()
        
        self.assertEqual(record.get_full_address(), "")
    
    def test_client_get_full_address_with_address(self):
        address = Address(zip_code='91323',
        country_sn='USA',
        state_sn = 'CA',
        city_sn='Fake city',
        latitude=Decimal(30),
        longitude=Decimal(20),
        street_address="fake street 123",
        street_address2 = "Apt 2"
        )
        address.save()
        user=User.objects.create_user('username', password='userpassword')
        user.is_superuser = False
        user.is_staff = False
        user.save()
        client = Client(
            user=user,
            address = address,
            dob=datetime.now(),
            profile_pic=""
        )
        #create client
        client.save()
        record = Client.objects.filter(id=client.id).first()
        
        self.assertEqual(record.get_full_address(), address)

    def test_client_get_full_name(self):
        user=User.objects.create_user('username', password='userpassword')
        user.is_superuser = False
        user.is_staff = False
        user.save()
        client = Client(
            user=user,
            dob=datetime.now(),
            profile_pic=""
        )
        #create client
        client.save()
        record = Client.objects.filter(id=client.id).first()
        
        self.assertEqual(record.get_full_name(), user.get_full_name())

    def test_client_get_email(self):
        user=User.objects.create_user('username', password='userpassword')
        user.is_superuser = False
        user.is_staff = False
        user.save()
        client = Client(
            user=user,
            dob=datetime.now(),
            profile_pic=""
        )
        #create client
        client.save()
        record = Client.objects.filter(id=client.id).first()
        
        self.assertEqual(record.get_email(), user.email)
    
    def test_client_to_string(self):
        user=User.objects.create_user('username', password='userpassword')
        user.is_superuser = False
        user.is_staff = False
        user.save()
        client = Client(
            user=user,
            dob=datetime.now(),
            profile_pic=""
        )
        #create client
        client.save()
        record = Client.objects.filter(id=client.id).first()
        
        self.assertEqual(str(record), user.username)


######################### Photographer model testing ########################

    def test_photographer_get_client_id(self):
        address = Address(zip_code='91323',
        country_sn='USA',
        state_sn = 'CA',
        city_sn='Fake city',
        latitude=Decimal(30),
        longitude=Decimal(20),
        street_address="fake street 123",
        street_address2 = "Apt 2"
        )
        address.save()
        user=User.objects.create_user('username', password='userpassword')
        user.is_superuser = False
        user.is_staff = False
        user.save()
        client = Client(
            user=user,
            address = address,
            dob=datetime.now(),
            profile_pic=""
        )
        #create client
        client.save()

        p = Photographer(
            client=client,
            bio="Hello test",
            radius=25,
            tags = ""
        )
        p.save()

        record = Photographer.objects.filter(id=p.id).first()
        self.assertEqual(record.get_client_id(), client.id)

    def test_photographer_get_address(self):
        address = Address(zip_code='91323',
        country_sn='USA',
        state_sn = 'CA',
        city_sn='Fake city',
        latitude=Decimal(30),
        longitude=Decimal(20),
        street_address="fake street 123",
        street_address2 = "Apt 2"
        )
        address.save()
        user=User.objects.create_user('username', password='userpassword')
        user.is_superuser = False
        user.is_staff = False
        user.save()
        client = Client(
            user=user,
            address = address,
            dob=datetime.now(),
            profile_pic=""
        )
        #create client
        client.save()

        p = Photographer(
            client=client,
            bio="Hello test",
            radius=25,
            tags = ""
        )
        p.save()

        record = Photographer.objects.filter(id=p.id).first()
        self.assertEqual(record.get_address(), address)
    
    def test_photographer_get_tags(self):
        address = Address(zip_code='91323',
        country_sn='USA',
        state_sn = 'CA',
        city_sn='Fake city',
        latitude=Decimal(30),
        longitude=Decimal(20),
        street_address="fake street 123",
        street_address2 = "Apt 2"
        )
        address.save()
        user=User.objects.create_user('username', password='userpassword')
        user.is_superuser = False
        user.is_staff = False
        user.save()
        client = Client(
            user=user,
            address = address,
            dob=datetime.now(),
            profile_pic=""
        )
        #create client
        client.save()

        p = Photographer(
            client=client,
            bio="Hello test",
            radius=25,
            tags = ""
        )
        p.save()

        record = Photographer.objects.filter(id=p.id).first()
        self.assertEqual(record.get_tags(), ["Tag1", "Tag2"])

    def test_photographer_get_full_name(self):
        address = Address(zip_code='91323',
        country_sn='USA',
        state_sn = 'CA',
        city_sn='Fake city',
        latitude=Decimal(30),
        longitude=Decimal(20),
        street_address="fake street 123",
        street_address2 = "Apt 2"
        )
        address.save()
        user=User.objects.create_user('username', password='userpassword')
        user.is_superuser = False
        user.is_staff = False
        user.save()
        client = Client(
            user=user,
            address = address,
            dob=datetime.now(),
            profile_pic=""
        )
        #create client
        client.save()

        p = Photographer(
            client=client,
            bio="Hello test",
            radius=25,
            tags = ""
        )
        p.save()

        record = Photographer.objects.filter(id=p.id).first()
        self.assertEqual(record.get_full_name(), client.get_full_name())

    def test_photographer_get_bio(self):
        address = Address(zip_code='91323',
        country_sn='USA',
        state_sn = 'CA',
        city_sn='Fake city',
        latitude=Decimal(30),
        longitude=Decimal(20),
        street_address="fake street 123",
        street_address2 = "Apt 2"
        )
        address.save()
        user=User.objects.create_user('username', password='userpassword')
        user.is_superuser = False
        user.is_staff = False
        user.save()
        client = Client(
            user=user,
            address = address,
            dob=datetime.now(),
            profile_pic=""
        )
        #create client
        client.save()

        p = Photographer(
            client=client,
            bio="Hello test",
            radius=25,
            tags = ""
        )
        p.save()

        record = Photographer.objects.filter(id=p.id).first()
        self.assertEqual(record.get_bio(), "Hello test")

    def test_photographer_get_radius(self):
        address = Address(zip_code='91323',
        country_sn='USA',
        state_sn = 'CA',
        city_sn='Fake city',
        latitude=Decimal(30),
        longitude=Decimal(20),
        street_address="fake street 123",
        street_address2 = "Apt 2"
        )
        address.save()
        user=User.objects.create_user('username', password='userpassword')
        user.is_superuser = False
        user.is_staff = False
        user.save()
        client = Client(
            user=user,
            address = address,
            dob=datetime.now(),
            profile_pic=""
        )
        #create client
        client.save()

        p = Photographer(
            client=client,
            bio="Hello test",
            radius=25,
            tags = ""
        )
        p.save()

        record = Photographer.objects.filter(id=p.id).first()
        self.assertEqual(record.get_radius(), 25)
    
    def test_photographer_to_string(self):
        address = Address(zip_code='91323',
        country_sn='USA',
        state_sn = 'CA',
        city_sn='Fake city',
        latitude=Decimal(30),
        longitude=Decimal(20),
        street_address="fake street 123",
        street_address2 = "Apt 2"
        )
        address.save()
        user=User.objects.create_user('username', password='userpassword')
        user.is_superuser = False
        user.is_staff = False
        user.save()
        client = Client(
            user=user,
            address = address,
            dob=datetime.now(),
            profile_pic=""
        )
        #create client
        client.save()

        p = Photographer(
            client=client,
            bio="Hello test",
            radius=25,
            tags = ""
        )
        p.save()

        record = Photographer.objects.filter(id=p.id).first()
        self.assertEqual(str(record), user.username)

####### Event_Type model testing #########
    def test_event_type(self):
        e = Event_Type(name="Test",
        adult_content = False
        )

        e.save()
        record = Event_Type.objects.filter(id=e.id).first()
        self.assertEqual(record, e)
    
    def test_event_type_to_string(self):
        e = Event_Type(name="Test",
        adult_content = False
        )

        e.save()
        record = Event_Type.objects.filter(id=e.id).first()
        self.assertEqual(str(record), "Test")
    
####### Photographer file model testing #######

   
############### File_Type model test ####################


############## Non model testing #########################

############## Retrive photograpers schedule ###############
    def test_retrieve_photographers_schedule_empty(self):
        address = Address(zip_code='91323',
        country_sn='USA',
        state_sn = 'CA',
        city_sn='Fake city',
        latitude=Decimal(30),
        longitude=Decimal(20),
        street_address="fake street 123",
        street_address2 = "Apt 2"
        )
        address.save()
        user=User.objects.create_user('username', password='userpassword')
        user.is_superuser = False
        user.is_staff = False
        user.save()
        client = Client(
            user=user,
            address = address,
            dob=datetime.now(),
            profile_pic=""
        )
        #create client
        client.save()

        p = Photographer(
            client=client,
            bio="Hello test",
            radius=25,
            tags = ""
        )
        p.save()

        record = Photographer.objects.filter(id=p.id).first()
        
        self.assertEqual(retrieve_photographers_schedules(record.id), "[]")

    def test_retrieve_photographers_schedule_results(self):
        address = Address(zip_code='91323',
        country_sn='USA',
        state_sn = 'CA',
        city_sn='Fake city',
        latitude=Decimal(30),
        longitude=Decimal(20),
        street_address="fake street 123",
        street_address2 = "Apt 2"
        )
        address.save()
        user=User.objects.create_user('username', password='userpassword')
        user.is_superuser = False
        user.is_staff = False
        user.save()
        client = Client(
            user=user,
            address = address,
            dob=datetime.now(),
            profile_pic=""
        )
        #create client
        client.save()

        p = Photographer(
            client=client,
            bio="Hello test",
            radius=25,
            tags = ""
        )
        p.save()

        # create schedule

        s = Schedule(
            photographer_id=p,
            date=datetime.now(),
            time="[]",
            fully_booked=False,
            max_bookings=3,
            cur_num_of_bookings=0,
            is_confirmed = False
        )

        s.save()
        record = Schedule.objects.filter(photographer_id = p.id).first()
        self.assertEqual(retrieve_photographers_schedules(p.id), json.dumps([{"date" : str(record.date)}]))

    def test_is_photographer_true(self):
        address = Address(zip_code='91323',
        country_sn='USA',
        state_sn = 'CA',
        city_sn='Fake city',
        latitude=Decimal(30),
        longitude=Decimal(20),
        street_address="fake street 123",
        street_address2 = "Apt 2"
        )
        address.save()
        user=User.objects.create_user('username', password='userpassword')
        user.is_superuser = False
        user.is_staff = False
        user.save()
        client = Client(
            user=user,
            address = address,
            dob=datetime.now(),
            profile_pic=""
        )
        #create client
        client.save()

        p = Photographer(
            client=client,
            bio="Hello test",
            radius=25,
            tags = ""
        )
        p.save()
        record = Photographer.objects.filter(id=p.id).first()
        self.assertEqual(True, is_photographer(record.client.user.id))
        
    def test_is_photographer_false(self):
        address = Address(zip_code='91323',
        country_sn='USA',
        state_sn = 'CA',
        city_sn='Fake city',
        latitude=Decimal(30),
        longitude=Decimal(20),
        street_address="fake street 123",
        street_address2 = "Apt 2"
        )
        address.save()
        user=User.objects.create_user('username', password='userpassword')
        user.is_superuser = False
        user.is_staff = False
        user.save()
        client = Client(
            user=user,
            address = address,
            dob=datetime.now(),
            profile_pic=""
        )
        #create client
        client.save()
        record = Client.objects.filter(id=client.id).first()
        self.assertEqual(False, is_photographer(record.user.id))
    
    def test_get_photographer_id_from_user_id(self):
        address = Address(zip_code='91323',
        country_sn='USA',
        state_sn = 'CA',
        city_sn='Fake city',
        latitude=Decimal(30),
        longitude=Decimal(20),
        street_address="fake street 123",
        street_address2 = "Apt 2"
        )
        address.save()
        user=User.objects.create_user('username', password='userpassword')
        user.is_superuser = False
        user.is_staff = False
        user.save()
        client = Client(
            user=user,
            address = address,
            dob=datetime.now(),
            profile_pic=""
        )
        #create client
        client.save()

        p = Photographer(
            client=client,
            bio="Hello test",
            radius=25,
            tags = ""
        )
        p.save()
        record = Photographer.objects.filter(id=p.id).first()
        self.assertEqual(p.id, get_photographer_id_from_user_id(p.client.user.id))

    def test_retrieve_photographs_events_and_schedule_none(self):
        address = Address(zip_code='91323',
        country_sn='USA',
        state_sn = 'CA',
        city_sn='Fake city',
        latitude=Decimal(30),
        longitude=Decimal(20),
        street_address="fake street 123",
        street_address2 = "Apt 2"
        )
        address.save()
        user=User.objects.create_user('username', password='userpassword')
        user.is_superuser = False
        user.is_staff = False
        user.save()
        client = Client(
            user=user,
            address = address,
            dob=datetime.now(),
            profile_pic=""
        )
        #create client
        client.save()

        p = Photographer(
            client=client,
            bio="Hello test",
            radius=25,
            tags = ""
        )
        p.save()

        record = Photographer.objects.filter(id=p.id).first()
        
        self.assertEqual(retrieve_photographers_events_and_schedule(record.id), ("{}", "[]"))
    #### Testing find_photographer_in_radius ####
    def test_find_photographer_in_radius_no_results(self):
        x = find_photographer_in_radius(10, 10, 25)
        self.assertEqual(x, ([], '[]'))
        
    def test_find_photographer_in_yuba_from_chico_50_mi(self):
        address = Address(zip_code = '95991',
            country_sn = 'US',
            state_sn = 'CA',
            city_sn = 'Yuba City',
            latitude = Decimal(39.134275),
            longitude = Decimal(-121.633859),
            street_address = '750 North Palora Avenue'
        )
        address.save()

        user=User.objects.create_user('username', password='userpassword')
        user.is_superuser = False
        user.is_staff = False
        user.save()
        client = Client(
            user=user,
            address = address,
            dob=datetime.now(),
            profile_pic=""
        )
        client.save()

        p = Photographer(
            client=client,
            bio="Hello test",
            radius=25,
            tags = ""
        )
        p.save()
        radius = 50
        radius = radius * 1.609# convert to km
        x = find_photographer_in_radius(Decimal(39.7284944), Decimal(-121.83747770000002),radius )
        
        self.assertEqual(x, ([p], '[{"name": "", "lat": 39.134275, "lng": -121.633859}]'))
        
    def test_find_photographer_in_yuba_from_chico_25_mi(self):
        address = Address(zip_code = '95991',
            country_sn = 'US',
            state_sn = 'CA',
            city_sn = 'Yuba City',
            latitude = Decimal(39.134275),
            longitude = Decimal(-121.633859),
            street_address = '750 North Palora Avenue'
        )
        address.save()

        user=User.objects.create_user('username', password='userpassword')
        user.is_superuser = False
        user.is_staff = False
        user.save()
        client = Client(
            user=user,
            address = address,
            dob=datetime.now(),
            profile_pic=""
        )
        client.save()

        p = Photographer(
            client=client,
            bio="Hello test",
            radius=25,
            tags = ""
        )
        p.save()
        radius = 25
        radius = radius * 1.609# convert to km
        x = find_photographer_in_radius(Decimal(39.7284944), Decimal(-121.83747770000002),radius )
        
        self.assertEqual(x, ([], '[]'))

    def test_find_photographer_in_yuba_from_chico_75_mi(self):
        address = Address(zip_code = '95991',
            country_sn = 'US',
            state_sn = 'CA',
            city_sn = 'Yuba City',
            latitude = Decimal(39.134275),
            longitude = Decimal(-121.633859),
            street_address = '750 North Palora Avenue'
        )
        address.save()

        user=User.objects.create_user('username', password='userpassword')
        user.is_superuser = False
        user.is_staff = False
        user.save()
        client = Client(
            user=user,
            address = address,
            dob=datetime.now(),
            profile_pic=""
        )
        client.save()

        p = Photographer(
            client=client,
            bio="Hello test",
            radius=25,
            tags = ""
        )
        p.save()
        radius = 75
        radius = radius * 1.609# convert to km
        x = find_photographer_in_radius(Decimal(39.7284944), Decimal(-121.83747770000002),radius )
        
        self.assertEqual(x, ([p], '[{"name": "", "lat": 39.134275, "lng": -121.633859}]'))

    def test_retrieve_photographers_events_and_schedule(self):
        # create photographer
        address = Address(zip_code = '95991',
            country_sn = 'US',
            state_sn = 'CA',
            city_sn = 'Yuba City',
            latitude = Decimal(39.134275),
            longitude = Decimal(-121.633859),
            street_address = '750 North Palora Avenue'
        )
        address.save()

        user=User.objects.create_user('username', password='userpassword')
        user.is_superuser = False
        user.is_staff = False
        user.save()
        client = Client(
            user=user,
            address = address,
            dob=datetime.now(),
            profile_pic=""
        )
        client.save()

        p = Photographer(
            client=client,
            bio="Hello test",
            radius=25,
            tags = ""
        )
        p.save()

        #create schedule
        s = Schedule(
            photographer_id=p,
            date=datetime.now(),
            time="[]",
            fully_booked=False,
            max_bookings=3,
            cur_num_of_bookings=0,
            is_confirmed = False
        )

        s.save()
        #create event
        et = Event_Type(
            name="Wedding",
        )

        et.save()

        #create client for event
        u=User.objects.create_user('booker', password='b123123')
        user.is_superuser = False
        user.is_staff = False
        user.save()
        c = Client(
            user = u,
            dob=datetime.now(),
            profile_pic=""
        )
        c.save()

        e = Event(
            event_type=et,
            schedule_id=s,
            client=c,
            start_time= datetime.now(),
            end_time= datetime.now(),
            confirmed = False
        )

        e.save()
        
        # gather expected info
        event_object = {
                "client_name": e.get_client_name(),
                "start_time": str(e.get_start_time()),
                "end_time": str(e.get_end_time()),
                "id": e.id,
                "confirmed": e.is_confirmed()
        }
        e_list = [event_object]

        schedule_data = {
            "date": str(s.date),
            "num_bookings": 0,
            "max_bookings": s.max_bookings,
            "fully_booked": s.fully_booked
        }
        events = {}
        events[str(s.date)] = e_list
        s_list = [schedule_data]
        x = retrieve_photographers_events_and_schedule(p.id)
        self.assertEqual(x,json.dumps(events), json.dumps(schedule_data))        
