# Работа с API Вконтакте

Работа с API Вконтакте заключается во взаимодействии с классом [`VKClient`](../../backend/parser-service/src/client/vk_client.py), ключающим в себя асинхронные методы, выполняющие POST-запросы к API Вконтакте и возвращающих от них ответ

## Поля [`VKClient`](../../backend/parser-service/src/client/vk_client.py)

Класс `VKClient` в ключает в себя такие поля как:

- `base_url:str`: URL адрес к API Вконтакте, по умолчанию - `https://api.vk.ru method/`
- `api_version:str`: Версия API Вконтакте, по умолчанию - `5.199`
- `token:str`: Сервисный токен доступа к API Вконтакте, берётся из `.env` файла. Токен доступа можно получить на этом [сайте](https://vkhost.github.io/)

## Методы [`VKClient`](../../backend/parser-service/src/client/vk_client.py)

### `api_call(method:str, params:dict) -> dict[str, dict]`

Базовый метод для работы с API Вконтакте. Возвращает JSON ответ от серверов VK. 

В случае ошибки метод генерирует исключение [`APICallError`](../../backend/parser-service/src/client/vk_errors.py)

#### Параметры

- `method:str`: Название VK API метода, например: [`wall.get`](https://dev.vk.com/ru/method/wall.get)
- `params:dict`: Словарь параметров метода

#### Пример работы

```python
params = {'domain': 'club283993',
          'count': 3}

response = await self.__api_call(method='wall.get', params=params)
print(response.get('response').get('items'))
```


Данные пример демонстрирует выполнение запроса к методу [`wall.get`](https://dev.vk.com/ru/method/wall.get) API Вконтакте. В качестве параметров указывается имя домена страницы ВК и количество постов, которые необходимо получить

В качестве ответа `api_call()` возвращает словарь с полями из JSON ответа от серверов


### `get_posts(self, domain:str, count:int, post_text_len:int) -> list[Post]`

Метод для получения постов со стены сообщества/пользователя Вконтакте.

Работает как обёртка над базовым методом [`api_call`](#api_callmethodstr-paramsdict---dictstr-dict), передавая ему необходимые параметры запроса для получения постов со стены и передавая его результат [парсеру](./parser.md). Возвращает список записей [постов](./post_structure.md). 

В случае ошибки:
- Если ошибка связана с запросом - генерирует исключение [`APICallError`](../../backend/parser-service/src/client/vk_errors.py)
- Если в ответе нет элементов - генерирует исключение [`NoItemsError`](../../backend/parser-service/src/client/vk_errors.py)

#### Параметры

- `domain:str`: Короткий адрес пользователя или сообщества
- `count:int`: Количество записей, которое необходимо получить. Максимальное значение: `100`
- `post_text_len:int`: Количество символов до которого нужно сократить текст

#### Пример работы

```python
client = VKClient()
response = await client.get_posts(domain='domain', 
                                  count=3, 
                                  post_text_len=70)
for post in response:
    print(f'Текст: {post.text}')
    print(f'Изображение: {post.first_image_url}')
    print(f'Ссылка: {post.post_link}')
```
