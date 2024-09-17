import requests
import pytest
import json


def get_test_params():
    test_params = []
    url = ('https://gist.githubusercontent.com/KotovVitaliy/138894aa5b6fa442163561b5db6e2e26/'
           'raw/6916020a6a9cf1fbf0ee34c7233ade94d766cc96/some.txt')
    try:
        response = requests.get(url)
    except Exception as e:
        assert False, f"Ошибка {e} при выполнении запроса к {url}"
    assert "User Agent:" in response.text, "Ошибка получения параметров теста. Не найдены параметры User Agent"
    # Разделяем полученный тест на части по User Agent
    for ua_split in response.text.split("User Agent:\n\n")[1:]:
        # Получаем значение User Agent и Expected values
        user_agent, expected_values = ua_split.split("\n\nExpected values:\n\n")
        # Отрезаем лишнее от expected values и заменяем кавычки для дальнейшего преобразования в JSON
        expected_values = expected_values.split("\n")[0].replace("'", "\"")
        # заполняем массив тестовых параметров
        test_params.append({"user_agent": user_agent, "expected_values": "{" + expected_values + "}"})
    return test_params


class TestUserAgent():
    test_param = get_test_params()
    url = "https://playground.learnqa.ru/ajax/api/user_agent_check"

    @pytest.mark.parametrize('test_param', test_param)
    def test_user_agent(self, test_param):
        header = {'User-Agent': test_param["user_agent"]}
        try:
            response = requests.get(self.url, headers=header)
        except Exception as e:
            assert False, f"Ошибка {e} при выполнении запроса к {self.url}"
        try:
            response = json.loads(response.text)
        except json.decoder.JSONDecodeError:
            assert False, f"Ответ сервера не в JSON формате '{response.text}'"
        try:
            expected = json.loads(test_param["expected_values"])
        except json.decoder.JSONDecodeError:
            assert False, f"Ожидаемые значения не в JSON формате '{test_param["expected_values"]}'"

        for expected_key in expected.keys():
            assert expected_key in response.keys(), (f"В ответе сервера {response} нет ожидаемого параметра "
                                                     f"{expected_key}")
            assert expected[expected_key] == response[expected_key], \
                (f"Ожидаемый и полученный результат разошлись для {test_param["user_agent"]}. "
                 f"Ожидаем: {expected_key} = {expected[expected_key]}. "
                 f"Получили: {expected_key} = {response[expected_key]}")
