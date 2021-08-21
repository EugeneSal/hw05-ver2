hw05_final ver 2.0
Доработтаный учебный проект hw05_final
***
Возможности стандартные:
* создание постов с картинками
* комментирование постов
* подписка на автора поста

Возможности расширенные:
* создание профиля с аватаркой
* изменение профиля
* удаление своего поста
* удаление своего комментария к постам любых авторов
* удаление комментарие любых авторов к своим постам
* отображение количества просмотров поста
* отображение количества зарегистрированных пользователей 
* создание групп

Подключен АПИ, возможности:
* создание поста
* комментирование поста
* подписка на автора
* авторизания по токену JWTAuthentication

***
Как запустить проект:
```
git clone https://github.com/EugeneSal/.git
```
Cоздать и активировать виртуальное окружение:
```
python -m venv env

source venv/bin/activate
```
обновить pip
```
python -m pip install --upgrade pip
```
Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
Выполнить миграции:
```
python manage.py migrate
```
Запустить сервер:
```
python manage.py runserver
```
Ссылка на локальный сервер:
http://127.0.0.1:8000/

Документация доступна по адресу:
http://127.0.0.1:8000/redoc/
***
Пример работы API:

Запрос для создания поста:
```python
import requests
url = 'http://127.0.0.1:8000/api/v1/posts/'
TOKEN = 'Тут ваш токен'

data = {
  "text": "Здесь ваш текст",
}
headers = {'Authorization': f'Bearer {TOKEN}'}
request = requests.post(url, headers=headers, data=data)
```
Ответ от API:
```json
{
    "author": "string",
    "group": "None",
    "id": 1,
    "image": "None",
    "pub_date": "2021-08-17T02:37:42.283465Z",
    "text": "Здесь ваш текст"
}
```
***
