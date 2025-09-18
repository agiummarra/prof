import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os
from reportlab.lib.pagesizes import landscape, A7, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import io

# Costanti
ISTITUTO_DEFAULT = 'Liceo Scientifico "E. Fermi" Ragusa'

# Configurazione della pagina
st.set_page_config(
    page_title="Gestione Orario Docente",
    page_icon="📚",
    layout="wide"
)

# Funzione per caricare configurazione salvata
def load_saved_config():
    """Carica la configurazione salvata se esiste"""
    try:
        if os.path.exists('config_orario.json'):
            with open('config_orario.json', 'r') as f:
                return json.load(f)
    except Exception as e:
        st.error(f"Errore nel caricamento della configurazione: {str(e)}")
    return None

# Inizializzazione session state
if 'schedule_data' not in st.session_state:
    # Prova a caricare configurazione salvata
    saved_config = load_saved_config()
    
    if saved_config:
        st.session_state.schedule_data = saved_config
        # Non mostrare il messaggio qui per evitare spam
    else:
        # Configurazione di default
        st.session_state.schedule_data = {
            'docente': 'Cristina Bellina Terra',
            'materie': 'Matematica e Fisica',
            'istituto': ISTITUTO_DEFAULT,
            'anno_scolastico': '2025/2026',
            'giorni_settimana': ['LUN', 'MAR', 'MER', 'GIO', 'VEN', 'SAB'],
            'giorno_libero': 'DOM',
            'include_giorno_libero': False,
            'ore_giornaliere': 6,
            'ore_attive': [1, 2, 3, 4, 5, 6],
            'orari': {
                '1': {'dalle': '08:15', 'alle': '09:15'},
                '2': {'dalle': '09:15', 'alle': '10:15'},
                '3': {'dalle': '10:15', 'alle': '11:15'},
                '4': {'dalle': '11:15', 'alle': '12:15'},
                '5': {'dalle': '12:15', 'alle': '13:15'},
                '6': {'dalle': '13:15', 'alle': '14:15'}
            },
            'schedule': {}
        }

