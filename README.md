# 🎮 Telegram Game Bot – "100 к 1"

> **Автор:** Партач Евгений Васильевич  
> **Email:** jendox1985@gmail.com  
> **Telegram:** [@jendox](https://t.me/jendox)

---

## 📦 Описание проекта

Микросервисное приложение, реализующее игру **"100 к 1"** в Telegram.  
Архитектура построена на взаимодействии между несколькими сервисами через брокер сообщений (RabbitMQ) и REST API.

---

## 🧩 Архитектура

**Сервисы:**

- `poller`: Получает обновления от Telegram API и публикует их в RabbitMQ.
- `bot`: Получает обновления из RabbitMQ, управляет игрой и отправляет ответы пользователям.
- `data_service` (web): API для админки и бота — получение вопросов, сессий и сохранение результатов.
- `postgres`: Хранит историю игр и вопросы.
- `redis`: Хранит активные игровые сессии во время игры.
- `rabbitmq`: Очередь между `poller` и `bot`.

---

## 🚀 Быстрый запуск

```bash
docker-compose -f docker/docker-compose.prod.yml up --build -d
```

---

## Пример shared_docker.env

`DATABASE_URL=postgresql://postgres:postgres@postgres:5432/course_db`  
`RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672/`  
`REDIS_URL=redis://redis:6379`  
`BOT_TOKEN=your_telegram_bot_token`

---

## Применение миграций

```bash
docker-compose -f docker/docker-compose.prod.yml exec web alembic upgrade head
```

---

## Наполнение базы вопросами

```bash
docker-compose -f docker/docker-compose.prod.yml exec -T postgres psql -U postgres -d course_db < data_service/migrations/questions.sql
```

---