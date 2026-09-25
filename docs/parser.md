# [Парсер](../../backend/parser-service/src/parser/parser.py)

Парсер - набор методов для обработки постов из [JSON ответа от сервера](vk_service.md#api_callmethodstr-paramsdict---dictstr-dict) Вконтакте

## Методы парсинга

### `prepare_post_text(raw_text:str, number_of_characters:int = 15) -> str:`

Метод для обработки текста поста из [JSON ответа от сервера](vk_service.md#api_callmethodstr-paramsdict---dictstr-dict)

Он обрабатывает исходный текст, удаляя из него эмодзи, цензуру и сокращая его до `number_of_characters` символов. Если в посте нет текста, возвращает `''`

#### Параметры

- `raw_text:str`: Исходный текст поста
- `number_of_characters:int`: Количество символов, после которого нужно сократить текст. По умолчанию - `15`

> Все сокращённые символы в тексте заменяются на `...`

#### Примеры работы

```python
raw_text = 'Этот текст явно длиннее пятнадцати символов'
text = prepare_post_text(raw_text)
print(text) # Этот текст явно...
```

```python
raw_text = '[#blur|Хуй|&$!] [#blur|хуй|&$!] да да?' # Именно так Вк цензурит мат
text = prepare_post_text(raw_text)
print(text) # Хуй хуй да да?
```

```python
raw_text = '😒😒😒Папочка🥵🥵🥵' # Простите ради Бога
text = prepare_post_text(raw_text)
print(text) # Папочка
```

### `get_post_url(owner_id:str, id:str, domain:str) -> str`

Подготавливает ссылку на пост

#### Параметры

- `owner_id:str`: ID группы или пользователя где был размещён пост
- `id:str`: ID поста на стене
- `domain:str`: Домен полизователя (или сообщества) Вконтакте

#### Пример работы

```python
    url = get_post_url('123456', '789012', 'durov')
    print(url) # https://vk.com/durov?w=wall123456_789012
```

### `get_first_image(attachments:list[dict]) -> str`

Среди прикреплённых медиа ищет первое изображение и возвращает ссылку на его оригинал. Если видео нет - возвращает `''`

#### Параметры

- `attachments:list[dict]`: Поле `attachments` из [JSON ответа от сервера](vk_service.md#api_callmethodstr-paramsdict---dictstr-dict)

#### Пример работы

```python
json_response = raw_json['response']['items'] # JSON ответ от серверов Вк
item = json_response[0]
attachments = item['attachments']

url = get_first_image(attachments)

print(url) # https://sun9-3.userapi.com/блаблабла
```

### `parse_posts_from_json(self, json_response: list[dict], domain:str, post_text_len:int=70) -> list[Post]`

Метод для парсинга и валидации данных о посте. Возвращает список объектов класса [`Post`](post_structure.md), содержащих в себе информацию о записи со стены

Метод проходится по элементам постов из [JSON ответа от сервера](vk_service.md#api_callmethodstr-paramsdict---dictstr-dict), получает из каждого поле `text`, `orig_photo`, `owner_id` и `id`. После этого формирует список [объектов постов](post_structure.md)

> В качестве фотографии для поста указывается ссылка на первое изображение в посте, если пост не имеет изображений, то ссылка не указывается
>  
>Текст поста при парсинге сокращается до `post_text_len` символов, оставшиеся символы заменяются многоточием

#### Параметры
- `json_response:list[dict]`: поля `items` из поля `response` [JSON ответа от сервера](vk_service.md#api_callmethodstr-paramsdict---dictstr-dict)
- `domain:str` Домен полизователя (или сообщества) Вконтакте, нужен для формирования ссылки на пост
- `post_text_len:int`: Количество символов, после которого нужно сократить текст. По умолчанию - `70`

#### Пример работы

```python
params = {'domain': 'slendycsama'
          'coint': 5}

response = await api_call('wall.get', params)
post_list = parse_posts_from_json(response['response']['items'], 'slendycsama')

for post in post_list:
    print(f'Текст: {post.text}')
    print(f'Изображение: {post.first_image_url}')
    print(f'Ссылка: {post.post_link}')
```


Данный пример демонстрирует [получение от API Вконтакте](vk_service.md#api_callmethodstr-paramsdict---dictstr-dict) списка постов при помощи метода [`wall.get`](https://dev.vk.com/ru/method/wall.get) и его последующего парсинга при помощи `parse_posts_from_json`

Подробнее о структуре `Post` можно узнать [здесь](post_structure.md)