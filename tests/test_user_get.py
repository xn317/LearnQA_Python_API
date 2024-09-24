from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure


@allure.epic("Get user info cases")
class TestUserGet(BaseCase):
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Test get user details without authorization")
    @allure.description("This test try to get user details without authorization")
    @allure.label("owner", "Dmitry Dubrovin")
    def test_get_user_details_not_auth(self):
        response = MyRequests.get("/user/2")

        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_key(response, "email")
        Assertions.assert_json_has_not_key(response, "firstName")
        Assertions.assert_json_has_not_key(response, "lastName")

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Test get user details")
    @allure.description("This test authorize by user and try to get the details of it")
    @allure.label("owner", "Dmitry Dubrovin")
    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        response2 = MyRequests.get(f"/user/{user_id_from_auth_method}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid})

        expected_fileds = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response2, expected_fileds)

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Test get user details by other user")
    @allure.description("This test authorize by user and try to get the details of other user")
    @allure.label("owner", "Dmitry Dubrovin")
    def test_get_user_details_auth_as_other_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        other_user_id = user_id_from_auth_method + 1

        response2 = MyRequests.get(f"/user/{other_user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid})

        expected_fields = ["username"]
        unexpected_fields = ["email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response2, expected_fields)
        Assertions.assert_json_has_not_keys(response2, unexpected_fields)
