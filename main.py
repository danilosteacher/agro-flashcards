import streamlit as st
from gtts import gTTS
import io

# Configuração de Página
st.set_page_config(page_title="Talk Agribusiness - Flashcards", page_icon="🚜", layout="wide")

# --- BANCO DE DADOS (Adicionei o campo 'ex') ---
data = {
    "Aula 14: Past & Business": {
        "Dia 1: Verbs & Time": {
            "BLOCK A: Verbs (Past)": [
                {"t": "work → worked", "p": "wɜːrkt", "tr": "trabalhei/trabalhou", "ex": "I worked late yesterday."},
                {"t": "call → called", "p": "kɔːld", "tr": "liguei/ligou", "ex": "He called the supplier this morning."},
                {"t": "email → emailed", "p": "ˈeɪmeɪld", "tr": "enviei email", "ex": "I emailed the report to the manager."}
            ]
        }
    }
}

# --- MOTOR DO SISTEMA ---
st.sidebar.header("🚜 Talk Agribusiness")
aula_sel = st.sidebar.selectbox("Aula:", list(data.keys()))
dia_sel = st.sidebar.selectbox("Dia:", list(data[aula_sel].keys()))
bloco_sel = st.sidebar.selectbox("Bloco:", list(data[aula_sel][dia_sel].keys()))

lista_cards = data[aula_sel][dia_sel][bloco_sel]

# Chaves de estado para controle do flashcard
idx_key = f"{aula_sel}_{dia_sel}_{bloco_sel}_idx"
reveal_key = f"{aula_sel}_{dia_sel}_{bloco_sel}_reveal"

if idx_key not in st.session_state:
    st.session_state[idx_key] = 0
if reveal_key not in st.session_state:
    st.session_state[reveal_key] = False

idx = st.session_state[idx_key]
card = lista_cards[idx]

# --- INTERFACE DO FLASHCARD ---
st.title(f"{aula_sel}")
st.write(f"**{dia_sel}** | {bloco_sel}")

with st.container(border=True):
    # Lado A: O Termo (Sempre Visível)
    st.markdown(f"<h1 style='text-align: center; font-size: 60px; color: #1E3A8A;'>{card['t']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #666;'>Pronúncia: /{card.get('p', '')}/</p>", unsafe_allow_html=True)
    
    # Botão de Áudio
    if st.button("🔊 Ouvir Pronúncia", use_container_width=True):
        texto_falar = card['t'].split('→')[-1].strip()
        tts = gTTS(text=texto_falar, lang='en')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        st.audio(fp, format='audio/mp3')

    st.divider()

    # Lado B: Revelação (Tradução e Exemplo)
    if not st.session_state[reveal_key]:
        if st.button("🔍 REVELAR RESPOSTA", type="primary", use_container_width=True):
            st.session_state[reveal_key] = True
            st.rerun()
    else:
        # Conteúdo Revelado
        st.markdown(f"### 🇧🇷 Tradução: {card.get('tr', '---')}")
        if 'ex' in card:
            st.markdown(f"**Exemplo:** *{card['ex']}*")
        
        if st.button("🙈 Esconder Resposta", use_container_width=True):
            st.session_state[reveal_key] = False
            st.rerun()

# Navegação
st.write("")
nav_col1, nav_col2, nav_col3 = st.columns([1, 2, 1])

with nav_col1:
    if st.button("⬅️ Anterior", use_container_width=True) and idx > 0:
        st.session_state[idx_key] -= 1
        st.session_state[reveal_key] = False # Esconde a resposta ao mudar
        st.rerun()

with nav_col3:
    if st.button("Próximo ➡️", use_container_width=True) and idx < len(lista_cards) - 1:
        st.session_state[idx_key] += 1
        st.session_state[reveal_key] = False # Esconde a resposta ao mudar
        st.rerun()

# Barra de Progresso
st.divider()
st.progress((idx + 1) / len(lista_cards))
st.write(f"Progresso: {idx + 1} de {len(lista_cards)}")
