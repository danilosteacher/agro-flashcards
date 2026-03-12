import streamlit as st
from gtts import gTTS
import io
import base64

# -------------------------
# CONFIGURAÇÃO DA PÁGINA
# -------------------------
st.set_page_config(
    page_title="Talk Agribusiness - Flashcards",
    page_icon="🚜",
    layout="centered"
)

# -------------------------
# FUNÇÃO DE ÁUDIO
# -------------------------
@st.cache_data
def gerar_audio(texto):
    tts = gTTS(text=texto, lang="en")
    
    mp3_fp = io.BytesIO()
    tts.write_to_fp(mp3_fp)
    
    mp3_fp.seek(0)
    
    return mp3_fp.read()


def tocar_audio(audio_bytes):
    b64 = base64.b64encode(audio_bytes).decode()
    
    audio_html = f"""
        <audio controls autoplay>
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
    """
    
    st.markdown(audio_html, unsafe_allow_html=True)


# -------------------------
# BANCO DE DADOS
# -------------------------
data = {
    "Aula 14: Corporate & Logistics": {
        "DAY 1": {
            "Vocabulary": [
                {"t": "quarterly", "p": "ˈkwɔːrtərli", "tr": "trimestral", "ex": "We need to review the quarterly results."},
                {"t": "results", "p": "rɪˈzʌlts", "tr": "resultados", "ex": "The harvest results were better than expected."},
                {"t": "available", "p": "əˈveɪləbl", "tr": "disponível", "ex": "Is the manager available for a call?"},
                {"t": "desk", "p": "desk", "tr": "mesa de trabalho", "ex": "He left the documents on my desk."},
                {"t": "busy", "p": "ˈbɪzi", "tr": "ocupado", "ex": "I am very busy with the export logistics."}
            ]
        }
    },

    "Aula 15: Past & Projects": {
        "DAY 1": {
            "Vocabulary": [
                {"t": "work → worked", "p": "wɜːrkt", "tr": "trabalhar / trabalhou", "ex": "I worked in the field yesterday."},
                {"t": "call → called", "p": "kɔːld", "tr": "ligar / ligou", "ex": "She called the supplier."},
                {"t": "email → emailed", "p": "ˈeɪmeɪld", "tr": "enviar email / enviou email", "ex": "I emailed the logistics department."}
            ]
        }
    }
}

# -------------------------
# SIDEBAR
# -------------------------
st.sidebar.title("🚜 Talk Agribusiness")

aula_sel = st.sidebar.selectbox("Escolha a Aula:", list(data.keys()))
dia_sel = st.sidebar.selectbox("Escolha o Dia:", list(data[aula_sel].keys()))

lista_cards = data[aula_sel][dia_sel]["Vocabulary"]

# -------------------------
# SESSION STATE
# -------------------------
idx_key = f"{aula_sel}_{dia_sel}_idx"
flip_key = f"{aula_sel}_{dia_sel}_flip"

if idx_key not in st.session_state:
    st.session_state[idx_key] = 0

if flip_key not in st.session_state:
    st.session_state[flip_key] = False

idx = st.session_state[idx_key]
card = lista_cards[idx]

# -------------------------
# INTERFACE
# -------------------------
st.title("Flashcards: Pronúncia & Contexto")
st.caption(f"Foco: {dia_sel}")

with st.container(border=True):

    if not st.session_state[flip_key]:

        st.markdown(
            f"<h1 style='text-align:center;font-size:55px;height:160px;display:flex;align-items:center;justify-content:center'>{card['t']}</h1>",
            unsafe_allow_html=True
        )

        st.markdown(
            f"<p style='text-align:center;color:gray;font-size:20px'>/{card.get('p','')}/</p>",
            unsafe_allow_html=True
        )

        if st.button("🔄 REVELAR TRADUÇÃO & EXEMPLO"):
            st.session_state[flip_key] = True
            st.rerun()

    else:

        st.markdown(
            f"<h2 style='text-align:center;color:#2E7D32'>{card['tr']}</h2>",
            unsafe_allow_html=True
        )

        st.write("**Exemplo:**")
        st.write(card["ex"])

        if st.button("⬅️ VOLTAR"):
            st.session_state[flip_key] = False
            st.rerun()

    # -------------------------
    # BOTÃO DE ÁUDIO
    # -------------------------
    if st.button("🔊 OUVIR PRONÚNCIA"):

        texto_limpo = card["t"].split("→")[-1].strip()

        audio_bytes = gerar_audio(texto_limpo)

        tocar_audio(audio_bytes)


# -------------------------
# NAVEGAÇÃO
# -------------------------
col1, col2, col3 = st.columns([1,2,1])

with col1:
    if st.button("Anterior") and idx > 0:
        st.session_state[idx_key] -= 1
        st.session_state[flip_key] = False
        st.rerun()

with col3:
    if st.button("Próximo") and idx < len(lista_cards)-1:
        st.session_state[idx_key] += 1
        st.session_state[flip_key] = False
        st.rerun()

st.divider()

st.progress((idx + 1) / len(lista_cards))

st.write(f"Card {idx + 1} de {len(lista_cards)}")
