# Skypro_PD_13.0_Sergey_Levchuk_HW_17

Выполнены все шаги из домашнего задания

    Запрос всех фильмов. При запросе с параметром
    :parameter- `/movies` — возвращает список всех фильмов, разделенный по страницам;
    :parameter- `/movies/<id>` — возвращает подробную информацию о фильме.
    
    Организован поиск по режиссерам и жанрам
    :parameter - /movies/?director_id=1

    выводит список фильмов по ID режиссером
    :parameter - /movies/?genre_id=4

    выводит список всех фильмов по ID жанров
    :parameter - /movies/?director_id=2&genre_id=4
    выводит список фильмов по ID режиссера и жанра

Реализована так же и по режиссерам ШАГ-3

    :parameter- `/directors/` — возвращает всех режиссеров,
    :parameter- `/directors/<id>` — возвращает подробную информацию о режиссере,

    :parameter- `POST /directors/` —  добавляет режиссера,
    :parameter- `PUT /directors/<id>` —  обновляет режиссера,
    :parameter- `DELETE /directors/<id>` —  удаляет режиссера.

Реализована так же и по режиссерам ШАГ-4

    :parameter- `/genres/` —  возвращает все жанры,
    :parameter- `/genres/<id>` — возвращает информацию о жанре с перечислением списка фильмов по жанру,

    :parameter- `POST /genres/` —  добавляет жанр,
    :parameter- `PUT /genres/<id>` —  обновляет жанр,
    :parameter- `DELETE /genres/<id>` —  удаляет жанр.