#!/bin/bash

echo "🚀 Остановка..."

cd docker

# Запускаем с учетом override (автоматически подхватывает override.yml)
sudo docker-compose down