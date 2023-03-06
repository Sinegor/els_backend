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
    #             'password': 'wzadnn',
    #             'userMail': 'sie.inn@gmal.com',
    #             'phoneNumber': '24'

    #         }
    #         result_response = http_client.post(f'/auth/registration/', json=testing_data)
    #         print(result_response.status_code)
    #         print(result_response.text)
    #         assert result_response.status_code ==201, "Query processed with an error"
    
            
    # def test_login(self):
    #     with TestClient(self.app) as http_client:
    #         test_data = {
    #                 'username':'Arny_big',
    #                 'password':'wzadnn'
    #         }
    #         return_response = http_client.post(f'/auth', data=test_data)
    #         print (return_response.text)
    #         assert return_response.status_code == 200, "Something is wrong!"
            
    def test_check_current_user(self):
        with TestClient(self.app) as http_client:
            token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2M2VjYTZmNmE3ZmZmZmRkNzllNzVmNmMiLCJsb2dpbiI6IkFybnlfYmlnIiwidXNlck1haWwiOiJzaW5lZWUuaW5uQGdtYWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOm51bGwsInBhc3N3b3JkIjoiJDJiJDEyJEIuazhzR0NuRGRIRk1OWU1tbUw3S2VZWGh4ZGJ6NGpJMXB0S3U5YVJBQmQuNS42ZVRGZkdDIiwicGhvbmVOdW1iZXIiOiIyMDAwMjIyNCIsImRldGFpbHMiOm51bGwsImRpc2FibGVkIjpudWxsLCJsYXN0X2FjdGl2aXR5IjpudWxsLCJsYXN0X21vZGlmaWNhdGlvbiI6bnVsbCwibW9kaWZpZWRfYnkiOm51bGwsInBheW1lbnRfZGV0YWlscyI6bnVsbCwibGVnYWxfaGVscF9hcHBsaWNhdGlvbnMiOm51bGwsImV4cCI6MTY3NzUxNTY3Mn0.853w4s25VXenT9kBSYbDmMFxfd3X4VaX5DlLbK5mvmk'
            result_response = http_client.get (f'/auth/users/me/', headers={'Authorization': f'Bearer {token}' })
            print (result_response.text)
            print (result_response.headers)
            print(result_response.status_code)
                     
