import json


def get_message_text(json_txt, message_number):
    try:
        obj = json.loads(json_txt)
    except json.JSONDecodeError:
        return "ОШИБКА! Не удалось прочитать JSON"

    if "messages" not in obj:
        return "ОШИБКА! В JSON отсутствует объект messages"

    if message_number-1 not in range(len(obj['messages'])):
        return f"ОШИБКА! Отсутствует сообщение под номером {message_number}"

    if "message" not in obj['messages'][message_number-1]:
        return f"ОШИБКА! Отсутствует текст сообщения под номером {message_number}"

    return obj['messages'][message_number - 1]['message']


if __name__ == "__main__":
    json_text = """{"messages":[
                     {"message":"This is the first message","timestamp":"2021-06-04 16:40:53"}
                    ,{"message":"And this is a second message","timestamp":"2021-06-04 16:41:01"}
                    ]}"""

    message_text = get_message_text(json_text, 2)
    print(message_text)
