import requests

http_methods_list = ["POST", "GET", "PUT", "DELETE", "HEAD", "OPTIONS", "PATCH"]
approved_http_method_list = ["POST", "GET", "PUT", "DELETE"]


# Метод для отправки запроса на сервер
def compare_query_type(http_method, send_method="", is_send_method=True):
    url = 'https://playground.learnqa.ru/ajax/api/compare_query_type'
    data = {}
    if is_send_method:
        data = {"method": send_method}
    r = getattr(requests, http_method.lower())
    if http_method == "GET":
        response = r(url, params=data)
    else:
        response = r(url, data=data)
    return response


# Метод для выполнения задания п.1
def p1(http_method):
    response = compare_query_type(http_method, is_send_method=False)
    print(f"П.1.\tПри выполнении запроса {http_method} без параметра method ответ сервера - "
          f"код: {response.status_code}, текст:{response.text}")


# Метод для выполнения задания п.2
def p2():
    for http_method in list(set(http_methods_list) - set(approved_http_method_list)):
        response = compare_query_type(http_method)
        print(f"П.2.\tПри выполнении запроса {http_method} не из списка допустимых кодов, ответ сервера - "
              f"код: {response.status_code}, текст:{response.text}")


# Метод для выполнения задания п.3
def p3(http_method, send_method):
    response = compare_query_type(http_method, send_method)
    print(f"П.3.\tПри выполнении запроса {http_method} с правильным method ответ сервера - "
          f"код: {response.status_code}, текст:{response.text}")


# Метод для выполнения задания п.4
def p4():
    correct_responses = []
    incorrect_responses = []
    for http_method in http_methods_list:
        for send_method in http_methods_list + [""]:
            is_incorrect_answer = False
            response = compare_query_type(http_method, send_method, is_send_method=True)
            # Проверяем корректность ответа для поддерживаемых методов
            if http_method in approved_http_method_list:
                if (http_method == send_method and response.text != '{"success":"!"}') or \
                   (http_method != send_method and response.text == '{"success":"!"}') or \
                   response.status_code != 200:
                    is_incorrect_answer = True
            else:  # Остальные методы не поддерживаются, поэтому не ожидаем успешного ответа.
                if response.status_code != 400 or response.text == '{"success":"!"}':
                    is_incorrect_answer = True

            if is_incorrect_answer:
                incorrect_responses.append({"http_method": http_method,
                                            "send_method": send_method,
                                            "response": response})
            else:
                correct_responses.append({"http_method": http_method,
                                          "send_method": send_method,
                                          "response": response})

    print(f"Некорректные ответы:")
    for incorrect_response in incorrect_responses:
        print(
            # f"Некорректный ответ: {is_incorrect_answer}, "
            f"Запрос: requests.{incorrect_response['http_method'].lower():<9}, "
            f"method: {incorrect_response['send_method']:<9}, "
            f"Результат: код:{incorrect_response['response'].status_code} текст:{incorrect_response['response'].text}")

    print(f"Корректные ответы:")
    for correct_response in correct_responses:
        print(
            # f"Некорректный ответ: {is_incorrect_answer}, "
            f"Запрос: requests.{correct_response['http_method'].lower():<9}, "
            f"method: {correct_response['send_method']:<9}, "
            f"Результат: код:{correct_response['response'].status_code} текст:{correct_response['response'].text}")


if __name__ == "__main__":
    print("П.1 Отправка запроса без method - ожидаем код:200 и текст ошибки Wrong method provided")
    p1("POST")
    print("П.2 Отправка запроса не из списка - ожидаем код:400 и текст ошибки Wrong HTTP method "
          "(для HEAD текст ошибки не ожидаем)")
    p2()
    print("П.3 Отправка запроса не из списка - ожидаем код:200 и текст ответа {\"success\":\"!\"}")
    p3("GET", "GET")
    print("П.4 Запускаем цикл по всем методам для проверки корректности ответа")
    p4()
