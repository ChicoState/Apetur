from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from .models import Address
from .models import Client

class BasicTest(TestCase):

    def test_addresses(self):

        #create test address as Address
        address = Address()
        address.zip_code = '95926'
        address.country_sn = '5'
        address.state_sn = 'CA'
        address.city_sn = 'Chico'
        address.latitude = '150'
        address.longitue = '20'
        address.street_address = 'hello 1520 St'
        address.street_address_2 = 'goodbye 0251 tS'

        #record = Address.object.get(pk=1)
        #test address
        record = address
        self.assertEqual(record, address)

    def test_client(self):

        #create client
        client = Client()
        client.city_sn = 'Chico'
        self.assertEqual(client, client)
        
        

        


