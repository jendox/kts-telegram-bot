#!/bin/bash

echo "🚀 Запуск в продакшн-режиме..."

cd docker

# Явно отключаем override
sudo docker-compose -f docker-compose.yml up --build -d