# Funzione per caricare dati di esempio
def load_example_data():
    example_schedule = {
        'LUN': {
            '1': {'classe': '', 'edificio': '', 'piano': '', 'aula': ''},
            '2': {'classe': '', 'edificio': '', 'piano': '', 'aula': ''},
            '3': {'classe': '2Esa', 'edificio': 'MB', 'piano': 'PT', 'aula': 'A15'},
            '4': {'classe': '1Dsa', 'edificio': 'MA', 'piano': 'PT', 'aula': 'A1'},
            '5': {'classe': '', 'edificio': '', 'piano': '', 'aula': ''},
            '6': {'classe': '', 'edificio': '', 'piano': '', 'aula': ''}
        },
        'MAR': {
            '1': {'classe': 'DISP.', 'edificio': '', 'piano': '', 'aula': ''},
            '2': {'classe': 'DISP.', 'edificio': '', 'piano': '', 'aula': ''},
            '3': {'classe': 'DISP.', 'edificio': '', 'piano': '', 'aula': ''},
            '4': {'classe': 'DISP.', 'edificio': '', 'piano': '', 'aula': ''},
            '5': {'classe': 'DISP.', 'edificio': '', 'piano': '', 'aula': ''},
            '6': {'classe': 'DISP.', 'edificio': '', 'piano': '', 'aula': ''}
        },
        'MER': {
            '1': {'classe': '1Asp', 'edificio': 'C', 'piano': '1P', 'aula': 'A43'},
            '2': {'classe': '1Asp', 'edificio': 'C', 'piano': '1P', 'aula': 'A43'},
            '3': {'classe': 'DISP.', 'edificio': '', 'piano': '', 'aula': ''},
            '4': {'classe': '', 'edificio': '', 'piano': '', 'aula': ''},
            '5': {'classe': '', 'edificio': '', 'piano': '', 'aula': ''},
            '6': {'classe': '', 'edificio': '', 'piano': '', 'aula': ''}
        },
        'GIO': {
            '1': {'classe': '1Bsa', 'edificio': 'MB', 'piano': 'PT', 'aula': 'A16'},
            '2': {'classe': '—', 'edificio': '', 'piano': '', 'aula': ''},
            '3': {'classe': '1Asp', 'edificio': 'C', 'piano': '1P', 'aula': 'A43'},
            '4': {'classe': '1Asp', 'edificio': 'C', 'piano': '1P', 'aula': 'A43'},
            '5': {'classe': '1Asa', 'edificio': 'MA', 'piano': '2P', 'aula': 'A20'},
            '6': {'classe': '', 'edificio': '', 'piano': '', 'aula': ''}
        },
        'VEN': {
            '1': {'classe': '1Dsa', 'edificio': 'MA', 'piano': 'PT', 'aula': 'A1'},
            '2': {'classe': 'DISP.', 'edificio': '', 'piano': '', 'aula': ''},
            '3': {'classe': '2Esa', 'edificio': 'MB', 'piano': 'PT', 'aula': 'A15'},
            '4': {'classe': '1Asp', 'edificio': 'C', 'piano': '1P', 'aula': 'A43'},
            '5': {'classe': '1Asp', 'edificio': 'C', 'piano': '1P', 'aula': 'A43'},
            '6': {'classe': '', 'edificio': '', 'piano': '', 'aula': ''}
        },
        'SAB': {
            '1': {'classe': '1Asp', 'edificio': 'C', 'piano': '1P', 'aula': 'A43'},
            '2': {'classe': 'DISP.', 'edificio': '', 'piano': '', 'aula': ''},
            '3': {'classe': '1Bsa', 'edificio': 'MB', 'piano': 'PT', 'aula': 'A13'},
            '4': {'classe': '1Asa', 'edificio': 'MA', 'piano': '2P', 'aula': 'A20'},
            '5': {'classe': '', 'edificio': '', 'piano': '', 'aula': ''},
            '6': {'classe': '', 'edificio': '', 'piano': '', 'aula': ''}
        }
    }
    
    # Aggiorna anche i campi docente, materie e istituto
    st.session_state.schedule_data['docente'] = 'Cristina Bellina Terra'
    st.session_state.schedule_data['materie'] = 'Matematica e Fisica'
    st.session_state.schedule_data['istituto'] = ISTITUTO_DEFAULT
    
    st.session_state.schedule_data['schedule'] = example_schedule

# Sidebar
st.sidebar.title("📚 Gestione Orario Docente")
st.sidebar.markdown("---")

# Menu di navigazione
menu_options = {
    "🏠 Home": "home",
    "📅 Orario": "orario",
    "⚙️ Configurazione": "configurazione"
}

selected_page = st.sidebar.selectbox("Seleziona pagina", list(menu_options.keys()))
page = menu_options[selected_page]

# Pulsante per caricare dati di esempio
if st.sidebar.button("📋 Carica Dati di Esempio"):
    load_example_data()
    st.sidebar.success("Dati di esempio caricati!")

# Pulsante per salvare configurazione
if st.sidebar.button("💾 Salva Configurazione"):
    with open('config_orario.json', 'w') as f:
        json.dump(st.session_state.schedule_data, f, indent=2)
    st.sidebar.success("Configurazione salvata!")

# Pulsante per ricaricare configurazione
if st.sidebar.button("🔄 Ricarica Configurazione"):
    saved_config = load_saved_config()
    if saved_config:
        st.session_state.schedule_data = saved_config
        st.sidebar.success("✅ Configurazione ricaricata!")
        st.rerun()  # Ricarica la pagina per aggiornare l'interfaccia
    else:
        st.sidebar.error("❌ Nessuna configurazione trovata!")

st.sidebar.markdown("---")

# Indicatore configurazione
if os.path.exists('config_orario.json'):
    st.sidebar.success("💾 Configurazione salvata disponibile")
    # Mostra se è stata caricata automaticamente
    if 'config_loaded' not in st.session_state:
        st.session_state.config_loaded = True
        st.sidebar.info("✅ Configurazione caricata automaticamente")
else:
    st.sidebar.info("💾 Nessuna configurazione salvata")

