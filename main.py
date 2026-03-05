import streamlit as st
from gtts import gTTS
import io

# Stable Premium Configuration
st.set_page_config(page_title="Talk Agribusiness | Flashcards Hub", page_icon="🚜", layout="centered")

# --- CUSTOM CSS (Optimized for active learning and branding) ---
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        transition: all 0.3s ease;
        font-weight: bold;
        border: 1px solid #1E3A8A;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .flashcard-container {
        background-color: white;
        padding: 50px 30px;
        border-radius: 25px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.05);
        text-align: center;
        border: 1px solid #f0f2f6;
        margin-bottom: 25px;
    }
    h1 { color: #1E3A8A; }
    </style>
    """, unsafe_allow_html=True)

# --- COMPLETE DATABASE (Aulas 14 & 15) ---
data = {
    "Session 14: Corporate & Logistics": {
        "DAY 1: The Story + Sarah's Email": [
            {"t": "quarterly", "p": "ˈkwɔːrtərli", "tr": "trimestral", "ex": "We need to review the quarterly results."},
            {"t": "results", "p": "rɪˈzʌlts", "tr": "resultados", "ex": "The harvest results were better than expected."},
            {"t": "available", "p": "əˈveɪləbl", "tr": "disponível", "ex": "Is the manager available for a call?"},
            {"t": "desk", "p": "desk", "tr": "mesa de trabalho", "ex": "He left the documents on my desk."},
            {"t": "busy", "p": "ˈbɪzi", "tr": "ocupado/a", "ex": "I am very busy with the export logistics."},
            {"t": "late", "p": "leɪt", "tr": "atrasado/a", "ex": "The truck is two hours late."},
            {"t": "absent", "p": "ˈæbsənt", "tr": "ausente", "ex": "The supervisor was absent yesterday."},
            {"t": "building", "p": "ˈbɪldɪŋ", "tr": "prédio / edifício", "ex": "Our office is in that building."},
            {"t": "reports", "p": "rɪˈpɔːrts", "tr": "relatórios", "ex": "Send me the production reports, please."},
            {"t": "meeting", "p": "ˈmiːtɪŋ", "tr": "reunião", "ex": "We have a meeting about the new budget."},
            {"t": "team", "p": "tiːm", "tr": "equipe", "ex": "Our sales team is visiting the farm."},
            {"t": "nobody", "p": "ˈnoʊbədi", "tr": "ninguém", "ex": "Nobody was at the warehouse."}
        ],
        "DAY 2: Grammar + Drills": [
            {"t": "ready", "p": "ˈredi", "tr": "pronto/a", "ex": "The contract is ready for signing."},
            {"t": "on time", "p": "ɒn taɪm", "tr": "no horário", "ex": "The delivery arrived exactly on time."},
            {"t": "in the office", "p": "ɪn ðə ˈɒfɪs", "tr": "no escritório", "ex": "Is the CEO in the office today?"}
        ]
    },
    "Session 15: Past & Projects": {
        "DAY 1: Monday Meeting": [
            {"t": "work → worked", "p": "wɜːrkt", "tr": "trabalhar / trabalhou", "ex": "I worked in the field all day yesterday."},
            {"t": "call → called", "p": "kɔːld", "tr": "ligar / ligou", "ex": "She called the supplier to check the order."}
        ]
    }
}

# --- AUDIO FUNCTION ---
def touch_audio(text):
    clean_text = text.split('→')[-1].strip()
    tts = gTTS(text=clean_text, lang='en')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    st.audio(fp, format='audio/mp3')

# --- LOGIC ENGINE ---
st.sidebar.markdown("## 🚜 Talk Agribusiness")
st.sidebar.markdown("---")
# Translated sidebar menus
aula_sel = st.sidebar.selectbox("Select Session:", list(data.keys()))
dia_sel = st.sidebar.selectbox("Select Study Day:", list(data[aula_sel].keys()))

lista_cards = data[aula_sel][dia_sel]

# Session State for Flip and Navigation
idx_key = f"{aula_sel}_{dia_sel}_idx"
flipped_key = f"{aula_sel}_{dia_sel}_flipped"

if idx_key not in st.session_state: st.session_state[idx_key] = 0
if flipped_key not in st.session_state: st.session_state[flipped_key] = False

idx = st.session_state[idx_key]
card = lista_cards[idx]

# --- USER INTERFACE (English Only) ---
st.title("Agro Executive Flashcards")
st.write(f"Current Session: {aula_sel} | {dia_sel}")

# Flashcard Container
with st.container():
    st.markdown('<div class="flashcard-container">', unsafe_allow_html=True)
    
    if not st.session_state[flipped_key]:
        # Front of the card (English Only)
        st.markdown(f"<h1 style='font-size: 55px; height: 140px; display: flex; align-items: center; justify-content: center;'>{card['t']}</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: #6c757d; font-size: 20px;'>Pronunciation: /{card.get('p', '')}/</p>", unsafe_allow_html=True)
        
        st.write("")
        # Updated Action Button: English + Teal Green
        if st.button("🔄 REVEAL CONTENT", key="reveal_btn"):
            st.session_state[flipped_key] = True
            st.rerun()
    else:
        # Back of the card (English examples, localized translations)
        st.markdown(f"<h2 style='color: #2E7D32; height: 100px; display: flex; align-items: center; justify-content: center;'>Translation: {card['tr']}</h2>", unsafe_allow_html=True)
        st.divider()
        st.markdown(f"**Contextual Example:**")
        st.write(f"*{card.get('ex', '')}*")
        
        st.write("")
        if st.button("⬅️ GO BACK", key="back_btn"):
            st.session_state[flipped_key] = False
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# Audio Button (Always available for active listening)
if st.button("🔊 LISTEN TO PRONUNCIATION", key="audio_btn"):
    touch_audio(card['t'])

# Navigation Columns
st.write("")
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    if st.button("⬅️ PREVIOUS", key="prev_btn") and idx > 0:
        st.session_state[idx_key] -= 1
        st.session_state[flipped_key] = False
        st.rerun()
with col3:
    if st.button("NEXT ➡️", key="next_btn") and idx < len(lista_cards) - 1:
        st.session_state[idx_key] += 1
        st.session_state[flipped_key] = False
        st.rerun()

# Professional Progress Bar
progresso = (idx + 1) / len(lista_cards)
st.progress(progresso)
st.markdown(f"<p style='text-align: center;'>Progress: {idx + 1} of {len(lista_cards)} terms</p>", unsafe_allow_html=True)
