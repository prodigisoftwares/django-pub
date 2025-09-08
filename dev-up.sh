#!/usr/bin/env bash

clear
poetry export --with dev -f requirements.txt --output pub/requirements.txt
docker compose up --remove-orphans --build --force-recreate
