#!/bin/sh

set -e

echo "========================================"
echo "Starting SAP RAG Platform"
echo "========================================"

echo ""
echo "1. Running database migrations..."
alembic upgrade head

echo ""
echo "Database migrations completed."

echo ""
echo "2. Synchronizing SAP base corpus..."
python -m scripts.sync_sap_corpus

echo ""
echo "SAP corpus synchronization completed."

echo ""
echo "3. Starting Streamlit..."

exec streamlit run streamlit_app.py \
    --server.address=0.0.0.0 \
    --server.port=8501