## Парсер лучших фильмов Кинопоиска ##

---

### Что может скрипт ###
Скрипт парсит [сайт](https://www.kinopoisk.ru/lists/movies/top250/) Кинопоиска с 250 лучшими непросмотренными вашими фильмами.
Затем можно либо выгрузить фильмы в виде таблички в экселе, либо выбрать по жанру случайный фильм на вечер c ссылкой на него.

### Запуск ###
* Клонируйте репозиторий себе:
```
git clone https://github.com/nendrukh/Kinopoisk_parser.git
```

* Cоздайте виртуальное окружение venv
```commandline
python3 -m venv venv
```

* Установите необходимые пакеты командой:
```commandline
pip install -r requirements.txt
```

* Создайте файл .env

* В файле .env укажите переменную COOKIE=... со своими cookie при заходе на [сайт](https://www.kinopoisk.ru/lists/movies/top250/)
будучи авторизованными: Netwrok - Headers - Cookie

* В файле .env ещё укажите переменную USER_AGENT=... со страницы: Netwrok - Headers - User-Agent

* Запустите main.py