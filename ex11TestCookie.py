import requests


class TestCookie:
    def test_cookie(self):
        url = 'https://playground.learnqa.ru/api/homework_cookie'
        response = requests.get(url)

        cookie_name = "HomeWork"
        cookie_value = "hw_value"

        assert response.status_code == 200, f"Ошибка выполнения запроса, код ответа: {response.status_code}"

        assert len(response.cookies) != 0, f"Ответ от сервера не содержит Cookies"

        for cookie in response.cookies:
            print(f"Получено cookie: {cookie.name}={cookie.value}")

        assert response.cookies.get(cookie_name) == cookie_value, \
            f"В ответе сервера отсутствует Cookie '{cookie_name}' со значением '{cookie_value}'"
