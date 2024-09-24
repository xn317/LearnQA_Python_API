import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure


@allure.epic("Delete user cases")
class TestUserDelete(BaseCase):

    def create_new_user(self):
        register_data = self.prepare_registration_data()
        response = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")
        register_data["id"] = self.get_json_value(response, "id")
        return register_data

    def user_login(self, email, password):
        login_data = {
            'email': email,
            'password': password
        }
        response = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response, "auth_sid")
        token = self.get_header(response, 'x-csrf-token')
        return auth_sid, token

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Test delete user with ID < 5")
    @allure.description("This test try to delete user with small ID")
    @allure.label("owner", "Dmitry Dubrovin")
    def test_delete_small_id_user(self):
        auth_sid, token = self.user_login('vinkotov@example.com', '1234')
        header = {"x-csrf-token": token}
        cookies = {"auth_sid": auth_sid}

        user_id = 2

        response = MyRequests.delete(f"/user/{user_id}", headers=header, cookies=cookies)
        Assertions.assert_code_status(response, 400)
        Assertions.assert_json_value_by_name(
            response,
            'error',
            "Please, do not delete test users with ID 1, 2, 3, 4 or 5.",
            f"Wrong error. Expected 'Please, do not delete test users with ID 1, 2, 3, 4 or 5."
        )

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Test delete user")
    @allure.description("This test create new user, delete this user and check it")
    @allure.label("owner", "Dmitry Dubrovin")
    def test_delete_user(self):
        user_data = self.create_new_user()

        user_id = user_data['id']

        auth_sid, token = self.user_login(user_data['email'], user_data['password'])
        header = {"x-csrf-token": token}
        cookies = {"auth_sid": auth_sid}

        response1 = MyRequests.delete(f"/user/{user_id}", headers=header, cookies=cookies)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_value_by_name(
            response1,
            'success',
            "!",
            f"Wrong answer. Expected '!'"
        )

        response2 = MyRequests.get(f"/user/{user_id}", headers=header, cookies=cookies)
        Assertions.assert_code_status(response2, 404)
        assert response2.content.decode("utf-8") == f"User not found", \
            f"Unexpected response content {response2.content}"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Test delete user by other user")
    @allure.description("This test create new user and try to delete it from other user")
    @allure.label("owner", "Dmitry Dubrovin")
    def test_delete_user_by_other(self):

        user_data1 = self.create_new_user()
        user_id1 = user_data1['id']
        auth_sid1, token1 = self.user_login(user_data1['email'], user_data1['password'])
        header1 = {"x-csrf-token": token1}
        cookies1 = {"auth_sid": auth_sid1}

        # Создаем и подключаемся другим пользователем
        user_data2 = self.create_new_user()
        user_id2 = user_data2['id']
        auth_sid2, token2 = self.user_login(user_data2['email'], user_data2['password'])
        header2 = {"x-csrf-token": token2}
        cookies2 = {"auth_sid": auth_sid2}

        response1 = MyRequests.delete(f"/user/{user_id1}", headers=header2, cookies=cookies2)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_value_by_name(
            response1,
            'success',
            "!",
            f"Wrong answer. Expected '!'"
        )

        response2 = MyRequests.get(f"/user/{user_id1}", headers=header1, cookies=cookies1)
        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "id")

        response3 = MyRequests.get(f"/user/{user_id2}", headers=header2, cookies=cookies2)
        Assertions.assert_code_status(response3, 404)
        assert response3.content.decode("utf-8") == f"User not found", \
            f"Unexpected response content {response3.content}"
