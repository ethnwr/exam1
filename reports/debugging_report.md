# Отчёт об отладке кода
## Система «Книжный интернет-магазин»

Дата: 18.06.2026
Разработчик: [твоё имя]

---

## Ошибка №1. FileNotFoundError при загрузке каталога

### Описание ошибки
При запуске `main.py` из корня проекта программа падала с ошибкой:
FileNotFoundError: [Errno 2] No such file or directory: 'data/products.json'
Причина: в `catalog.py` путь к файлу был прописан как `data/products.json`, но при запуске из `src/main.py` рабочая директория — `src/`, и Python искал `src/data/products.json`.

### Как обнаружил
Запустил программу — увидел трейс ошибки в консоли. Поставил точку останова на строке `with open(DATA_FILE, 'r')` и увидел в переменной `DATA_FILE` значение `'data/products.json'`, которое не совпадало с реальным расположением.

### Решение
Изменил путь на абсолютный относительно расположения модуля:
```python
DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'products.json')