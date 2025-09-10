#!/usr/bin/env bash

clear
poetry export --with dev -f requirements.txt --output requirements.txt
cp requirements.txt pub/requirements.txt
docker compose -f docker-compose.prod.yml down -v
docker compose -f docker-compose.prod.yml up --remove-orphans --build --force-recreate -d

# trap 'echo -e "\nEnter dc stop to stop containers."' SIGINT
# docker compose logs -f
