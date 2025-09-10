#!/usr/bin/env bash

clear
poetry export --with dev -f requirements.txt --output pub/requirements.txt
docker compose up --remove-orphans --build --force-recreate -d

trap 'echo -e "\nEnter dc stop to stop containers."' SIGINT
docker compose logs -f
