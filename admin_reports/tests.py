from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, RequestsClient
from rest_framework import status



class AdminReportsTest(APITestCase):

    def test_active_merchants(self):
        url = "http://localhost:8000/api/v1.0/cross-border-transfers/"
        response = self.client.get(url)
        # assert response.status_code ==  status.HTTP_200_OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['local_currency'], "NGN")

    # def cross_border_transfer_test(self):
    #     url = "http://localhost:8000/api/v1.0/cross-border-transfers/"
    #     response = self.client.get(url)
    #     assert response.status_code ==  status.HTTP_200_OK


class ListOfMerchantTest(APITestCase):
    def list_of_merchants_test(self):
        pass

    def test_post_merchants(self):
        pass
