import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure

@allure.epic("Authorization cases")
class TestUserAuth(BaseCase):
    exclude_params = ["no_cookie", "no_token"]

    @pytest.fixture(autouse=True)
    def setup(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post("/user/login", data=data)

        self.auth_sid = self.get_cookie(response1, "auth_sid")
        self.token = self.get_header(response1, "x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(response1, "user_id")

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Test auth user")
    @allure.description("This test successfully authorize user by email and password")
    @allure.label("owner", "Dmitry Dubrovin")
    def test_auth_user(self):
        response2 = MyRequests.get("/user/auth",
                                   headers={"x-csrf-token": self.token},
                                   cookies={"auth_sid": self.auth_sid})

        Assertions.assert_json_value_by_name(
            response2,
            "user_id",
            self.user_id_from_auth_method,
            "User id from auth method is not equal to user id from check method"
        )

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Test auth user without cookie or token")
    @allure.description("This test check authorization status w/o sending auth cookies or token")
    @allure.label("owner", "Dmitry Dubrovin")
    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_auth_check(self, condition):
        if condition == "no_cookie":
            response2 = MyRequests.get("/user/auth",
                                       headers={"x-csrf-token": self.token})
        else:
            response2 = MyRequests.get("/user/auth",
                                       cookies={"auth_sid": self.auth_sid})

        Assertions.assert_json_value_by_name(
            response2,
            "user_id",
            0,
            f"User is authorized with condition {condition}"
        )
