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
    #             'userMail': 'sinegor.nn@gmail.com',
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
    #                 'username':'SuperMario',
    #                 'password':'password'
    #         }
    #         return_response = http_client.post(f'/auth', data=test_data)
    #         print (return_response.text)
    #         print(return_response.headers)
    #         assert return_response.status_code == 200, "Something is wrong!"
            
    def test_check_current_user(self):
        with TestClient(self.app) as http_client:
            token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2NDRlNjM5NjcyNmU0NDc1NThlMWFhOTEiLCJleHRlcm5hbF9pZCI6bnVsbCwibG9naW4iOiJTdXBlck1hcmlvIiwidXNlck1haWwiOiJzaW5lZ29yLm5uQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjpudWxsLCJwYXNzd29yZCI6IiQyYiQxMiRPY3ZCWnRoQlVUN2hVRGlseUR5a211SUJEYUY0UGR1NVNlLlJ0Z0FaTnlRNmg0QmR3dVNPSyIsInBob25lTnVtYmVyIjoiMjQiLCJkZXRhaWxzIjpudWxsLCJkaXNhYmxlZCI6bnVsbCwibGFzdF9hY3Rpdml0eSI6bnVsbCwibGFzdF9tb2RpZmljYXRpb24iOm51bGwsIm1vZGlmaWVkX2J5IjpudWxsLCJwYXltZW50X2RldGFpbHMiOm51bGwsImxlZ2FsX2hlbHBfYXBwbGljYXRpb25zIjpudWxsLCJleHAiOjE2ODI4NjY5NjZ9.SDPCdm5DiEwV-JhyDiF7XzPnCSU9i0ZJWwmzcpmQ8K8'
            result_response = http_client.get (f'/auth/users/me/', headers={'Authorization': f'Bearer {token}' })
            print (result_response.text)
            print (result_response.headers)
            print(result_response.status_code)
                     