st.sidebar.markdown(f"**Docente:** {st.session_state.schedule_data.get('docente', 'Cristina Bellina Terra')}")
st.sidebar.markdown(f"**Materie:** {st.session_state.schedule_data.get('materie', 'Matematica e Fisica')}")
st.sidebar.markdown(f"**Istituto:** {st.session_state.schedule_data.get('istituto', ISTITUTO_DEFAULT)}")
st.sidebar.markdown(f"**A.S.:** {st.session_state.schedule_data.get('anno_scolastico', '2025/2026')}")

# Funzioni di supporto
def display_schedule(show_empty=False, format_type="Standard"):
    """Visualizza l'orario in formato tabellare"""
    
    # Debug: mostra la struttura dei dati
    if st.checkbox("🔍 Debug - Mostra struttura dati", value=False):
        st.json(st.session_state.schedule_data)
    
    schedule = st.session_state.schedule_data.get('schedule', {})
    if not schedule:
        st.warning("⚠️ Nessun orario configurato. Vai alla sezione Configurazione o carica i dati di esempio.")
        return
    
    # Prepara i dati per la tabella
    giorni = st.session_state.schedule_data['giorni_settimana']
    ore_attive = st.session_state.schedule_data['ore_attive']
    orari = st.session_state.schedule_data['orari']
    
    # Crea header
    header = ["Giorno"] + [f"{i}ª" for i in ore_attive]
    
    # Crea righe dati
    data_rows = []
    for giorno in giorni:
        if giorno == st.session_state.schedule_data['giorno_libero'] and not st.session_state.schedule_data['include_giorno_libero']:
            continue
            
        row = [giorno]
        for ora in ore_attive:
            ora_str = str(ora)  # Converti in stringa per compatibilità con JSON
            if giorno in schedule and ora_str in schedule[giorno]:
                slot = schedule[giorno][ora_str]
                if slot['classe'] or show_empty:
                    if format_type == "Tascabile":
                        # Formato compatto per stampa tascabile
                        if slot['classe'] in ['DISP.', '—', '']:
                            text = slot['classe'] if slot['classe'] else ''
                        else:
                            time_str = f"{orari[ora_str]['dalle']}-{orari[ora_str]['alle']}"
                            text = f"{time_str} {slot['classe']}"
                            if slot['edificio']:
                                text += f" {slot['edificio']}"
                            if slot['piano']:
                                text += f" {slot['piano']}"
                            if slot['aula']:
                                text += f" {slot['aula']}"
                    elif format_type == "Compatto":
                        # Formato compatto per visualizzazione
                        if slot['classe'] in ['DISP.', '—', '']:
                            text = slot['classe'] if slot['classe'] else ''
                        else:
                            time_str = f"{orari[ora_str]['dalle']}-{orari[ora_str]['alle']}"
                            text = f"**{time_str}** {slot['classe']}"
                            if slot['edificio'] or slot['piano'] or slot['aula']:
                                location_parts = [slot['edificio'], slot['piano'], slot['aula']]
                                location = ' '.join([p for p in location_parts if p])
                                if location:
                                    text += f" 📍{location}"
                    else:
                        # Formato standard
                        if slot['classe'] in ['DISP.', '—', '']:
                            text = slot['classe'] if slot['classe'] else ''
                        else:
                            time_str = f"{orari[ora_str]['dalle']}-{orari[ora_str]['alle']}"
                            text = f"**{time_str}**\n{slot['classe']}"
                            if slot['edificio'] or slot['piano'] or slot['aula']:
                                location_parts = [slot['edificio'], slot['piano'], slot['aula']]
                                location = ' '.join([p for p in location_parts if p])
                                if location:
                                    text += f"\n📍 {location}"
                    row.append(text)
                else:
                    row.append('')
            else:
                row.append('')
        
        data_rows.append(row)
    
    # Crea DataFrame e visualizza
    df = pd.DataFrame(data_rows, columns=header)
    
    if format_type == "Tascabile":
        st.markdown("### 📱 Formato Tascabile (7.5x4cm)")
        st.markdown("*Ottimizzato per stampa in formato tascabile*")
        
        # Stile compatto
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            height=400
        )
    else:
        st.markdown(f"### 📊 Formato {format_type}")
        
        # Visualizza la tabella con formattazione markdown
        if data_rows:
            # Crea una tabella markdown con colonne allineate
            markdown_table = "| " + " | ".join(header) + " |\n"
            markdown_table += "| " + " | ".join(["---"] * len(header)) + " |\n"
            
            for row in data_rows:
                # Allinea le colonne sostituendo i caratteri di controllo
                formatted_row = []
                for cell in row:
                    # Sostituisce \n con <br/> per markdown
                    formatted_cell = cell.replace('\n', '<br/>')
                    formatted_row.append(formatted_cell)
                markdown_table += "| " + " | ".join(formatted_row) + " |\n"
            
            st.markdown(markdown_table, unsafe_allow_html=True)
        else:
            st.info("Nessun dato da visualizzare")
    
    # Pulsanti per la stampa
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🖨️ Stampa PDF Standard"):
            with st.spinner("Generazione PDF Standard..."):
                pdf_data, filename = generate_pdf("standard")
                if pdf_data:
                    st.download_button(
                        label="📥 Scarica PDF Standard",
                        data=pdf_data,
                        file_name=filename,
                        mime="application/pdf"
                    )
                else:
                    st.error("Errore nella generazione del PDF Standard")
    
    with col2:
        if st.button("📱 Stampa PDF Tascabile"):
            with st.spinner("Generazione PDF Tascabile..."):
                pdf_data, filename = generate_pdf("tascabile")
                if pdf_data:
                    st.download_button(
                        label="📥 Scarica PDF Tascabile",
                        data=pdf_data,
                        file_name=filename,
                        mime="application/pdf"
                    )
                else:
                    st.error("Errore nella generazione del PDF Tascabile")
    
    with col3:
        if st.button("📄 Stampa PDF A4"):
            with st.spinner("Generazione PDF A4..."):
                pdf_data, filename = generate_pdf("a4")
                if pdf_data:
                    st.download_button(
                        label="📥 Scarica PDF A4",
                        data=pdf_data,
                        file_name=filename,
                        mime="application/pdf"
                    )
                else:
                    st.error("Errore nella generazione del PDF A4")

