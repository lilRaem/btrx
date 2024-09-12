# ex1:
Вот пример функции на Python, которая будет добавлять и обновлять словари в списке:

```python
def update_dictionary(data_list, new_data):
    # Проверяем, есть ли в списке словарь с таким же ключом и значением
    for i, data in enumerate(data_list):
        if data["id"] == new_data["id"]:
            # Если данные совпадают, просто обновляем значения
            if data == new_data:
                data_list[i] = new_data
            # Если данные не совпадают, обновляем только отличающиеся значения
            else:
                for key, value in new_data.items():
                    if data[key] != value:
                        data[key] = value
            # Завершаем функцию, так как обновление выполнено
            return

    # Если словаря с таким же ключом и значением нет, добавляем новый словарь в список
    data_list.append(new_data)
```

Пример использования функции:

```python
data_list = []  # Здесь будет храниться список словарей

new_data = {
    "id": 20329,
    "katalog": "Здравоохранение/zdravoohranenie",
    "type_zdrav": "ВО",
    "spec": "Повышение квалификации (НМО)",
    "name": "Женское здоровье: ультразвуковая диагностика",
    "fullname": None,
    "price": 39600,
    "hour": 36,
    "nmoSpec": None,
    "linkNmo": None,
    "url": "https://company.ru/katalog/zdravoohranenie/zhenskoe-zdorove-ultrazvukovaya-diagnostika/",
    "final_url": "https://company.ru/katalog/zdravoohranenie/zhenskoe-zdorove-ultrazvukovaya-diagnostika/?program=Женское здоровье: ультразвуковая диагностика&header=Курс НМО Женское здоровье: ультразвуковая диагностика&cost=39600&tovar=20329&sendsay_email=${ Recipient.Email }"
}

update_dictionary(data_list, new_data)
print(data_list)  # Выводим список словарей
```
Вы можете вызывать функцию `update_dictionary` с разными словарями, чтобы добавлять и обновлять данные в списке.

# ex2:

Конечно! Вот еще один пример реализации функции, где словари хранятся в файле в формате JSON. При каждом запуске программы файл считывается, данные загружаются в список, и после обновления список записывается обратно в файл:

```python
import json


def update_dictionary(data_list, new_data):
    for i, data in enumerate(data_list):
        if data["id"] == new_data["id"]:
            if data == new_data:
                data_list[i] = new_data
            else:
                for key, value in new_data.items():
                    if data[key] != value:
                        data[key] = value
            return
    data_list.append(new_data)

def save_data_to_file(file_name, data_list):
    with open(file_name, "w") as file:
        json.dump(data_list, file)

def load_data_from_file(file_name):
    try:
        with open(file_name, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def main():
    file_name = "data.json"
    data_list = load_data_from_file(file_name)

    new_data = {
        "id": 20329,
        "katalog": "Здравоохранение/zdravoohranenie",
        "type_zdrav": "ВО",
        "spec": "Повышение квалификации (НМО)",
        "name": "Женское здоровье: ультразвуковая диагностика",
        "fullname": None,
        "price": 39800,
        "hour": 36,
        "nmoSpec": None,
        "linkNmo": None,
        "url": "https://company.ru/katalog/zdravoohranenie/zhenskoe-zdorove-ultrazvukovaya-diagnostika/",
        "final_url": "https://company.ru/katalog/zdravoohranenie/zhenskoe-zdorove-ultrazvukovaya-diagnostika/?program=Женское здоровье: ультразвуковая диагностика&header=Курс НМО Женское здоровье: ультразвуковая диагностика&cost=39800&tovar=20329&sendsay_email=${ Recipient.Email }"
    }
    update_dictionary(data_list, new_data)
    save_data_to_file(file_name, data_list)

if __name__ == "__main__":
    main()
```
При запуске программы словари из файла "data.json" будут загружены в список `data_list`. Затем новый словарь `new_data` будет добавлен или обновлен в списке с помощью функции `update_dictionary`. Наконец, обновленный список будет сохранен обратно в файл с помощью функции `save_data_to_file`.

# ex3:

Вот пример функции на языке Python, которая сохраняет словарь в список и затем сохраняет список в файл JSON. При последующем запуске функции, она проверяет наличие данных по ключу и значению в словаре и обновляет их, если данные не совпадают:

```python
import json

def update_data(dictionary):
    # Проверяем, есть ли уже данные в файле JSON
    try:
        with open('data.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []   # Если файл не найден, создаем новый пустой список
    # Проверяем, есть ли данные в списке с таким же ключом и значением
    for i, item in enumerate(data):
        if item['id'] == dictionary['id'] and item['name'] == dictionary['name']:
            data[i] = dictionary   # Обновляем данные в списке
            break
    else:
        data.append(dictionary)   # Добавляем данные в список, если запись не найдена
    # Сохраняем список в файл JSON
    with open('data.json', 'w') as f:
        json.dump(data, f)

# Пример использования функции
example_dict = {
    "id": 20329,
    "katalog": "Здравоохранение/zdravoohranenie",
    "type_zdrav": "ВО",
    "spec": "Повышение квалификации (НМО)",
    "name": "Женское здоровье: ультразвуковая диагностика",
    "fullname": None,
    "price": 39600,
    "hour": 36,
    "nmoSpec": None,
    "linkNmo": None,
    "url": "https://company.ru/katalog/zdravoohranenie/zhenskoe-zdorove-ultrazvukovaya-diagnostika/",
    "final_url": "https://company.ru/katalog/zdravoohranenie/zhenskoe-zdorove-ultrazvukovaya-diagnostika/?program=Женское здоровье: ультразвуковая диагностика&header=Курс НМО Женское здоровье: ультразвуковая диагностика&cost=39600&tovar=20329&sendsay_email=${Recipient.Email}"
}
update_data(example_dict)
```
Этот пример сохраняет словарь в файл JSON с именем "data.json". При каждом запуске функции, данные обновляются или добавляются в файле, если они не совпадают с уже существующими записями.