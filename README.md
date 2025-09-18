# 📚 Gestione Orario Docente - Web App Streamlit

Una web application per la gestione dell'orario di una docente di matematica e fisica di un liceo scientifico.

## 🚀 Funzionalità

### 📅 Gestione Orario

- **Visualizzazione orario settimanale** con layout stampabile
- **Configurazione flessibile** di giorni, orari e aule
- **Formati di stampa multipli**:
  - Standard (A4 landscape)
  - Tascabile (7.5x4cm - A7 landscape)
  - A4 portrait

### ⚙️ Configurazione

- **Giorni della settimana** personalizzabili
- **Giorno libero** configurabile con opzione di inclusione/esclusione
- **Orari delle lezioni** (max 6 ore giornaliere)
- **Dettagli aule**: edificio, piano, numero aula
- **Salvataggio/caricamento** configurazioni

### 🖨️ Stampa

- **PDF ottimizzati** per diversi formati
- **Formato tascabile** con abbreviazioni per risparmiare spazio
- **Layout responsive** e stampabile

## 📦 Installazione

1. **Clona o scarica** il progetto
2. **Installa le dipendenze**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Avvia l'applicazione**:
   ```bash
   streamlit run app.py
   ```

## 🎯 Utilizzo

### Prima Configurazione

1. **Carica dati di esempio** usando il pulsante nella sidebar
2. **Personalizza** giorni e orari nella sezione "Configurazione"
3. **Modifica** i dettagli delle lezioni per ogni giorno
4. **Salva** la configurazione per uso futuro

### Gestione Orario

1. **Visualizza** l'orario nella sezione "Orario"
2. **Scegli** il formato di visualizzazione (Standard/Compatto/Tascabile)
3. **Stampa** in PDF usando i pulsanti dedicati

### Formati di Stampa

#### 📱 Tascabile (7.5x4cm)

- Ottimizzato per stampa in formato tascabile
- Abbreviazioni per risparmiare spazio
- Layout compatto con informazioni essenziali

#### 📄 Standard (A4 Landscape)

- Formato leggibile con dettagli completi
- Ideale per consultazione quotidiana
- Layout spazioso e chiaro

#### 📋 A4 Portrait

- Formato verticale per documentazione
- Adatto per archiviazione

## 🔧 Struttura Dati

L'orario è strutturato come:

```
Giorno -> Ora -> {classe, edificio, piano, aula}
```

### Esempi di Inserimento

- **Classe**: `1A`, `2B`, `DISP.`, `—`
- **Edificio**: `A`, `B`, `C`, `MB`, `MA`
- **Piano**: `PT`, `1P`, `2P`, `3P`
- **Aula**: `A1`, `A15`, `A43`

## 💾 Salvataggio

- **Configurazione automatica** in `config_orario.json`
- **Backup** delle impostazioni personalizzate
- **Caricamento** rapido di configurazioni salvate

## 🎨 Personalizzazione

L'applicazione supporta:

- **Giorni personalizzati** (es. solo lunedì-venerdì)
- **Orari flessibili** (es. 5 ore invece di 6)
- **Giorno libero** configurabile
- **Formati di stampa** multipli

## 📱 Responsive Design

L'interfaccia si adatta a:

- **Desktop** (layout completo)
- **Tablet** (layout ottimizzato)
- **Mobile** (layout compatto)

## 🔄 Aggiornamenti

Per aggiornare l'applicazione:

1. **Salva** la configurazione corrente
2. **Sostituisci** i file dell'applicazione
3. **Carica** la configurazione salvata

## 🆘 Supporto

Per problemi o suggerimenti:

- Controlla i **log di Streamlit** per errori
- Verifica la **configurazione** dei dati
- Usa i **dati di esempio** come riferimento

---

**Sviluppato per docenti di matematica e fisica** 📐⚗️