def configure_schedule():
    """Interfaccia per configurare l'orario"""
    
    st.subheader("👤 Configurazione Docente e Istituto")
    
    # Configurazione docente, materie e istituto
    col1, col2 = st.columns(2)
    
    with col1:
        docente = st.text_input(
            "Nome Docente:",
            value=st.session_state.schedule_data.get('docente', 'Cristina Bellina Terra'),
            key="docente_input"
        )
        st.session_state.schedule_data['docente'] = docente
        
        materie = st.text_input(
            "Materie:",
            value=st.session_state.schedule_data.get('materie', 'Matematica e Fisica'),
            key="materie_input"
        )
        st.session_state.schedule_data['materie'] = materie
    
    with col2:
        istituto = st.text_input(
            "Istituto:",
            value=st.session_state.schedule_data.get('istituto', ISTITUTO_DEFAULT),
            key="istituto_input"
        )
        st.session_state.schedule_data['istituto'] = istituto
        
        anno_scolastico = st.text_input(
            "Anno Scolastico:",
            value=st.session_state.schedule_data.get('anno_scolastico', '2025/2026'),
            key="anno_scolastico_input"
        )
        st.session_state.schedule_data['anno_scolastico'] = anno_scolastico
    
    st.markdown("---")
    
    st.subheader("📅 Configurazione Giorni e Orari")
    
    # Configurazione giorni
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Giorni della Settimana")
        giorni_settimana = st.multiselect(
            "Seleziona i giorni attivi:",
            options=['LUN', 'MAR', 'MER', 'GIO', 'VEN', 'SAB', 'DOM'],
            default=st.session_state.schedule_data['giorni_settimana']
        )
        st.session_state.schedule_data['giorni_settimana'] = giorni_settimana
    
    with col2:
        st.markdown("#### Giorno Libero")
        giorno_libero = st.selectbox(
            "Giorno libero o di vacanza:",
            options=['LUN', 'MAR', 'MER', 'GIO', 'VEN', 'SAB', 'DOM'],
            index=['LUN', 'MAR', 'MER', 'GIO', 'VEN', 'SAB', 'DOM'].index(st.session_state.schedule_data['giorno_libero'])
        )
        st.session_state.schedule_data['giorno_libero'] = giorno_libero
        
        include_libero = st.checkbox(
            "Includi giorno libero nella stampa",
            value=st.session_state.schedule_data['include_giorno_libero']
        )
        st.session_state.schedule_data['include_giorno_libero'] = include_libero
    
    st.markdown("---")
    
    # Configurazione ore
    st.subheader("⏰ Configurazione Orari")
    
    ore_attive = st.multiselect(
        "Seleziona le ore attive (max 6):",
        options=[1, 2, 3, 4, 5, 6],
        default=st.session_state.schedule_data['ore_attive'],
        max_selections=6
    )
    
    # Aggiorna ore attive
    st.session_state.schedule_data['ore_attive'] = ore_attive
    
    # Inizializza orari solo per le ore che non esistono
    for ora in ore_attive:
        ora_str = str(ora)
        if ora_str not in st.session_state.schedule_data['orari']:
            # Orari di default progressivi solo se non esistono
            default_times = {
                '1': {'dalle': '08:15', 'alle': '09:15'},
                '2': {'dalle': '09:15', 'alle': '10:15'},
                '3': {'dalle': '10:15', 'alle': '11:15'},
                '4': {'dalle': '11:15', 'alle': '12:15'},
                '5': {'dalle': '12:15', 'alle': '13:15'},
                '6': {'dalle': '13:15', 'alle': '14:15'}
            }
            st.session_state.schedule_data['orari'][ora_str] = default_times.get(ora_str, {'dalle': '08:15', 'alle': '09:15'})
    
    # Configurazione orari specifici
    st.markdown("#### Orari delle Lezioni")
    
    for ora in ore_attive:
        col1, col2 = st.columns(2)
        
        # Gli orari sono già stati inizializzati sopra se necessario
        
        with col1:
            dalle = st.time_input(
                f"{ora}ª ora - Dalle:",
                value=datetime.strptime(st.session_state.schedule_data['orari'][str(ora)]['dalle'], '%H:%M').time(),
                key=f"dalle_{ora}"
            )
        with col2:
            alle = st.time_input(
                f"{ora}ª ora - Alle:",
                value=datetime.strptime(st.session_state.schedule_data['orari'][str(ora)]['alle'], '%H:%M').time(),
                key=f"alle_{ora}"
            )
        
        st.session_state.schedule_data['orari'][str(ora)] = {
            'dalle': dalle.strftime('%H:%M'),
            'alle': alle.strftime('%H:%M')
        }
    
    st.markdown("---")
    
    # Configurazione dettagliata dell'orario
    st.subheader("📚 Configurazione Dettagliata Orario")
    
    if st.button("🔄 Inizializza Orario Vuoto"):
        initialize_empty_schedule()
        st.success("Orario inizializzato!")
    
    # Editor per ogni giorno
    giorni_attivi = [g for g in st.session_state.schedule_data['giorni_settimana'] 
                     if g != st.session_state.schedule_data['giorno_libero'] or st.session_state.schedule_data['include_giorno_libero']]
    
    for giorno in giorni_attivi:
        with st.expander(f"📅 {giorno}"):
            edit_day_schedule(giorno)

