from django.test import TestCase
from .models import Client, Mailing, Message
from django.shortcuts import get_object_or_404
from django.utils import timezone


class TestClientsAPI(TestCase):
    """
    Tests API endpoints concerning client base
    """

    def setUp(self):
        self.client_url = '/clients/'
        self.data = {
            "phone_number": 79998887766,
            "tag": "wrong_test_tag",
            "timezone": "Africa/Abidjan"
        }
        self.client.post(
            self.client_url,
            self.data,
            follow=True
        )

    def testAddUser(self):
        """
        Tests /clients/ with method POST to create a client
        """
        self.data = {
            "phone_number": 71112223344,
            "tag": "test_tag",
            "timezone": "Africa/Abidjan"
        }
        self.response = self.client.post(
            self.client_url,
            self.data,
            follow=True
        )
        self.status_code = self.response.status_code
        self.assertEqual(self.status_code, 201)
        self.client_data = Client.objects.get(phone_number=self.data['phone_number'])
        if self.client_data:
            self.result = True
        else:
            self.result = False
        self.assertTrue(self.result)

    def testEditUser(self):
        """
        Tests /clients/{int} with method PUT to edit a client
        """
        self.data = {
            "phone_number": 79998887766,
            "tag": "right_test_tag",
            "timezone": "Africa/Abidjan"
        }
        self.client_data = Client.objects.get(phone_number=self.data["phone_number"])
        self.id = self.client_data.id
        self.response = self.client.put(
            self.client_url + str(self.id),
            self.data,
            follow=True
        )
        self.status_code = self.response.status_code
        self.assertEqual(self.status_code, 200)

    def testDeleteUser(self):
        """
        Tests /clients/{int} with method DELETE to delete a client
        """
        self.client_data = Client.objects.get(phone_number=self.data["phone_number"])
        self.id = self.client_data.id
        self.response = self.client.delete(
            self.client_url + str(self.id),
            follow=True
        )
        self.status_code = self.response.status_code
        self.assertEqual(self.status_code, 200)


class TestMailingAPI(TestCase):
    """
    Tests API endpoints concerning mailing base
    """

    def setUp(self):
        self.mailing_url = '/mailings/'
        self.data = {
            "start_datetime": timezone.now(),
            "text": "some_text",
            "filter_tag": "some_tag",
            "filter_code": "some_code",
            "end_datetime": timezone.now()
        }
        test = Mailing.objects.create(
            start_datetime=self.data['start_datetime'],
            text=self.data['text'],
            filter_tag=self.data['filter_tag'],
            end_datetime=self.data['end_datetime'],
            filter_code=self.data['filter_code']
        )
        test.save()
        self.mailing_id = test.id

    def testAddMailing(self):
        """
        Tests /mailings/ with method POST to add a new mailing
        """
        self.data = {
            "start_datetime": timezone.now(),
            "text": "some_other_text",
            "filter_tag": "some_other_tag",
            "end_datetime": timezone.now(),
            "filter_code": "some_other_code"
        }
        self.response = self.client.post(
            self.mailing_url,
            self.data,
            follow=True
        )
        self.status_code = self.response.status_code
        self.assertEqual(self.status_code, 201)

    def testGetMailings(self):
        """
        Tests /mailings/ with method GET to get info on all mailings
        """
        self.response = self.client.get(
            self.mailing_url,
            follow=True
        )

    def testGetMailing(self):
        """
        Tests /mailings/{id} with method GET to get info on a particular mailing
        """
        self.response = self.client.get(
            self.mailing_url + str(self.mailing_id),
            follow=True
        )
        self.status_code = self.response.status_code
        self.assertEqual(self.status_code, 200)

    def testEditMailing(self):
        """
        Tests /mailings/{id} with method PUT to edit a mailing
        """
        self.data = {
            "start_datetime": timezone.now(),
            "text": "some_text_but_another",
            "filter_tag": "some_tag",
            "end_datetime": timezone.now(),
            "filter_code": "some_code"
        }
        self.response = self.client.put(
            self.mailing_url + str(self.mailing_id),
            self.data,
            follow=True
        )
        self.status_code = self.response.status_code
        self.assertEqual(self.status_code, 200)

    def testDeleteMailing(self):
        """
        Tests /mailings/{id} with method DELETE to delete a mailing
        """
        self.response = self.client.delete(
            self.mailing_url + str(self.mailing_id),
            follow=True
        )
        self.status_code = self.response.status_code
        self.assertEqual(self.status_code, 200)
