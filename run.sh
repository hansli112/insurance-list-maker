#!/bin/bash
docker pull hansli112/insurance-list-maker
docker run --rm -p 8501:8501 hansli112/insurance-list-maker
