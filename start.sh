#!/bin/bash
echo "🚀 Iniciando frontend com Streamlit..."

PORT=${PORT:-8501}
streamlit run src/login.py --server.port=$PORT --server.address=0.0.0.0
