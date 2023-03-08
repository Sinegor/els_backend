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

    # def test_new_registration(self):
    #     with TestClient(self.app) as http_client:
    #         testing_data = {
    #             'login': 'SuperMario',
    #             'password': 'password',
    #             'userMail': 'sie.inn@gmal.com',
    #             'phoneNumber': '24',
                

    #         }
    #         result_response = http_client.post(f'/auth/registration/', json=testing_data)
    #         print(result_response.status_code)
    #         print(result_response.text)
    #         print (result_response.headers)
    #         assert result_response.status_code ==200, "Query processed with an error"
    
            
    # def test_login(self):
    #     with TestClient(self.app) as http_client:
    #         test_data = {
    #                 'username':'Arny_big',
    #                 'password':'wzadnn'
    #         }
    #         return_response = http_client.post(f'/auth', data=test_data)
    #         print (return_response.text)
    #         print(return_response.headers)
    #         assert return_response.status_code == 200, "Something is wrong!"
            
    def test_check_current_user(self):
        with TestClient(self.app) as http_client:
            token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHRlcm5hbF9pZCI6bnVsbCwibG9naW4iOiJTdXBlck1hcmlvIiwidXNlck1haWwiOiJzaWUuaW5uQGdtYWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOm51bGwsInBhc3N3b3JkIjoiJDJiJDEyJHVyYm1LYnBraFU3N3Bvc2NYVUZ6ak8xNk13MTNFZWZIL3RQUVF6MkdPbTRZV1lxVkJ6aWNPIiwicGhvbmVOdW1iZXIiOiIyNCIsImRldGFpbHMiOm51bGwsImRpc2FibGVkIjpudWxsLCJsYXN0X2FjdGl2aXR5IjpudWxsLCJsYXN0X21vZGlmaWNhdGlvbiI6bnVsbCwibW9kaWZpZWRfYnkiOm51bGwsInBheW1lbnRfZGV0YWlscyI6bnVsbCwibGVnYWxfaGVscF9hcHBsaWNhdGlvbnMiOm51bGwsImV4cCI6MTY3ODI4NDUzMX0.b_ywIOXn0Fn-uboQlFOx2zWlSEacX3xvmo_I-yiMsKA'
            result_response = http_client.get (f'/auth/users/me/', headers={'Authorization': f'Bearer {token}' })
            print (result_response.text)
            print (result_response.headers)
            print(result_response.status_code)
                     
