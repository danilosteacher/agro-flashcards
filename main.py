import streamlit as st
from gtts import gTTS
import io

# Configuração da página
st.set_page_config(
    page_title="Talk Agribusiness - Flashcards",
    page_icon="🚜",
    layout="centered"
)

# -------------------------
# FUNÇÃO DE GERAÇÃO DE ÁUDIO (COM CACHE)
# -------------------------
@st.cache_data
def gerar_audio(texto):
    tts = gTTS(text=texto, lang="en")
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp.read()


# -------------------------
# BANCO DE DADOS
# -------------------------
data = {
    "Aula 14: Corporate & Logistics": {
        "DAY 1: The Story + Sarah's Email": {
            "Vocabulary": [
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
            ]
        }
    },

    "Aula 15: Past & Projects": {
        "DAY 1: Monday Meeting": {
            "Vocabulary": [
                {"t": "work → worked", "p": "wɜːrkt", "tr": "trabalhar / trabalhou", "ex": "I worked in the field all day yesterday."},
                {"t": "call → called", "p": "kɔːld", "tr": "ligar / ligou", "ex": "She called the supplier to check the order."},
                {"t": "email → emailed", "p": "ˈeɪmeɪld", "tr": "enviar email / enviou email", "ex": "I emailed the logistics department."},
                {"t": "finish → finished", "p": "ˈfɪnɪʃt", "tr": "terminar / terminou", "ex": "We finished the report before 5 PM."},
                {"t": "prepare → prepared", "p": "prɪˈperd", "tr": "preparar / preparou", "ex": "They prepared the presentation for the board."},
                {"t": "talk → talked", "p": "tɔːkt", "tr": "conversar / conversou", "ex": "We talked about the new budget."},
                {"t": "report", "p": "rɪˈpɔːrt", "tr": "relatório", "ex": "The sales report is on your desk."},
                {"t": "client", "p": "ˈklaɪənt", "tr": "cliente", "ex": "The client is waiting in the lobby."},
                {"t": "meeting", "p": "ˈmiːtɪŋ", "tr": "reunião", "ex": "The meeting starts in ten minutes."},
                {"t": "team", "p": "tiːm", "tr": "equipe", "ex": "Our team won the safety award."},
                {"t": "manager", "p": "ˈmænɪdʒər", "tr": "gerente", "ex": "The manager approved the travel expenses."},
                {"t": "project", "p": "ˈprɒdʒekt", "tr": "projeto", "ex": "The irrigation project is almost complete."}
            ]
        }
    }
}

# -------------------------
# SIDEBAR
# -------------------------
st.sidebar.title("🚜 Talk Agribusiness")

aula_sel = st.sidebar.selectbox(
    "Escolha a Aula:",
    list(data.keys())
)

dia_sel = st.sidebar.selectbox(
    "Escolha o Dia:",
    list(data[aula_sel].keys())
)

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

        if st.button("🔄 REVELAR TRADUÇÃO & EXEMPLO", use_container_width=True):
            st.session_state[flip_key] = True
            st.rerun()

    else:

        st.markdown(
            f"<h2 style='text-align:center;color:#2E7D32'>{card['tr']}</h2>",
            unsafe_allow_html=True
        )

        st.divider()

        st.markdown("**Exemplo de uso:**")
        st.write(f"*{card.get('ex','')}*")

        if st.button("⬅️ VOLTAR PARA O TERMO", use_container_width=True):
            st.session_state[flip_key] = False
            st.rerun()

    # -------------------------
    # BOTÃO DE ÁUDIO
    # -------------------------
    if st.button("🔊 OUVIR PRONÚNCIA", use_container_width=True):

        texto_limpo = card["t"].split("→")[-1].strip()

        audio_bytes = gerar_audio(texto_limpo)

        st.audio(audio_bytes, format="audio/mp3")


# -------------------------
# NAVEGAÇÃO
# -------------------------
col1, col2, col3 = st.columns([1,2,1])

with col1:
    if st.button("Anterior", use_container_width=True) and idx > 0:
        st.session_state[idx_key] -= 1
        st.session_state[flip_key] = False
        st.rerun()

with col3:
    if st.button("Próximo", use_container_width=True) and idx < len(lista_cards)-1:
        st.session_state[idx_key] += 1
        st.session_state[flip_key] = False
        st.rerun()

# -------------------------
# PROGRESSO
# -------------------------
st.divider()

st.progress((idx + 1) / len(lista_cards))

st.write(f"Card {idx + 1} de {len(lista_cards)}")
