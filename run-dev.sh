#!/bin/bash

echo "🚀 Запуск в режиме разработки..."

cd docker

# Запускаем с учетом override (автоматически подхватывает override.yml)
sudo docker-compose up --build -d