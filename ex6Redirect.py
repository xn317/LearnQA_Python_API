import requests

request_header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                "AppleWebKit/537.36 (KHTML, like Gecko) "
                                "Chrome/128.0.0.0 "
                                "Safari/537.36"}

response = requests.get('https://playground.learnqa.ru/api/long_redirect', headers=request_header)

for i, redirect in enumerate(response.history, start=1):
    print(f"Редирект {i}: статус:{redirect.status_code}, {redirect.url} -> {redirect.headers.get('location')}")

print(f"Конечная точка: статус {response.status_code}, {response.url}")
