import requests
import json
import time
import datetime

url = 'https://playground.learnqa.ru/ajax/api/longtime_job'


class LongTimeJob:
    def __init__(self, token=None):
        self.status = None
        self.error = None
        self.result = None
        response = requests.get(url)
        try:
            self.token = response.json()['token']
            self.seconds = response.json()['seconds']
        except json.JSONDecodeError:
            self.token = None
            self.seconds = None
            print(f"Ошибка чтения JSON при создании задачи")
            exit(0)
        self.creation_time = datetime.datetime.now()
        self.time_to_complete = self.creation_time + datetime.timedelta(seconds=self.seconds)

    def info(self):
        print(f"Token = {self.token}; "
              f"Seconds = {self.seconds}; "
              f"Status = {self.status}; "
              f"Result = {self.result}; "
              f"Error = {self.error}; ")

    def get_status(self):
        response = requests.get(url, params={"token": self.token})
        try:
            json_status = response.json()
        except json.JSONDecodeError:
            print(f"Ошибка чтения JSON при запросе статуса")
            return -1
        if "result" in json_status:
            self.result = json_status["result"]
        if "status" in json_status:
            self.status = json_status["status"]
        elif "error" in json_status:
            self.error = json_status["error"]
        else:
            print(f"Ошибка получения статуса")
            return -1
        return 0

    def do_job(self):
        print(f"Запуск выполнения задачи созданной {self.creation_time.strftime("%m/%d/%Y, %H:%M:%S")}")
        print(f"Текущие параметры задачи:")
        self.info()
        print(f"Получаем статус:")
        self.get_status()
        self.info()
        if self.time_to_complete > datetime.datetime.now():
            wait_time = round((self.time_to_complete - datetime.datetime.now()).total_seconds())
            print(f"Время до завершения задачи {wait_time} секунд, ожидаем...")
            time.sleep(wait_time)
        print(f"Задача уже должна быть выполнена - проверяем")
        self.get_status()
        self.info()
        if self.status == "Job is ready" and self.result == "42":
            print(f"Задача успешно выполнена!")
        else:
            print(f"Задача не выполнена после запланированного времени. Что-то идет не так...")


if __name__ == "__main__":
    x = LongTimeJob()
    x.do_job()
