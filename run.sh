#!/bin/bash
docker pull hansli112/insurance-list-maker
docker run \
    --rm \
    -p 8501:8501 \
    --mount type=bind,source=./database.csv,target=/insurance-list-maker/database.csv \
    insurance-list-maker
