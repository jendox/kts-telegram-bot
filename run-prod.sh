#!/bin/bash

echo "🚀 Запуск в продакшн-режиме..."

# shellcheck disable=SC2164
cd docker

# Явно отключаем override
sudo docker-compose -f docker-compose.yml up --build -d