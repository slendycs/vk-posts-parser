# VK Posts Parser

Сервис для парсинга постов из групп и страниц ВКонтакте с использованием VK API. Построен на базе **FastAPI**, поддерживает асинхронную работу и легко разворачивается через Docker.

## 🚀 Возможности

- Парсинг постов из указанной группы или страницы ВКонтакте.
- Асинхронная архитектура на базе `FastAPI` и `asyncio`.
- Готовая конфигурация для запуска в Docker и Docker Compose.
- Встроенная проверка состояния сервиса (Healthcheck).
- Покрытие тестами с использованием `pytest` и поддержкой генерации отчетов через `allure`.

## 📋 Требования

- Python 3.9+
- Docker и Docker Compose *(рекомендуемый способ запуска)*
- Сервисный ключ доступа к VK API (`VK_API_KEY`)

## ⚙️ Конфигурация

Сервис настраивается через переменные окружения. Вы можете создать файл `.env` или передать переменные напрямую в Docker Compose.

| Переменная | Описание | Пример |
|------------|----------|--------|
| `VK_API_KEY` | Сервисный ключ доступа к VK API. Обязательная переменная. | `your_vk_service_key` |
| `VK_GROUP_DOMAIN` | Домен группы или пользователя ВКонтакте, откуда будут парситься посты по умолчанию. | `apiclub` или `durov` |
| `LOG_LEVEL` | Уровень логирования приложения. | `info`, `debug`, `error` |

## 🛠 Установка и запуск

### Способ 1: Docker Compose (Рекомендуется)

1. Склонируйте репозиторий:
   ```bash
   git clone https://github.com/slendycs/vk-posts-parser.git
   cd vk-posts-parser
   ```
2. Отредактируйте `docker-compose.yml`, добавив ваш `VK_API_KEY` и `VK_GROUP_DOMAIN` в секцию `environment`.
3. Запустите сервис:
   ```bash
   docker-compose up -d --build
   ```
   Сервис будет доступен по адресу: http://localhost:7000

### Способ 2: Локальный запуск (для разработки)

1. Создайте и активируйте виртуальное окружение:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Для Linux/macOS
   # или
   venv\Scripts\activate     # Для Windows
   ```
2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
3. Создайте файл `.env` в корневой директории и заполните его:
   ```bash
   VK_API_KEY=ваш_ключ
   VK_GROUP_DOMAIN=ваш_домен
   LOG_LEVEL=debug
   ```
4. Запустите приложение через Uvicorn:
   ```bash
   uvicorn src.main:app --reload --port 7000
   ```

## 📡 Использование API

После запуска интерактивная документация Swagger UI автоматически генерируется и доступна по адресу: http://localhost:7000/

## Основные эндпоинты:

- `GET /api/service/health` - проверка работоспособности сервиса (используется в healthcheck)
- `GET /api/posts` - получение списка постов из указанной группы

## 🧪 Тестирование

Проект использует `pytest` для модульного и интеграционного тестирования.

1. Запуск базовых тестов:
   ```bash
   pytest
   ```
2. Запуск тестов с генерацией отчета Allure:
   ```bash
   pytest --alluredir=allure-results
   allure serve allure-results
   ```

## 📂 Структура проекта

```
.
├── src/
│   ├── client/         # Клиент для взаимодействия с VK API (vk_client.py, vk_errors.py)
│   ├── configs/        # Конфигурации приложения (например, через python-decouple)
│   ├── parser/         # Логика парсинга и структуры данных (data_structures.py, parser.py)
│   ├── routes/         # API роуты (base_api.py, service_api.py)
│   ├── tests/          # Тесты
│   └── main.py         # Точка входа FastAPI приложения
├── docker-compose-example.yml
├── Dockerfile
├── .dockerignore
├── .gitignore
├── requirements.txt
└── pytest.ini
```