def initialize_empty_schedule():
    """Inizializza un orario vuoto"""
    schedule = {}
    for giorno in st.session_state.schedule_data['giorni_settimana']:
        schedule[giorno] = {}
        for ora in st.session_state.schedule_data['ore_attive']:
            schedule[giorno][str(ora)] = {
                'classe': '',
                'edificio': '',
                'piano': '',
                'aula': ''
            }
    st.session_state.schedule_data['schedule'] = schedule

def edit_day_schedule(giorno):
    """Editor per un singolo giorno"""
    if giorno not in st.session_state.schedule_data['schedule']:
        st.session_state.schedule_data['schedule'][giorno] = {}
    
    for ora in st.session_state.schedule_data['ore_attive']:
        ora_str = str(ora)
        if ora_str not in st.session_state.schedule_data['schedule'][giorno]:
            st.session_state.schedule_data['schedule'][giorno][ora_str] = {
                'classe': '', 'edificio': '', 'piano': '', 'aula': ''
            }
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            classe = st.text_input(
                f"Classe {ora}ª ora:",
                value=st.session_state.schedule_data['schedule'][giorno][ora_str]['classe'],
                key=f"classe_{giorno}_{ora}",
                placeholder="es. 1A, 2B, DISP."
            )
        
        with col2:
            edificio = st.text_input(
                f"Edificio {ora}ª ora:",
                value=st.session_state.schedule_data['schedule'][giorno][ora_str]['edificio'],
                key=f"edificio_{giorno}_{ora}",
                placeholder="es. A, B, C"
            )
        
        with col3:
            piano = st.text_input(
                f"Piano {ora}ª ora:",
                value=st.session_state.schedule_data['schedule'][giorno][ora_str]['piano'],
                key=f"piano_{giorno}_{ora}",
                placeholder="es. PT, 1P, 2P"
            )
        
        with col4:
            aula = st.text_input(
                f"Aula {ora}ª ora:",
                value=st.session_state.schedule_data['schedule'][giorno][ora_str]['aula'],
                key=f"aula_{giorno}_{ora}",
                placeholder="es. A1, A15, A43"
            )
        
        # Aggiorna i dati
        st.session_state.schedule_data['schedule'][giorno][ora_str] = {
            'classe': classe,
            'edificio': edificio,
            'piano': piano,
            'aula': aula
        }

