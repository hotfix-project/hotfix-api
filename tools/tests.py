from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
import json

class QrcodeTests(APITestCase):
    def test_qrcode(self):
        url = '/qrcode/http://www.qianbao.com'
        response = self.client.get(url)
        content_type = json.dumps(response._headers["content-type"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content_type, '["Content-Type", "image/png"]')

    def test_qrcode_404(self):
        url = '/qrcode/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
