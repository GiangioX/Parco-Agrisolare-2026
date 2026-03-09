import streamlit as st
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Bando Agrisolare 2026",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="auto"
)

# Custom CSS for a beautiful, premium "Agrisolare" theme
# We'll use dark mode base with vibrant emerald green and sun yellow accents
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    .stApp {
        background-color: #0d120e;
        color: #e6f0e9;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: rgba(14, 23, 17, 0.75) !important;
        backdrop-filter: blur(12px);
        border-right: 1px solid #1c3224;
    }
    
    /* Cards and Containers */
    div.stExpander, .custom-card {
        background-color: #121e15 !important;
        border: 1px solid #1c3224;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.4);
    }
    
    /* Input Fields */
    .stTextInput>div>div>input, .stNumberInput>div>div>div>input, .stSelectbox>div>div>div {
        background-color: #0b110c !important;
        color: #e6f0e9 !important;
        border: 1px solid #1c3224 !important;
        border-radius: 8px !important;
    }
    .stSelectbox>div>div>div:hover, .stTextInput>div>div>input:hover, .stNumberInput>div>div>div>input:hover {
        border-color: #fca311 !important;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #fca311, #ffb703);
        color: #0b110c;
        border-radius: 8px;
        font-weight: 700;
        border: none;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 4px 12px rgba(252, 163, 17, 0.3);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(252, 163, 17, 0.5);
        background: linear-gradient(135deg, #ffb703, #ffc300);
        color: #000;
    }
    
    /* Warning/Info Alerts */
    .stAlert {
        border-radius: 12px;
        border: 1px solid #1c3224;
    }
    
    /* Metric styling custom card */
    .custom-metric-card {
        background: linear-gradient(145deg, #182a1d, #111e15);
        border: 1px solid #23402c;
        border-radius: 16px;
        padding: 20px;
        text-align: left;
        box-shadow: 0 8px 16px rgba(0,0,0,0.3);
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
    }
    .custom-metric-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; width: 100%; height: 4px;
        background: linear-gradient(90deg, #fca311, #38b000);
    }
    .metric-title {
        color: #a3c4a9;
        font-size: 0.9rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }
    .metric-value {
        font-size: 2.2rem;
        color: #fca311;
        font-weight: 800;
        margin-bottom: 5px;
        text-shadow: 0 2px 4px rgba(0,0,0,0.5);
    }
    .metric-delta {
        font-size: 0.85rem;
        color: #38b000;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
        border-bottom: 1px solid #1c3224;
    }
    .stTabs [data-baseweb="tab"] {
        color: #8b9d91;
        font-size: 1.1rem;
        font-weight: 500;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        color: #fca311 !important;
        font-weight: 700 !important;
        border-bottom-color: #fca311 !important;
        border-bottom-width: 3px !important;
    }
    
    /* Headers & Markdown */
    h1, h2, h3 {
        color: #e6f0e9;
        font-family: 'Outfit', sans-serif;
    }
    a {
        color: #fca311;
        text-decoration: none;
    }
    a:hover {
        text-decoration: underline;
    }
    
    /* Hide Streamlit Production Header & Deploy Button */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden; display: none !important;}
    footer {visibility: hidden;}
    
    /* Responsive Fixes */
    @media (max-width: 768px) {
        .metric-value { font-size: 1.8rem !important; }
        [data-testid="stChatInputContainer"] {
            padding-bottom: 40px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

if "rag_chain" not in st.session_state:
    if os.environ.get("OPENAI_API_KEY"):
        with st.spinner("Avvio motore intelligenza Agrisolare... 🚜☀️"):
            try:
                from rag_engine import get_rag_chain
                st.session_state.rag_chain = get_rag_chain()
                st.session_state.rag_error = None
            except Exception as e:
                import traceback
                st.session_state.rag_error = f"{type(e).__name__}: {str(e)}"
                st.session_state.rag_chain = None
    else:
        st.session_state.rag_error = None
        st.session_state.rag_chain = None

# Sidebar
with st.sidebar:
    st.markdown("""
        <div style="display:flex; align-items:center; gap: 15px; margin-bottom: 30px;">
            <div style="background: linear-gradient(135deg, #fca311, #fb8500); border-radius: 12px; padding: 14px; box-shadow: 0 4px 15px rgba(252, 163, 17, 0.4);">
                <span style="font-size: 32px; line-height: 1;">☀️</span>
            </div>
            <div>
                <h2 style="margin:0; padding:0; font-size: 1.6rem; font-weight: 800; letter-spacing: -0.5px; color: white;">Agrisolare</h2>
                <p style="margin:0; padding:0; color: #a3c4a9; font-size: 0.9rem; font-weight: 500;">Bando 2026 - MASAF</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Financial Status Card
    st.markdown("""
    <div class="custom-metric-card" style="margin-bottom: 25px;">
        <div class="metric-title">Fondi Disponibili PNRR</div>
        <div class="metric-value">€ 789 Mln</div>
        <div class="metric-delta">📌 Contributo fondo perduto a sportello</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h3 style='font-size: 1.1rem; color: #a3c4a9; margin-bottom: 12px;'>🗓️ Date Chiave</h3>", unsafe_allow_html=True)
    
    events = [
        {"icon": "🚀", "title": "Apertura Sportello", "date": "10 Marzo 2026", "time": "Ore 12:00"},
        {"icon": "⏳", "title": "Chiusura Sportello", "date": "09 Aprile 2026", "time": "Ore 12:00"},
        {"icon": "🏗️", "title": "Fine Lavori", "date": "Entro 18 mesi", "time": "Dalla concessione"}
    ]
    
    for ev in events:
        st.markdown(f"""
        <div style="background: rgba(20, 35, 24, 0.6); border: 1px solid #1c3224; padding: 12px 15px; margin-bottom: 10px; border-radius: 10px; display: flex; align-items: center; gap: 12px;">
            <div style="font-size: 1.5rem;">{ev['icon']}</div>
            <div>
                <div style="color: #ffffff; font-weight: 600; font-size: 0.95rem;">{ev['title']}</div>
                <div style="color: #fca311; font-size: 0.85rem; font-weight: 700;">{ev['date']} <span style="color:#a3c4a9; font-weight: 400;">{ev['time']}</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
            
    st.markdown("<br>", unsafe_allow_html=True)
    st.success("💡 **Novità 2026:** Fino all'80% a fondo perduto per impianti da 6 a 1.000 kWp su coperture di fabbricati rurali.")

# Main Interface
st.title("🚜 Parco Agrisolare 2026")
st.markdown("<p style='font-size: 1.2rem; color: #a3c4a9; margin-top: -10px; font-weight: 400;'>Piattaforma informativa, simulatore incentivi e consulente IA per le aziende agricole.</p>", unsafe_allow_html=True)
# Setup query params for tab state retention (optional, minimal effort to mitigate chat reset)
tab1, tab2, tab3 = st.tabs(["ℹ️ Informativa Bando", "💶 Simulatore Contributo", "💬 Assistente Agrisolare"])

# --- TAB 1: INFORMATIVA ---
with tab1:
    st.markdown("""
    ### 🎯 Obiettivi e Contesto della Misura

    La misura **"Parco Agrisolare 2026"** (finanziata dal PNRR per **789 Milioni di Euro** complessivi) sostiene l'installazione di nuova capacità di generazione solare fotovoltaica su **coperture di fabbricati strumentali** all'attività agricola, agro-meccanica, d'allevamento e agroindustriale, promuovendo contestualmente l'efficienza energetica e la riqualificazione delle strutture.
    
    > **ATTENZIONE:** La misura si applica **esclusivamente su coperture** (tetti). L'installazione di moduli fotovoltaici "a terra" (che comporta consumo di suolo agricolo) **non è ammissibile** ai sensi di questo bando, fatte salve le eccezioni del Decreto Agricoltura (DL 63/2024) per l'agrivoltaico avanzato, che seguono iter differenti.
    
    ---
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: #121e15; border: 1px solid #23402c; border-radius: 12px; padding: 20px; text-align: center; height: 100%;">
            <div style="font-size: 2.5rem; margin-bottom: 15px;">🏛️</div>
            <h4 style="color:#fca311; margin-top:0; font-size:1.1rem;">Soggetti Beneficiari</h4>
            <p style="color:#a3c4a9; font-size:0.90rem; text-align:left;">
            Possono presentare domanda di accesso al contributo:<br>
            • Imprenditori agricoli (singoli o in forma societaria)<br>
            • Imprese agroindustriali e agro-meccaniche<br>
            • Cooperative agricole e consorzi<br>
            • Raggruppamenti temporanei di imprese (RTI) e reti d'impresa.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background: #121e15; border: 1px solid #23402c; border-radius: 12px; padding: 20px; text-align: center; height: 100%;">
            <div style="font-size: 2.5rem; margin-bottom: 15px;">⚡</div>
            <h4 style="color:#fca311; margin-top:0; font-size:1.1rem;">Requisiti e Limiti Impianto</h4>
            <p style="color:#a3c4a9; font-size:0.90rem; text-align:left;">
            L'impianto fotovoltaico ammissibile deve prevedere:<br>
            • Potenza di picco compresa tra <b>6 kWp</b> e <b>1.000 kWp</b>.<br>
            • Obbligo di soddisfare il fabbisogno energetico dell'azienda (con o senza l'autoconsumo condiviso).<br>
            • Fine lavori tassativa entro <b>18 mesi</b> dal provvedimento di ammissione.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="background: #121e15; border: 1px solid #23402c; border-radius: 12px; padding: 20px; text-align: center; height: 100%;">
            <div style="font-size: 2.5rem; margin-bottom: 15px;">💶</div>
            <h4 style="color:#fca311; margin-top:0; font-size:1.1rem;">Intensità del Contributo</h4>
            <p style="color:#a3c4a9; font-size:0.90rem; text-align:left;">
            Contributo in conto capitale (fondo perduto) calcolato sulle spese ammissibili:<br>
            • Fino all'<b>80%</b> per imprese nel Mezzogiorno o giovani agricoltori.<br>
            • Fino al <b>65%</b> o <b>50%</b> nelle restanti regioni (a seconda della dimensione d'impresa e premialità).<br>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("### 🛠️ Interventi Complementari ed Efficienza Energetica")
    st.info("Oltre alla fornitura e posa in opera dei pannelli fotovoltaici (inclusi inverter e quadri), è possibile inserire a budget spese accessorie e riqualificazioni strutturali (che godono della medesima aliquota agevolata):")
    
    st.markdown("""
    1. 🧱 **Rimozione e smaltimento amianto / eternit** dalle coperture esistenti (con rifacimento del tetto idoneo per il solare).
    2. 🌡️ **Isolamento termico dei tetti** (coibentazione della copertura per migliorare l'efficienza energetica dell'immobile).
    3. 💨 **Sistemi di aerazione** (creazione di sistemi di ventilazione integrati alla nuova copertura).
    4. 🔋 **Sistemi di accumulo (BESS)** per ottimizzare l'autoconsumo energetico dell'azienda (nel limite della spesa massimale definita dal GSE).
    5. 🔌 **Infrastrutture di ricarica elettrica** aziendali (Wallbox o colonnine, esclusivamente per mezzi strumentali all'attività agricola).
    """)

# --- TAB 2: SIMULATORE ---
with tab2:
    st.markdown("### 🧮 Simulatore Plafond Ammissibile")
    st.markdown("Usa questo strumento per stimare rapidamente la **Spesa Massima Ammissibile** secondo i parametri medi di mercato (che verranno cappati dai limiti €/kW indicati nelle direttive GSE) e valutare i ritorni economici potenziali.")
    
    with st.container():
        st.markdown("<div class='custom-card' style='padding: 25px;'>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            potenza_fv = st.number_input("⚡ Potenza Impianto Fotovoltaico (kWp) [Da 6 a 1.000]", min_value=6.0, max_value=1000.0, value=50.0, step=1.0)
            include_batteria = st.checkbox("🔋 Includi Sistema di Accumulo (Batteria)", value=True)
        with c2:
            amianto_mq = st.number_input("🧱 Superficie tetto ex-amianto da bonificare (Metri Quadri)", min_value=0, max_value=10000, value=0, step=50)
            colonnina = st.checkbox("🔌 Includi Colonnina di ricarica per i veicoli", value=False)
            
        st.markdown("---")
        aliquota_scelta = st.radio("Seleziona l'intensità del fondo perduto attesa (Varia in base a Regione, Dimensione Impresa e Premialità):", options=[0.80, 0.65, 0.50], format_func=lambda x: f"{int(x*100)}% Fondo Perduto", horizontal=True)
        st.markdown("---")

        # Stime indicative per simulazione (allineate empiricamente ai prezziari del settore)
        costo_fv = potenza_fv * 1500  # Costo stimato 1500€ per kWp installato chiavi in mano
        costo_batt = (potenza_fv * 1000 * 0.5) if include_batteria else 0 # Dimensionamento batteria ipotetico a 50% della potenza oraria
        costo_amianto = amianto_mq * 150  # Costo bonifica+smaltimento+rifacimento copertura estimato a 150€/mq
        costo_colonnina = 8000 if colonnina else 0
        
        spesa_totale = costo_fv + costo_batt + costo_amianto + costo_colonnina
        fondo_perduto = spesa_totale * aliquota_scelta
        quota_privata = spesa_totale - fondo_perduto
        
        btn_calc = st.button("Avvia Simulazione Economica")
        st.markdown("</div>", unsafe_allow_html=True)
        
        if btn_calc:
            st.markdown("<br>", unsafe_allow_html=True)
            
            mc1, mc2, mc3 = st.columns(3)
            with mc1:
                st.markdown(f"""
                <div class="custom-metric-card">
                    <div class="metric-title">Spesa Totale (Stima)</div>
                    <div class="metric-value" style="font-size: 1.8rem;">€ {spesa_totale:,.2f}</div>
                    <div class="metric-delta" style="color: #a3c4a9;">Costi Impianto + Opere Extra</div>
                </div>
                """, unsafe_allow_html=True)
            with mc2:
                st.markdown(f"""
                <div class="custom-metric-card" style="border-color: #fca311;">
                    <div class="metric-title">Fondo Perduto ({int(aliquota_scelta*100)}%)</div>
                    <div class="metric-value" style="color: #38b000; font-size: 1.8rem;">€ {fondo_perduto:,.2f}</div>
                    <div class="metric-delta" style="color: #fca311;">Incentivo Diretto MASAF</div>
                </div>
                """, unsafe_allow_html=True)
            with mc3:
                st.markdown(f"""
                <div class="custom-metric-card" style="border-color: #fca311;">
                    <div class="metric-title">Quota Aziendale Residua</div>
                    <div class="metric-value" style="color: #ffb703; font-size: 1.8rem;">€ {quota_privata:,.2f}</div>
                    <div class="metric-delta" style="color: #fca311;">Esposizione al netto della tariffa incentivante</div>
                </div>
                """, unsafe_allow_html=True)

            with st.expander("📊 Apri il Dettaglio Analitico delle Voci di Costo", expanded=True):
                st.markdown(f"""
                - **Fornitura e Posa Moduli FV ({potenza_fv} kWp):** € {costo_fv:,.2f} 
                  *(inclusi inverter, quadri, progettazione e oneri di connessione stimati).*
                """)
                if include_batteria: 
                    st.markdown(f"- **Sistema di Accumulo (BESS):** € {costo_batt:,.2f} *(Stima approssimativa per ~{potenza_fv*0.5} kWh di capacità).*")
                if amianto_mq > 0: 
                    st.markdown(f"- **Rimozione Amianto e Rifacimento tetto ({amianto_mq} mq):** € {costo_amianto:,.2f}")
                if colonnina: 
                    st.markdown(f"- **Infrastruttura Diramata di Ricarica EV:** € {costo_colonnina:,.2f}")
                
            st.warning("⚠️ **AVVISO IMPORTANTE:** *I valori riportati sono proiezioni indicative per supportare la valutazione preliminare del business plan. I quadri economici finali ammissibili a finanziamento (plafond) sono determinati rigidamente dalle tabelle ministeriali dei costi massimi consentiti espressi in €/kW o €/kWh.* L'IVA è da considerarsi esclusa e non agevolabile se l'attività agricola la scarica/recupera.")


# --- TAB 3: CHAT AI ---
with tab3:
    st.markdown("### 💬 L'Intelligenza Artificiale che Conosce il Bando 2026")
    st.markdown("Fai una domanda per verificare l'**ammissibilità del tuo codice ATECO**, i requisiti tecnici (vincolo autoconsumo vs vendita), la differenza con le procedure canoniche DILA/PAS per il fotovoltaico a terra e i prerequisiti per presentare le domande sul portale GSE del **10 Marzo 2026**.")
    
    if not st.session_state.rag_chain:
        if st.session_state.get("rag_error"):
            st.error(f"Errore caricamento Modello AI: {st.session_state.rag_error}\nVerifica i logs o i pacchetti Python installati.")
        else:
            st.warning("⚠️ **Assistente Offline** - Inserisci OPENAI_API_KEY nel file `.env` e riavvia per sbloccare la consulenza in tempo reale sul bando Agrisolare 2026.")
        
    # Quick Prompts
    st.markdown("<p style='font-size: 0.9rem; color: #a3c4a9; margin-bottom: 5px;'>Schiaccia un pulsante o scrivi la tua domanda personalizzata:</p>", unsafe_allow_html=True)
    qp1, qp2, qp3 = st.columns(3)
    quick_prompt = None
    
    if qp1.button("Imprese miste ed ATECO ammessi?"): 
        quick_prompt = "Le imprese agricole con attività agrituristica mista o serre possono partecipare al Bando Agrisolare 2026? Quali codici ATECO sono idonei?"
    if qp2.button("Autoconsumo o Vendita?"): 
        quick_prompt = "Nel bando Agrisolare 2026 l'energia fotovoltaica prodotta deve essere totalmente autoconsumata dall'azienda o può essere venduta in rete? Cosa cambia per i raggruppamenti (CER/AUC)?"
    if qp3.button("Limiti di spesa e GSE?"): 
        quick_prompt = "C'è un limite massimo assoluto in €/kWp per il fotovoltaico e per i sistemi di accumulo associati all'impianto dettato dal GSE per giustificare le spese?"

    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_area("Poni il tuo quesito normativo o tecnico all'IA Agrisolare...", height=100)
        submitted = st.form_submit_button("Invia Domanda 🚀")
        
    active_prompt = None
    if submitted and user_input.strip():
        active_prompt = user_input.strip()
    elif quick_prompt:
        active_prompt = quick_prompt

    if active_prompt:
        st.session_state.chat_messages.append({"role": "user", "content": active_prompt})
        
        with st.spinner("Ricerca nei decreti MASAF e nelle Linee Guida GSE (Bando 2026)..."):
            if st.session_state.rag_chain:
                try:
                    response = st.session_state.rag_chain.invoke({"input": active_prompt})
                    answer = response.get("output", str(response))
                except Exception as e:
                    answer = f"Errore server AI: {e}"
            else:
                answer = "*(Questa è una demo off-line. Per rispondere esplorerei il regolamento del MASAF e le linee guida del GSE relative al tuo quesito. Collega OpenAI per testare l'algoritmo completo)*."
            
            st.session_state.chat_messages.append({"role": "assistant", "content": answer})

    st.markdown("<hr style='border-color: #1c3224; margin: 30px 0;'>", unsafe_allow_html=True)
    st.markdown("#### Storico Conversazione (Ultimi messaggi in alto)")
    
    # Render Chat REVERSED
    reversed_msgs = list(reversed(st.session_state.chat_messages))
    for msg in reversed_msgs:
        if msg["role"] == "user":
            with st.chat_message("user", avatar="🧑‍🌾"):
                st.markdown(f"<span style='color: #e6f0e9;'>{msg['content']}</span>", unsafe_allow_html=True)
        else:
            with st.chat_message("assistant", avatar="🚜"):
                st.markdown(msg["content"])

# Footer UI
st.markdown("<hr style='border-color: #1c3224; margin-top: 50px;'>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #a3c4a9; font-size: 0.85rem;'>☀️ Piattaforma Bando Agrisolare 2026 - powered by Streamlit & IA Avanzata. Non costituisce parere legale ufficiale.</p>", unsafe_allow_html=True)
