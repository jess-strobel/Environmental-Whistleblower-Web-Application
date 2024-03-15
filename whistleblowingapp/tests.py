from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
from django.test import TestCase
from django.urls import reverse

from whistleblowingapp.models import User


# Create your tests here.
class userTypeTests(TestCase):
    #print("testing user types")

    def setUp(self):
        self.u1 = User.objects.create(admin=False, user="user1", password="pass1")
        self.a1 = User.objects.create(admin=True, user="admin1", password="pass2")
        site = Site.objects.get_current()
        social_app = SocialApp.objects.create(
            provider='google',
            name='Google',
            client_id='your_test_client_id',
            secret='your_test_secret',
            key=''
        )
        social_app.sites.add(site)
        social_app.save()

    def testAdminStatus(self):
        self.assertFalse(self.u1.isadmin())
        self.assertTrue(self.a1.isadmin())

    def testIndexView(self):
        response = self.client.get(reverse('whistleblowingapp:whistleblowingapp'))
        # print("RESPONSE: ", response.content.decode('utf-8'))
        self.assertIn("Log in to Google!", response.content.decode('utf-8'))

    def testSignedInView(self):
        response = self.client.get(reverse('whistleblowingapp:signedin'))
        #self.client.force_login(self.u1)
        #mock the user being signed in so that {% if user.is_authenticated %} gets triggered
        print(response.content.decode('utf-8'))
        self.assertNotIn("Log in to Google!", response.content.decode('utf-8'))

        #TODO: possibly refactor our User model to extend Django AbstractUser??
        #then we could make use of methods like force_logi

