#!/usr/bin/env bash

APP="pub"
REQUIREMENTS="${APP}/requirements.txt"

function main() {
    pip-compile -o ${REQUIREMENTS} &&
    pip-sync ${REQUIREMENTS} 
}

main;
