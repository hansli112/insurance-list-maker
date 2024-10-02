#!/bin/bash
docker build -t insurance_list_maker:latest .
docker run --rm -p 8501:8501 insurance_list_maker:latest
