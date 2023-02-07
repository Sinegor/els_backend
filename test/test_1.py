import unittest
import os
from fastapi.testclient import TestClient
import json
from server.main import app


class UserAPITestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = app

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_start(self):
        with TestClient(self.app) as http_client:
            testing_data = {
                'login': 'Lena',
                'password': '12134234',
                'userMail': 'fdfdfdfdf',
                'phoneNumber': '42424224424224'

            }
            result_response = http_client.post(f'/client/registration/', json=testing_data)
            #print(result_response.request.url)
            assert result_response.status_code ==200, "Query processed with an error"
            

    
    # def test_start_1(self):
    #     with TestClient(self.app) as http_client:
    #         result_response = http_client.get(f'/')
    #         assert result_response.status_code ==200, "Query processed with an error"
    #         print(result_response.status_code)
    #         print(result_response.request.headers)
            
            
    