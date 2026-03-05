import streamlit as st
from gtts import gTTS
import io

# Configuração de Página e Estética Profissional
st.set_page_config(page_title="Talk Agribusiness - Flashcards", page_icon="🚜", layout="wide")

# --- BANCO DE DADOS (Área de Gestão de Conteúdo) ---
# Para adicionar a Aula 15, basta criar um novo bloco abaixo da Aula 14
data = {
    "Aula 14: Past & Business": {
        "Dia 1: Verbs & Time": {
            "BLOCK A: Verbs (Past)": [
                {"t": "work → worked", "p": "wɜːrkt"},
                {"t": "call → called", "p": "kɔːld"},
                {"t": "email → emailed", "p": "ˈeɪmeɪld"},
                {"t": "finish → finished", "p": "fɪnɪʃt"},
                {"t": "schedule → scheduled", "p": "skedʒuːld"},
                {"t": "prepare → prepared", "p": "prɪˈperd"},
                {"t": "check → checked", "p": "tʃekt"},
                {"t": "talk → talked", "p": "tɔːkt"},
                {"t": "present → presented", "p": "prɪˈzentɪd"},
                {"t": "help → helped", "p": "helpt"},
                {"t": "visit → visited", "p": "vɪzɪtɪd"},
                {"t": "explain → explained", "p": "ɪkˈspleɪnd"},
                {"t": "discuss → discussed", "p": "dɪˈskʌst"},
                {"t": "complete → completed", "p": "kəmˈpliːtɪd"},
                {"t": "confirm → confirmed", "p": "kənˈfɜːrmd"},
                {"t": "clean → cleaned", "p": "kliːnd"},
                {"t": "watch → watched", "p": "wɒtʃt"},
                {"t": "walk → walked", "p": "wɔːkt"},
                {"t": "need → needed", "p": "ˈniːdɪd"},
                {"t": "want → wanted", "p": "ˈwɒntɪd"}
            ],
            "BLOCK B: Time Expressions": [
                {"t": "yesterday", "p": "ˈjestədeɪ"},
                {"t": "yesterday morning", "p": "ˈjestədeɪ ˈmɔːrnɪŋ"},
                {"t": "last week", "p": "lɑːst wiːk"},
                {"t": "last month", "p": "lɑːst mʌnθ"},
                {"t": "two days ago", "p": "tuː deɪz əˈɡəʊ"},
                {"t": "this morning", "p": "ðɪs ˈmɔːrnɪŋ"}
            ]
        },
        "Dia 2: Business Vocab": {
            "BLOCK C: Management": [
                {"t": "report", "p": "rɪˈpɔːrt", "tr": "relatório"},
                {"t": "client", "p": "ˈklaɪənt", "tr": "cliente"},
                {"t": "meeting", "p": "ˈmiːtɪŋ", "tr": "reunião"},
                {"t": "supplier", "p": "səˈplaɪər", "tr": "fornecedor"},
                {"t": "deadline", "p": "ˈdedlaɪn", "tr": "prazo"},
                {"t": "budget", "p": "ˈbʌdʒɪt", "tr": "orçamento"},
                {"t": "proposal", "p": "prəˈpəʊzəl", "tr": "proposta"}
            ]
        },
        "Dia 3: Phrases": {
            "BLOCK D: Professional Expressions": [
                {"t": "On time", "p": "ɒn taɪm", "tr": "No prazo / pontualmente"},
                {"t": "Great teamwork!", "p": "ɡreɪt ˈtiːmwɜːrk", "tr": "Ótimo trabalho em equipe!"},
                {"t": "I finished it before lunch", "p": "bɪˈfɔːr lʌntʃ", "tr": "Terminei antes do almoço"},
                {"t": "The project is ready", "p": "ˈprɒdʒekt ɪz ˈredi", "tr": "O projeto está pronto"}
            ]
        },
        "Dia 4: Structures": {
            "BLOCK E: Question Words": [
                {"t": "What", "p": "wɒt", "tr": "O que"},
                {"t": "When", "p": "wen", "tr": "Quando"},
                {"t": "Where", "p": "weər", "tr": "Onde"},
                {"t": "Did", "p": "dɪd", "tr": "Auxiliar para perguntas no passado"}
            ]
        },
        "Dia 5: Full Review": {
            "Review All": [
                {"t": "I called three clients", "p": "kɔːld θriː ˈklaɪənts", "tr": "Liguei para três clientes"},
                {"t": "We worked together", "p": "wɜːrkt təˈɡeðər", "tr": "Trabalhamos juntos"},
                {"t": "Update", "p": "ʌpˈdeɪt", "tr": "Atualização"}
            ]
        }
    }
}

# --- INTERFACE E LOGICA (O MOTOR) ---
st.sidebar.header("🚜 Talk Agribusiness")
st.sidebar.subheader("Menu de Estudo")

# Seletores Hierárquicos
aula_sel = st.sidebar.selectbox("Selecione a Aula:", list(data.keys()))
dia_sel = st.sidebar.selectbox("Selecione o Dia:", list(data[aula_sel].keys()))
bloco_sel = st.sidebar.selectbox("Selecione o Bloco:", list(data[aula_sel][dia_sel].keys()))

lista_cards = data[aula_sel][dia_sel][bloco_sel]

# Controle de Navegação (Preserva o índice para cada bloco)
state_key = f"{aula_sel}_{dia_sel}_{bloco_sel}_idx"
if state_key not in st.session_state:
    st.session_state[state_key] = 0

idx = st.session_state[state_key]
card = lista_cards[idx]

# --- EXIBIÇÃO ---
st.title(f"{aula_sel}")
st.markdown(f"**{dia_sel}** | {bloco_sel}")

with st.container(border=True):
    # Card Principal
    st.markdown(f"<h1 style='text-align: center; font-size: 50px;'>{card['t']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #666;'>Pronúncia: /{card.get('p', '')}/</p>", unsafe_allow_html=True)
    
    st.divider()
    
    # Botões de Ação
    col_audio, col_trad = st.columns(2)
    
    with col_audio:
        if st.button("🔊 Ouvir Áudio", use_container_width=True):
            # Limpa o texto (pega só depois da seta se houver)
            texto_falar = card['t'].split('→')[-1].strip()
            tts = gTTS(text=texto_falar, lang='en')
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            st.audio(fp, format='audio/mp3')
            
    with col_trad:
        if 'tr' in card:
            if st.button("🔍 Ver Tradução", use_container_width=True):
                st.success(f"**Tradução:** {card['tr']}")
        else:
            st.button("🔍 Sem tradução disponível", disabled=True, use_container_width=True)

# Navegação entre Cards
st.write("")
nav_col1, nav_col2, nav_col3 = st.columns([1, 2, 1])

with nav_col1:
    if st.button("⬅️ Anterior", use_container_width=True) and idx > 0:
        st.session_state[state_key] -= 1
        st.rerun()

with nav_col3:
    if st.button("Próximo ➡️", use_container_width=True) and idx < len(lista_cards) - 1:
        st.session_state[state_key] += 1
        st.rerun()

# Progresso
st.divider()
progresso = (idx + 1) / len(lista_cards)
st.progress(progresso)
st.write(f"Você estudou {idx + 1} de {len(lista_cards)} termos deste bloco.")
