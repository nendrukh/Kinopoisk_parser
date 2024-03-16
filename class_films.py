class Films:
    """
    Класс, который хранит в себе информацию о всех фильмах.
    """
    def __init__(self) -> None:
        self.films = dict()

    def added_film(self, film_name: str, genre: str, author: str, link: str) -> None:
        """
        Функция для добавления информации о фильме в класс.
        Добавляется информация о фильме, а также прибавляется 1 к общему кол-ву фильмов.
        Args:
            film_name (str): Название фильма
            genre (str): Жанр
            author (str): Режиссёр
            link (str): Ссылка на фильм в Кинопоиске
        """
        self.films[film_name] = {
            "genre": genre,
            "author": author,
            "link": link
        }
