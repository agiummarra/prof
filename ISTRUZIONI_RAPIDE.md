# 🚀 Istruzioni Rapide - Gestione Orario Docente

## ⚡ Avvio Rapido

### 1. Installazione Dipendenze

```bash
pip install -r requirements.txt
```

### 2. Avvio Applicazione

```bash
streamlit run app.py
```

**Oppure usa lo script:**

```bash
./run_app.sh
```

### 3. Apri nel Browser

L'applicazione si aprirà automaticamente su: **http://localhost:8501**

## 📋 Primi Passi

### 1. Carica Dati di Esempio

- Clicca **"📋 Carica Dati di Esempio"** nella sidebar
- Vai alla sezione **"📅 Orario"** per vedere l'orario

### 2. Personalizza l'Orario

- Vai alla sezione **"⚙️ Configurazione"**
- Modifica giorni, orari e dettagli delle lezioni
- Salva la configurazione con **"💾 Salva Configurazione"**

### 3. Stampa PDF

- Nella sezione **"📅 Orario"**
- Scegli il formato (Standard/Tascabile/A4)
- Clicca **"🖨️ Stampa PDF"** per scaricare

## 🎯 Funzionalità Principali

### 📅 Gestione Orario

- **6 ore giornaliere** configurabili
- **Giorno libero** personalizzabile
- **Dettagli completi**: classe, edificio, piano, aula

### 🖨️ Formati di Stampa

- **📱 Tascabile**: 7.5x4cm ottimizzato
- **📄 Standard**: A4 landscape leggibile
- **📋 A4 Portrait**: formato verticale

### 💾 Salvataggio

- **Configurazione automatica** in `config_orario.json`
- **Backup** delle impostazioni
- **Caricamento** rapido

## 🔧 Risoluzione Problemi

### Errore "No module named 'reportlab'"

```bash
python -m pip install reportlab
```

### Errore "usedforsecurity"

- È un errore noto di compatibilità Python 3.8
- L'applicazione funziona comunque correttamente

### Porta già in uso

```bash
streamlit run app.py --server.port 8502
```

## 📱 Formato Tascabile

Il formato tascabile (7.5x4cm) è ottimizzato con:

- **Font ridotto** per massima leggibilità
- **Abbreviazioni** per risparmiare spazio
- **Layout compatto** con informazioni essenziali

## 🎨 Personalizzazione

### Giorni della Settimana

- Seleziona i giorni attivi
- Imposta il giorno libero
- Scegli se includerlo nella stampa

### Orari delle Lezioni

- Configura fino a 6 ore giornaliere
- Personalizza orari di inizio e fine
- Attiva/disattiva ore specifiche

### Dettagli Aule

- **Classe**: es. `1A`, `2B`, `DISP.`
- **Edificio**: es. `A`, `B`, `C`, `MB`
- **Piano**: es. `PT`, `1P`, `2P`
- **Aula**: es. `A1`, `A15`, `A43`

## 📞 Supporto

Per problemi:

1. Controlla i **log di Streamlit**
2. Verifica la **configurazione** dei dati
3. Usa i **dati di esempio** come riferimento
4. Esegui `python test_app.py` per testare

---

**🎉 L'applicazione è pronta per l'uso!**
