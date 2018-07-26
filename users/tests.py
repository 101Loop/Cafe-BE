from django.test import TestCase
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model


user1 = get_user_model().objects.create_user(username='test1', email='test1@civilmachines.com', password='123@abcd@123',
                                             name='Test User - 1', mobile='8800610541')

# class RegisterTests(APITestCase):
#
#