def generate_pdf(format_type="standard"):
    """Genera PDF dell'orario"""
    
    if not st.session_state.schedule_data.get('schedule'):
        st.error("⚠️ Nessun orario configurato!")
        return None, None
    
    try:
        # Prepara i dati
        giorni = st.session_state.schedule_data['giorni_settimana']
        ore_attive = st.session_state.schedule_data['ore_attive']
        orari = st.session_state.schedule_data['orari']
        schedule = st.session_state.schedule_data['schedule']
        
        # Configura formato
        if format_type == "tascabile":
            pagesize = landscape(A7)
            margins = 2
            font_size = 5.5
            leading = 6.0
        elif format_type == "a4":
            pagesize = A4
            margins = 20
            font_size = 10
            leading = 12
        else:  # standard
            pagesize = landscape(A4)
            margins = 15
            font_size = 8
            leading = 10
        
        # Crea buffer per il PDF
        buffer = io.BytesIO()
        try:
            doc = SimpleDocTemplate(buffer, pagesize=pagesize, 
                                  rightMargin=margins, leftMargin=margins, 
                                  topMargin=margins, bottomMargin=margins)
        except Exception as e:
            st.error(f"Errore nella creazione del documento PDF: {str(e)}")
            return None, None
        
        # Stili
        styles = getSampleStyleSheet()
        style = styles["Normal"]
        style.fontSize = font_size
        style.leading = leading
        
        # Stile per header
        header_style = styles["Normal"]
        header_style.fontSize = font_size
        header_style.leading = leading
        header_style.alignment = 1  # CENTER
        
        # Prepara dati tabella
        table_data = []
        
        # Titolo con informazioni docente
        docente = st.session_state.schedule_data.get('docente', 'Cristina Bellina Terra')
        materie = st.session_state.schedule_data.get('materie', 'Matematica e Fisica')
        istituto = st.session_state.schedule_data.get('istituto', ISTITUTO_DEFAULT)
        anno_scolastico = st.session_state.schedule_data.get('anno_scolastico', '2025/2026')
        
        if format_type == "tascabile":
            # Per formato tascabile, aggiungi solo il nome del docente
            title_style = styles["Title"]
            title_style.fontSize = font_size + 1
            title_style.alignment = 1  # CENTER
            
            # Crea una riga con il titolo che si estende su tutte le colonne
            title_row = [Paragraph(f"<b>{docente}</b>", title_style)] + [""] * len(ore_attive)
            table_data.append(title_row)
        else:
            # Per formati più grandi, aggiungi tutte le informazioni
            title_style = styles["Title"]
            title_style.fontSize = font_size + 2
            title_style.alignment = 1  # CENTER
            
            # Aggiungi titolo che si estende su tutte le colonne
            title_row = [Paragraph(f"<b>ORARIO SETTIMANALE</b>", title_style)] + [""] * len(ore_attive)
            table_data.append(title_row)
            
            docente_row = [Paragraph(f"<b>{docente}</b>", style)] + [""] * len(ore_attive)
            table_data.append(docente_row)
            
            materie_row = [Paragraph(f"{materie}", style)] + [""] * len(ore_attive)
            table_data.append(materie_row)
            
            istituto_row = [Paragraph(f"{istituto}", style)] + [""] * len(ore_attive)
            table_data.append(istituto_row)
            
            anno_scolastico_row = [Paragraph(f"A.S. {anno_scolastico}", style)] + [""] * len(ore_attive)
            table_data.append(anno_scolastico_row)
            
            # Riga vuota
            empty_row = [""] * (1 + len(ore_attive))
            table_data.append(empty_row)
        
        # Header
        if format_type == "tascabile":
            header = ["Giorno"] + [f"{i}ª ora" for i in ore_attive]
        else:
            header = ["Giorno"] + [f"{i}ª ora" for i in ore_attive]
        
        table_data.append([Paragraph(f"<b>{h}</b>", header_style) for h in header])
        
        # Verifica che ci siano dati da stampare
        has_data = False
        
        # Righe dati
        for giorno in giorni:
            if giorno == st.session_state.schedule_data['giorno_libero'] and not st.session_state.schedule_data['include_giorno_libero']:
                continue
            
            row = [Paragraph(f"<b>{giorno}</b>", style)]
            
            for ora in ore_attive:
                ora_str = str(ora)
                if giorno in schedule and ora_str in schedule[giorno]:
                    slot = schedule[giorno][ora_str]
                    
                    if slot['classe'] in ['DISP.', '—', '']:
                        text = slot['classe'] if slot['classe'] else ''
                    else:
                        time_str = f"{orari[ora_str]['dalle']}-{orari[ora_str]['alle']}"
                        
                        if format_type == "tascabile":
                            # Formato compatto per tascabile
                            text = f"{time_str} {slot['classe']}"
                            if slot['edificio']:
                                text += f" {slot['edificio']}"
                            if slot['piano']:
                                text += f" {slot['piano']}"
                            if slot['aula']:
                                text += f" {slot['aula']}"
                        else:
                            # Formato standard
                            text = f"<b>{time_str}</b><br/>{slot['classe']}"
                            if slot['edificio'] or slot['piano'] or slot['aula']:
                                location_parts = [slot['edificio'], slot['piano'], slot['aula']]
                                location = ' '.join([p for p in location_parts if p])
                                if location:
                                    text += f"<br/>{location}"
                        
                        # Marca che ci sono dati
                        if slot['classe'] and slot['classe'] not in ['DISP.', '—', '']:
                            has_data = True
                    
                    row.append(Paragraph(text, style))
                else:
                    row.append(Paragraph("", style))
            
            table_data.append(row)
        
        # Verifica che ci siano dati da stampare
        if not has_data:
            st.warning("⚠️ Nessun dato da stampare nell'orario!")
            return None, None
        
        # Calcola l'indice dell'header (la riga che contiene "Giorno" e le ore)
        # L'header è la riga che abbiamo aggiunto dopo il titolo
        # Devo contare quante righe del titolo ci sono
        if format_type == "tascabile":
            # Per formato tascabile: 1 riga titolo + 1 riga header
            header_row = 1
        else:
            # Per formati più grandi: 5 righe titolo + 1 riga vuota + 1 riga header
            header_row = 6
        
        # Crea tabella
        if format_type == "tascabile":
            col_widths = [35] + [45] * len(ore_attive)  # Allargata colonna Giorno
        else:
            col_widths = [80] + [110] * len(ore_attive)  # Allargata colonna Giorno
        
        # Per il titolo, usa una colonna che si estende su tutte le colonne
        if format_type == "tascabile":
            # Per formato tascabile, il titolo è solo il nome del docente
            table = Table(table_data, colWidths=col_widths)
        else:
            # Per formati più grandi, il titolo si estende su tutte le colonne
            table = Table(table_data, colWidths=col_widths)
        
        # Stile tabella
        table_style = [
            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),  # Centratura verticale
            ("ALIGN", (0,0), (-1,-1), "CENTER"),    # Centratura orizzontale
        ]
        
        # Applica griglia a tutta la tabella
        table_style.extend([
            ("GRID", (0,0), (-1,-1), 0.25, colors.grey),
        ])
        
        # Tutte le celle hanno sfondo bianco (nessun sfondo grigio)
        
        # Unisci le celle del titolo per farlo estendere su tutte le colonne
        if format_type == "tascabile":
            # Per formato tascabile, unisci solo la prima riga (titolo docente)
            table_style.append(("SPAN", (0,0), (-1,0)))
        else:
            # Per formati più grandi, unisci tutte le righe del titolo e la riga vuota
            table_style.extend([
                ("SPAN", (0,0), (-1,0)),  # ORARIO SETTIMANALE
                ("SPAN", (0,1), (-1,1)),  # Nome docente
                ("SPAN", (0,2), (-1,2)),  # Materie
                ("SPAN", (0,3), (-1,3)),  # Istituto
                ("SPAN", (0,4), (-1,4)),  # Anno scolastico
                ("SPAN", (0,5), (-1,5)),  # Riga vuota
            ])
        
        if format_type != "tascabile":
            table_style.append(("FONTSIZE", (0,0), (-1,-1), font_size))
        
        table.setStyle(TableStyle(table_style))
        
        # Genera PDF
        try:
            doc.build([table])
            
            # Prepara download
            buffer.seek(0)
            pdf_data = buffer.getvalue()
            
            # Verifica che il PDF sia stato generato correttamente
            if len(pdf_data) == 0:
                st.error("Errore: PDF generato vuoto")
                return None, None
            
            # Nome file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"orario_docente_{format_type}_{timestamp}.pdf"
            
            st.success(f"✅ PDF {format_type} generato con successo! ({len(pdf_data)} bytes)")
            return pdf_data, filename
            
        except Exception as e:
            st.error(f"Errore nella generazione del PDF: {str(e)}")
            return None, None
        
    except Exception as e:
        st.error(f"❌ Errore nella generazione del PDF: {str(e)}")
        return None, None

