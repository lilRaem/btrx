## fast_bitrix24

[fast_bitrix24](https://github.com/leshchenko1979/fast_bitrix24 "fast_bitrix24") - API wrapper для Питона для быстрого получения данных от Битрикс24 через REST API.

#### Как используется в проекте?

##### Расположение файла методов:

[module/btrx.py](module/btrx.py)

##### Методы:

###### save_to_json(datalist, filename, path):

> Сохраняет `datalist` по пути `path` c именем `filename`:`/data/json/btrx_data/XX.XX.XX_file.json`
> возвращает преобразованный в json **list(`datalist`)**

###### load_from_jsonFile(filename, path):

> Загружает файл по имени `filename` и путь `path`: `/data/json/btrx_data/XX.XX.XX_file.json` 
> возвращает преобразованный в  json **list(`data_from_file`)**

###### get_product_list(btrx):

> Наследует класс `Bitrix` с webhook'ом
> Загружает список товаров с полями: 
> `<span style='color: magenta;'>id</span>, <span style='color: yellow;'>name</span>, <span style='color: lightgreen;'>price</span>, <span style='color: lightblue;'>hour</span>`
> возвращает **list(products)**

###### get_users_with_innerPhone(btrx):

> Наследует класс `Bitrix` с webhook'ом
> Загружает список пользователей со всеми полями
> возвращает **list(users)**

###### set_product_price(btrx,id,price):

> Наследует класс `Bitrix` с webhook'ом
> обновлят поле `price` по `id`

###### get_all_data(data):

> Принимает list `data` из `get_product_list(btrx)` и преобразует данные в  json-формат
> возвращает **list(datalist)**

---

## Pydantic

[Pydantic](https://pydantic-docs.helpmanual.io/ "Pydantic") - работа с JSON данными

---

## Colorama

[Colorama](https://github.com/tartley/colorama) - Оформление текста в терминале


4. [Requests](https://github.com/psf/requests) - Веб запросы и отправка