import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure


@allure.epic("Edit user cases")
class TestUserEdit(BaseCase):
    user_params = ['username', 'firstName', 'lastName', 'email']

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

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Test edit user")
    @allure.description("This test create new user and edit firstName to it")
    def test_edit_just_created_user(self):
        user_data = self.create_new_user()

        user_id = user_data['id']
        first_name = user_data['firstName']

        auth_sid, token = self.user_login(user_data['email'], user_data['password'])
        header = {"x-csrf-token": token}
        cookies = {"auth_sid": auth_sid}

        # Проверяем, что у нового пользователя корректный firstName
        response1 = MyRequests.get(f"/user/{user_id}", headers=header, cookies=cookies)
        Assertions.assert_json_value_by_name(
            response1,
            "firstName",
            first_name,
            "Wrong name of the user before edit"
        )

        # EDIT
        new_name = "Changed Name"
        response2 = MyRequests.put(f"/user/{user_id}", headers=header, cookies=cookies, data={"firstName": new_name})
        Assertions.assert_code_status(response2, 200)

        # GET
        response3 = MyRequests.get(f"/user/{user_id}", headers=header, cookies=cookies)
        Assertions.assert_json_value_by_name(
            response3,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Test edit user without auth")
    @allure.description("This test create new user and try edit params without auth")
    @pytest.mark.parametrize('param', user_params)
    def test_no_auth_edit(self, param):
        user_data = self.create_new_user()

        user_id = user_data['id']

        auth_sid, token = self.user_login(user_data['email'], user_data['password'])
        header = {"x-csrf-token": token}
        cookies = {"auth_sid": auth_sid}

        # Проверяем, что у нового пользователя перед изменением отображается ожидаемый параметр
        response1 = MyRequests.get(f"/user/{user_id}", headers=header, cookies=cookies)
        Assertions.assert_json_value_by_name(
            response1,
            param,
            user_data[param],
            f"Wrong param {param} of the user before edit"
        )

        # EDIT without auth (no header or cookie or both)
        new_param = "CHANGED PARAM!!!"
        not_auth_responses = [MyRequests.put(f"/user/{user_id}", headers=header, data={param: new_param}),
                              MyRequests.put(f"/user/{user_id}", cookies=cookies, data={param: new_param}),
                              MyRequests.put(f"/user/{user_id}", data={param: new_param})]

        for not_auth_response in not_auth_responses:
            Assertions.assert_code_status(not_auth_response, 400)
            Assertions.assert_json_value_by_name(
                not_auth_response,
                'error',
                "Auth token not supplied",
                f"Wrong error. Expected 'Auth token not supplied'"
            )

        # Проверяем, что у пользователя после попытки изменения параметры не изменились
        response5 = MyRequests.get(f"/user/{user_id}", headers=header, cookies=cookies)
        Assertions.assert_json_value_by_name(
            response5,
            param,
            user_data[param],
            f"Wrong param {param} of the user after edit"
        )

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Test edit user by other user")
    @allure.description("This test create new user and try edit params by other user")
    @pytest.mark.parametrize('param', user_params)
    def test_edit_by_other_user(self, param):
        user_data = self.create_new_user()

        user_id = user_data['id']

        auth_sid1, token1 = self.user_login(user_data['email'], user_data['password'])
        header1 = {"x-csrf-token": token1}
        cookies1 = {"auth_sid": auth_sid1}

        # Проверяем, что у нового пользователя перед изменением отображается ожидаемый параметр
        response1 = MyRequests.get(f"/user/{user_id}", headers=header1, cookies=cookies1)
        Assertions.assert_json_value_by_name(
            response1,
            param,
            user_data[param],
            f"Wrong param {param} of the user before edit"
        )
        # Создаем и подключаемся другим пользователем
        user_data2 = self.create_new_user()
        auth_sid2, token2 = self.user_login(user_data2['email'], user_data2['password'])
        header2 = {"x-csrf-token": token2}
        cookies2 = {"auth_sid": auth_sid2}

        # EDIT new user by other user
        new_param = "CHANGED"+user_data[param]
        response2 = MyRequests.put(f"/user/{user_id}", headers=header2, cookies=cookies2, data={param: new_param})
        Assertions.assert_code_status(response2, 200)

        # Проверяем, что у первого пользователя после попытки изменения параметры не изменились
        response3 = MyRequests.get(f"/user/{user_id}", headers=header1, cookies=cookies1)
        Assertions.assert_json_value_by_name(
            response3,
            param,
            user_data[param],
            f"Wrong param {param} of the user1 after edit. Expected:{user_data[param]}"
        )

        # Проверяем, что у второго пользователя после попытки изменения параметры изменились
        response4 = MyRequests.get(f"/user/{user_data2['id']}", headers=header2, cookies=cookies2)
        Assertions.assert_json_value_by_name(
            response4,
            param,
            new_param,
            f"Wrong param {param} of the user2 after edit. Expected:{new_param} "
        )

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Test edit user and set incorrect email")
    @allure.description("This test create new user and try edit email to incorrect")
    def test_edit_email_to_incorrect(self):
        user_data = self.create_new_user()

        user_id = user_data['id']

        auth_sid, token = self.user_login(user_data['email'], user_data['password'])
        header = {"x-csrf-token": token}
        cookies = {"auth_sid": auth_sid}

        # EDIT new user by other user
        new_email = "testmail.com"
        response1 = MyRequests.put(f"/user/{user_id}", headers=header, cookies=cookies, data={'email': new_email})
        Assertions.assert_code_status(response1, 400)
        Assertions.assert_json_value_by_name(
            response1,
            'error',
            "Invalid email format",
            f"Wrong error. Expected 'Invalid email format'"
        )

        # Проверяем, что у пользователя после попытки изменения параметры не изменились
        response2 = MyRequests.get(f"/user/{user_id}", headers=header, cookies=cookies)
        Assertions.assert_json_value_by_name(
            response2,
            'email',
            user_data['email'],
            f"Wrong email of the user after edit"
        )

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Test edit user and set incorrect firstName")
    @allure.description("This test create new user and try edit firstName to incorrect")
    def test_edit_firstname_to_incorrect(self):
        user_data = self.create_new_user()

        user_id = user_data['id']

        auth_sid, token = self.user_login(user_data['email'], user_data['password'])
        header = {"x-csrf-token": token}
        cookies = {"auth_sid": auth_sid}

        new_firstname = "1"
        response1 = MyRequests.put(f"/user/{user_id}", headers=header, cookies=cookies, data={'firstName': new_firstname})
        Assertions.assert_code_status(response1, 400)
        Assertions.assert_json_value_by_name(
            response1,
            'error',
            "The value for field `firstName` is too short",
            f"Wrong error. Expected 'The value for field `firstName` is too short'"
        )
        # Проверяем, что у пользователя после попытки изменения параметры не изменились
        response2 = MyRequests.get(f"/user/{user_id}", headers=header, cookies=cookies)
        Assertions.assert_json_value_by_name(
            response2,
            'firstName',
            user_data['firstName'],
            f"Wrong email of the user after edit"
        )