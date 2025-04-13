#!/bin/bash

echo "🚀 Запуск в режиме разработки..."

# shellcheck disable=SC2164
cd docker

# Запускаем с учетом override (автоматически подхватывает override.yml)
sudo docker-compose up --build -d