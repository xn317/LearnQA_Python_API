class TestShortPhrase:
    def test_short_phrase(self):
        max_len = 15
        phrase = input("Введите фразу диной менее 15 символов: ")
        assert phrase != "", f"Вы не ввели фразу"
        assert len(phrase) < max_len, f"Длина фразы '{phrase}' составляет {max_len} или более символов"
        