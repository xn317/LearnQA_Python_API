import requests


class TestHeader:
    def test_header(self):
        url = 'https://playground.learnqa.ru/api/homework_header'
        response = requests.get(url)

        header_name = "x-secret-homework-header"
        header_value = "Some secret value"

        assert response.status_code == 200, f"Ошибка выполнения запроса, код ответа: {response.status_code}"

        assert len(response.headers) != 0, f"Ответ от сервера не содержит Headers"

        for name, value in response.headers.items():
            print(f"Получен header: {name}={value}")

        assert response.headers.get(header_name) == header_value, \
            f"В ответе сервера отсутствует Header '{header_name}' со значением '{header_value}'"
