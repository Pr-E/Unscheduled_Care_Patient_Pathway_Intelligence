#!/bin/bash
set -e

uvicorn src.api.main:app --host 0.0.0.0 --port 8000 &

streamlit run app/home.py \
  --server.address=0.0.0.0 \
  --server.port=8501 \
  --server.headless=true \
  --server.enableCORS=false \
  --server.enableXsrfProtection=false