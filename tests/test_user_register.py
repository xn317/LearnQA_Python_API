import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure


@allure.epic("Registration cases")
class TestUserRegister(BaseCase):

    registr_url = '/user/'
    registration_fields = ['password', 'username', 'firstName', 'lastName', 'email']

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Test create user")
    @allure.description("This test successfully create user")
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post(self.registr_url, data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Test create user with existing email")
    @allure.description("This test successfully create user with existing email")
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email=email)

        response = MyRequests.post(self.registr_url, data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
                                                   f"Unexpected response content {response.content}"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Test create user with incorrect email")
    @allure.description("This test try to create user with incorrect email (no '@' symbol)")
    def test_create_user_with_invalid_email(self):
        email = 'vinkotovexample.com'
        data = self.prepare_registration_data(email=email)

        response = MyRequests.post(self.registr_url, data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Test create user without some fields")
    @allure.description("This test try to create user without some fields")
    @pytest.mark.parametrize('field', registration_fields)
    def test_create_user_without_field(self, field):
        data = self.prepare_registration_data()
        del data[field]

        response = MyRequests.post(self.registr_url, data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {field}"

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Test create user with very short name")
    @allure.description("This test try to create user with very short name fields (1 symbol)")
    @pytest.mark.parametrize('name_field', filter(lambda key: 'name' in key.lower(), registration_fields))
    def test_create_user_with_short_name(self, name_field):
        data = self.prepare_registration_data()
        data[name_field] = '1'

        response = MyRequests.post(self.registr_url, data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of '{name_field}' field is too short"

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Test create user with long name")
    @allure.description("This test try to create user with long name fields (>250 symbols)")
    @pytest.mark.parametrize('name_field', filter(lambda key: 'name' in key.lower(), registration_fields))
    def test_create_user_with_long_name(self, name_field):
        data = self.prepare_registration_data()
        data[name_field] = '1'*251

        response = MyRequests.post(self.registr_url, data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of '{name_field}' field is too long"