# Contenuto principale
if page == "home":
    st.title("🏠 Benvenuti nella Gestione Orario Docente")
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Giorni Attivi", len([g for g in st.session_state.schedule_data['giorni_settimana'] if g != st.session_state.schedule_data['giorno_libero']]))
    
    with col2:
        st.metric("Ore Giornaliere", st.session_state.schedule_data['ore_giornaliere'])
    
    with col3:
        st.metric("Ore Attive", len(st.session_state.schedule_data['ore_attive']))
    
    st.markdown("### 📋 Funzionalità Disponibili")
    st.markdown("""
    - **📅 Orario**: Visualizza e gestisci l'orario delle lezioni
    - **⚙️ Configurazione**: Personalizza giorni, orari e impostazioni
    - **🖨️ Stampa**: Genera PDF in diversi formati (standard, tascabile)
    - **💾 Salvataggio**: Salva e carica configurazioni personalizzate
    """)

elif page == "orario":
    st.title("📅 Gestione Orario")
    st.markdown("---")
    
    # Controlli per la visualizzazione
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.subheader("Orario Settimanale")
    
    with col2:
        show_empty = st.checkbox("Mostra ore vuote", value=False)
    
    with col3:
        format_type = st.selectbox("Formato", ["Standard", "Compatto", "Tascabile"])
    
    # Visualizzazione orario
    display_schedule(show_empty, format_type)

elif page == "configurazione":
    st.title("⚙️ Configurazione Orario")
    st.markdown("---")
    
    configure_schedule()

if __name__ == "__main__":
    pass
