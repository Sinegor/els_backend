import unittest
import os
from fastapi import Request
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

    def test_new_registration(self):
        with TestClient(self.app) as http_client:
            testing_data = {
                'login': 'SuperMario',
                'password': 'wzadnn',
                'userMail': 'sie.inn@gmal.com',
                'phoneNumber': '24'

            }
            result_response = http_client.post(f'/auth/registration/', json=testing_data)
            print(result_response.status_code)
            print(result_response.text)
            assert result_response.status_code ==201, "Query processed with an error"
    
            
    # def test_login(self):
    #     with TestClient(self.app) as http_client:
    #         test_data = {
    #                 'username':'Arny_big',
    #                 'password':'wzadnn'
    #         }
    #         return_response = http_client.post(f'/auth', data=test_data)
    #         print(return_response.text)
    #         assert return_response.status_code == 200, "Something is wrong!"
            
    # def test_check_current_user(self):
    #     with TestClient(self.app) as http_client:
    #         result_response = http_client.get (f'/users/me/')
    #         print (result_response.request.url)
    #         print(result_response.status_code)
                     
