import random
import re
from config import COOKIE, USER_AGENT
from typing import Tuple

import requests
import pandas as pd
from requests import Response
from bs4 import BeautifulSoup, PageElement


def start_kinopoisk_parser() -> None:
    """
    Функция обращается к страницам сайта с помощью запроса GET 5 раз, так как на сайте именно 5 страниц с фильмами.
    С результатом запроса запускаем функцию-парсер.
    """
    choice: int = ask_user()
    films = dict()
    headers = {
        "Cookie": COOKIE,
        "User-Agent": USER_AGENT
    }

    for page in range(1, 6):
        kinopoisk_response: Response = requests.get(
            f"https://www.kinopoisk.ru/lists/movies/top250/?utm_referrer=www.kinopoisk.ru&page={page}",
            headers=headers
        )
        parser_website(kinopoisk_response, films)

    if choice == 1:
        upload_movie_excel(films)
    else:
        get_random_film(films)


def ask_user() -> int:
    """
    Функция для предоставления выбора. Если пользователь хочет выгрузить фильмы в эксель, то надо ввести 1.
    Если хочет получить просто случайный фильм, то надо ввести 2.
    :return: Выбор пользователя int 1 or 2
    """
    while True:
        choice = input("\nЧто сделаем?"
                       "\n1 - Выгрузить неоцененные фильмы в экселе;"
                       "\n2 - Выдать случайный фильм по жанру.\n")

        if choice.isalpha():
            print("Нужно ввести число!")
        elif int(choice) > 2 or int(choice) < 1:
            print("Нужно ввести число из предложенных!")
        else:
            break

    return int(choice)


def parser_website(response: Response, films: dict) -> None:
    """
    Функция-парсер. Находим все фильмы на странице и проходимся по ним циклом.
    Если на фильме нет оценки, значит фильм не просмотрен, собираем по нему информацию и добавляем в словарь.
    :param response:(Response) Ответ от сервера
    :param films:(dict) Словарь с фильмами
    """
    text_response: str = response.text
    soup = BeautifulSoup(text_response, "html.parser")
    all_films = soup.find_all("div", class_="styles_root__ti07r")

    for film in all_films:
        if film.find("i", "styles_star__R6DQ_ styles_controls__X1G1t"):
            film_name, link, genre, author = take_info_about_film(film)
            added_film(films, film_name, genre, author, link)


def take_info_about_film(film: PageElement) -> Tuple[str, str, str, str]:
    """
    Достаем информацию о непросмотренном фильме.
    :param film:(PageElement) Непросмотренный фильм из html страницы сайта
    :return: Название фильма, ссылку на фильм, жанр фильма и режиссёр
    """
    try:
        film_name = film.find("div", "base-movie-main-info_mainInfo__ZL_u3").string
    except TypeError:
        raise TypeError

    genre_and_author = film.find("div", "desktop-list-main-info_additionalInfo__Hqzof").string
    genre_and_author = re.sub("\xa0\xa0", ". ", genre_and_author)

    url_film = film.find("a", "base-movie-main-info_link__YwtP1")["href"]

    link = "https://www.kinopoisk.ru" + url_film
    genre = re.search(r"\b\w+\.", genre_and_author).group()
    genre = genre[:-1]  # убираем точку в конце
    author = re.search(r"\b[А-ЯЁ]\w+[\s\-][а-яА-ЯЁ]\w+[\s\-]?([А-ЯЁ]\w+)?\b", genre_and_author).group()

    return film_name, link, genre, author


def added_film(films: dict, film_name: str, genre: str, author: str, link: str) -> None:
    """
    Добавление фильма со всей необходимой о нем информацией в словарь с фильмами
    :param films:(dict) Словарь с непросмотренными фильмами и с их информацией.
    :param film_name:(str) Название фильма
    :param genre:(str) Жанр фильма
    :param author:(str) Режиссёр фильма
    :param link:(str) Ссылка на страницу фильма
    """
    films[film_name] = {
        "genre": genre,
        "author": author,
        "link": link
    }


def upload_movie_excel(films: dict) -> None:
    """
    Загрузка фильмов в эксель.
    Выгружаем все фильмы с их параметрами в отдельные списки list и записываем в data frame
    :param films:(dict) Словарь всех непросмотренных фильмов
    """
    films_name = films.keys()
    genres = [film.get("genre") for film in films.values()]
    authors = [film.get("author") for film in films.values()]
    links = [film.get("link") for film in films.values()]

    data_frame = pd.DataFrame({
        "Фильм": films_name,
        "Жанр": genres,
        "Режиссёр": authors,
        "Ссылка": links
    })
    data_frame.to_excel("films.xlsx", sheet_name="Фильмы", index=False)
    print("Файл эксель загружен в текущую директиву")


def get_random_film(films: dict) -> None:
    """
    Отдаем пользователю случайный непросмотренный фильм.
    Предаврительно собираем все жанры из непросмотренных фильмов
    и отдаем их список пользователю, чтобы выбрал, написав название
    :param films:(dict) Словарь всех непросмотренных фильмов
    """
    all_genres = set([film.get("genre") for film in films.values()])
    print(f"\nНапиши жанр фильма из доступных по твоим непросмотренным фильмам: \n{', '.join(all_genres)}")

    while True:
        selected_genres = input()
        if selected_genres in all_genres:
            break
        else:
            print("\nНаписать жанр надо в точности как указано!")

    all_films_by_selected_genre = [film for film in films.items() if film[1].get("genre") == selected_genres]
    random_film = random.choice(all_films_by_selected_genre)

    print(f'\nСлучайный фильм к просмотру "{random_film[0]}" с жанром {random_film[1].get("genre")} '
          f'от автора {random_film[1].get("author")}.\nСсылка на фильм: {random_film[1].get("link")}')


if __name__ == "__main__":
    start_kinopoisk_parser()
