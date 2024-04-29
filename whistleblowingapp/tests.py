from unittest.mock import patch, MagicMock

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse



from whistleblowingapp.models import User, Report, ReportForm
from whistleblowingapp.views import signedin, viewUserReports


# Create your tests here.
class userTypeTests(TestCase):

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

class MockUser:
    def __init__(self, is_authenticated=True, is_staff=False, first_name="", last_name="", email=""):
        self.is_authenticated = is_authenticated
        self.is_staff = is_staff
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

class differentViewsTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def testSignedInViewAdmin(self):
        request = self.factory.get(reverse('whistleblowingapp:signedin'))
        mockFirst = "Alexs"
        mockLast = "Admin"
        mockEmail = "iamadmin@gmail.com"
        request.user = MockUser(is_authenticated=True, is_staff=True, first_name=mockFirst, last_name=mockLast, email=mockEmail)

        response = signedin(request)

        #print(response.content.decode('utf-8'))
        self.assertIn(("You are signed in as: " + mockFirst + " "+ mockLast), response.content.decode('utf-8'))
        self.assertIn(("Admin/Staff status: True"), response.content.decode('utf-8'))

    def testSignedInViewDefault(self):
        request = self.factory.get(reverse('whistleblowingapp:signedin'))
        mockFirst = "Bob"
        mockLast = "NotAdmin"
        mockEmail = "iamnotanadmin@gmail.com"
        request.user = MockUser(is_authenticated=True, is_staff=False, first_name=mockFirst, last_name=mockLast, email=mockEmail)

        response = signedin(request)

        #print(response.content.decode('utf-8'))
        self.assertIn(("You are signed in as: " + mockFirst + " "+ mockLast), response.content.decode('utf-8'))
        self.assertIn(("Admin/Staff status: False"), response.content.decode('utf-8'))

class ReportFormTests(TestCase):

    def test_valid_data_with_upload(self):
        dummy_txt = SimpleUploadedFile("report.txt", b"Report text content")
        dummy_pdf = SimpleUploadedFile("report.pdf", b"PDF content", content_type="application/pdf")

        form_data = {
            'reportTitle': 'Test Report Title',
            'reportDescription': 'This is a test report description.',
        }
        form = ReportForm(data=form_data, files={'reportText': dummy_txt, 'reportPDF': dummy_pdf})
        self.assertTrue(form.is_valid())

    def test_valid_data_no_uploads(self):
        form_data = {
            'reportTitle': 'Test Report Title',
            'reportDescription': 'This is a test report description.',
        }
        form = ReportForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_data_no_data(self):
        form = ReportForm(data={})
        self.assertFalse(form.is_valid())

    def test_invalid_data_empty_title(self):
        form = ReportForm(data={'reportTitle': '', 'reportDescription': 'This is the description'})
        self.assertFalse(form.is_valid())

    def test_invalid_data_empty_description(self):
        form = ReportForm(data={'reportTitle': 'This is the title', 'reportDescription': ''})
        self.assertFalse(form.is_valid())

    def test_report_submitted(self):
        response = self.client.post(reverse('whistleblowingapp:submitted'), data={
            'reportTitle': 'Another Test Report xxxasdf',
            'reportDescription': 'Detailed description of the report123.',
        })
        self.assertTemplateUsed(response, 'whistleblowingapp/submitted.html')
        self.assertEqual(Report.objects.count(),1)
        report = Report.objects.first()
        self.assertEqual(report.reportTitle, 'Another Test Report xxxasdf')
        self.assertEqual(report.reportDescription, 'Detailed description of the report123.')


    #TODO: possibly refactor our User model to extend Django AbstractUser idk if necessary??

    # then we could make use of methods like force_login
    # def testSignedInView(self):
    #     # self.client = self.client_class()
    #     # self.client.handler._middleware_chain = MockAuthenticationMiddleware(
    #     #     self.client.handler._middleware_chain, self.u1
    #     # )
    #
    #     session = self.client.session
    #     session['user_id'] = self.u1.id
    #     session.save()
    #
    #     response = self.client.get(reverse('whistleblowingapp:signedin'))
    #     #self.client.force_login(self.u1)
    #     #mock the user being signed in so that {% if user.is_authenticated %} gets triggered
    #     print(response.content.decode('utf-8'))
    #     self.assertNotIn("Log in to Google!", response.content.decode('utf-8'))
    #     self.assertIn("You are signed in as", response.content.decode('utf-8'))
    #

    #

    #
    # class MockAuthenticationMiddleware:
    #     def __init__(self, get_response, user):
    #         self.get_response = get_response
    #         self.user = user
    #
    #     def __call__(self, request):
    #         request.user = self.user
    #         response = self.get_response(request)
    #         return response

