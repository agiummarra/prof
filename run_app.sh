#!/bin/bash

# Script per avviare l'applicazione Gestione Orario Docente

echo "📚 Avvio Gestione Orario Docente..."
echo "=================================="

# Verifica se streamlit è installato
if ! command -v streamlit &> /dev/null; then
    echo "❌ Streamlit non trovato. Installazione delle dipendenze..."
    pip install -r requirements.txt
fi

# Avvia l'applicazione
echo "🚀 Avvio dell'applicazione..."
streamlit run app.py --server.port 8501 --server.address localhost

echo "✅ Applicazione avviata su http://localhost:8501"
