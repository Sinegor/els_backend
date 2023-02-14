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

    def test_start(self):
        with TestClient(self.app) as http_client:
            testing_data = {
                'login': 'Armen_21',
                'password': 'wzadnn',
                'userMail': 'sin.nn@gmal.com',
                'phoneNumber': '422442224'

            }
            result_response = http_client.post(f'/client/registration/', json=testing_data)
            print(result_response.status_code)
            assert result_response.status_code ==201, "Query processed with an error"
            

    
    # def test_start_1(self):
    #     with TestClient(self.app) as http_client:
    #         result_response = http_client.get(f'/items/', headers={'Authorization':'Bearer'})
    #         print(f"Ответ: {result_response.headers}")
    #         print (result_response.request.headers)
    #         assert result_response.status_code ==200, "Query processed with an error"
            
    # def test_login(self):
    #     with TestClient(self.app) as http_client:
    #         test_data = {
    #                 'username':'Armen',
    #                 'password':'wzadnn'
    #         }
    #         return_response = http_client.post(f'/authorization/token', data=test_data)
    #         print(return_response.text)
    #         assert return_response.status_code == 200, "Something is wrong!"
            
