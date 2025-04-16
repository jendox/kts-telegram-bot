#!/bin/bash

echo "💀 Остановка..."

# shellcheck disable=SC2164
cd docker

# Запускаем с учетом override (автоматически подхватывает override.yml)
sudo docker-compose -f docker-compose.yml down