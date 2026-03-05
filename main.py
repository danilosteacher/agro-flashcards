import streamlit as st
from gtts import gTTS
import io

st.set_page_config(page_title="Agro English Flashcards", page_icon="🚜")

st.title("🚜 Agro English Flashcards")
st.write("Melhore sua pronúncia técnica no agronegócio.")

# Banco de dados simples (Você pode expandir isso depois)
cards = [
    {"termo": "Crop rotation", "traducao": "Rotação de culturas"},
    {"termo": "Livestock management", "traducao": "Manejo de gado"},
    {"termo": "Yield monitor", "traducao": "Monitor de produtividade"},
    {"termo": "Soil fertility", "traducao": "Fertilidade do solo"}
]

if 'indice' not in st.session_state:
    st.session_state.indice = 0

card_atual = cards[st.session_state.indice]

# Interface do Card
with st.container():
    st.subheader(f"Termo: {card_atual['termo']}")
    
    if st.button("Revelar Tradução"):
        st.info(f"Tradução: {card_atual['traducao']}")

    # Gerar Áudio via Google TTS
    if st.button("Ouvir Pronúncia"):
        tts = gTTS(text=card_atual['termo'], lang='en')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        st.audio(fp, format='audio/mp3')

# Navegação
col1, col2 = st.columns(2)
with col1:
    if st.button("Anterior") and st.session_state.indice > 0:
        st.session_state.indice -= 1
        st.rerun()
with col2:
    if st.button("Próximo") and st.session_state.indice < len(cards) - 1:
        st.session_state.indice += 1
        st.rerun()
