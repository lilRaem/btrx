# Программа для генерации и парсинга товаров, ссылок company.ru
Помогает держать базу данных и данные на сайте в порядке находя дубликаты или неверные названия/цены

В проекте используется работа с BitrixAPI, BeautifulSoup, Selenium + Автоустановщик драйвера.

Pydantic чтобы типизировать данные т.к. их тут много

Много работы с JSON файлами и генерации HTML шаблонов


[Основная бибилиотека](docs/MainReadme.md)
# TODO
- [ ] Перевести все print'ы в логи с сохранением в файл
- [ ] Добавить запоминание похожих данных (cache)
- [ ] Сделать поиск по фильтру на сайте

      `https://company.ru/katalog/ajax/filter/` и  `https://company.ru/katalog/ajax/`

# TODO что необходимо во время работы

- [x] подставлять id товара автоматически
- [x] Поиск товара автоматически
- [?] Добавить колличество программ в название файла
- [x] Во временно tmpfile.json ищет по словам которых по факту в программе нет (теперь все работает)
- [x] поиск по словам и цене работает не корректно
- [x] сделать списки более универсальными (чтобы была ссылка нмо и id)
- [ ] скопировать таблицы из pdf (https://medium.com/@winston.smith.spb/python-an-easy-way-to-extract-data-from-pdf-tables-c8de22308341, https://github.com/jsvine/pdfplumber)
- [x] Создание многоуровнего json: https://stackoverflow.com/a/49957442

# TODO Что нужно сделать:

Разбросать важные функции по отдельным модулям python (отдельно выгрузка с битрикс, отдельно генератор шаблона, отдельно поиск и сравнение элементов)
Отдельным файлом:

- [x] выгрузка с битрикс
- [x] генератор шаблона
- [x] поиск и сравнение c таблицами
- [x] парсинг документов pdf, docx, csv, xlsx
- [x] производить поиск по сайту через python

# TODO Сделать тесты:

- [?] main.py
- [?] parserdocx.py
- [x] btrx.py
- [ ] parserdocx2table.py
- [x] parserhtml.py

# TODO Что минимально нужно чтобы получить id товара?
- [x] Имя программы, цена
