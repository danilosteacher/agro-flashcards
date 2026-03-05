import streamlit as st
from gtts import gTTS
import io

# Configuração de Identidade Visual
st.set_page_config(page_title="Talk Agribusiness - Flashcards", page_icon="🚜", layout="centered")

# --- BANCO DE DADOS ATUALIZADO (Aula 14) ---
data = {
    "Aula 14: Corporate & Logistics": {
        "DAY 1: The Story + Sarah's Email": {
            "Vocabulary": [
                {"t": "quarterly", "p": "ˈkwɔːrtərli", "tr": "trimestral"},
                {"t": "results", "p": "rɪˈzʌlts", "tr": "resultados"},
                {"t": "available", "p": "əˈveɪləbl", "tr": "disponível"},
                {"t": "desk", "p": "desk", "tr": "mesa de trabalho"},
                {"t": "busy", "p": "ˈbɪzi", "tr": "ocupado/a"},
                {"t": "late", "p": "leɪt", "tr": "atrasado/a"},
                {"t": "absent", "p": "ˈæbsənt", "tr": "ausente"},
                {"t": "building", "p": "ˈbɪldɪŋ", "tr": "prédio / edifício"},
                {"t": "reports", "p": "rɪˈpɔːrts", "tr": "relatórios"},
                {"t": "meeting", "p": "ˈmiːtɪŋ", "tr": "reunião"},
                {"t": "team", "p": "tiːm", "tr": "equipe"},
                {"t": "nobody", "p": "ˈnoʊbədi", "tr": "ninguém"}
            ]
        },
        "DAY 2: Grammar + Drills": {
            "Vocabulary": [
                {"t": "ready", "p": "ˈredi", "tr": "pronto/a"},
                {"t": "on time", "p": "ɒn taɪm", "tr": "no horário"},
                {"t": "in the office", "p": "ɪn ðə ˈɒfɪs", "tr": "no escritório"},
                {"t": "in the meeting", "p": "ɪn ðə ˈmiːtɪŋ", "tr": "na reunião"},
                {"t": "at work", "p": "æt wɜːrk", "tr": "no trabalho"},
                {"t": "in the morning", "p": "ɪn ðə ˈmɔːrnɪŋ", "tr": "de manhã"},
                {"t": "in the afternoon", "p": "ɪn ðə ˌæftərˈnuːn", "tr": "à tarde"},
                {"t": "manager", "p": "ˈmænɪdʒər", "tr": "gerente"},
                {"t": "colleague", "p": "ˈkɒliːɡ", "tr": "colega"},
                {"t": "available by phone", "p": "əˈveɪləbl baɪ foʊn", "tr": "disponível por telefone"},
                {"t": "out of office", "p": "aʊt əv ˈɒfɪs", "tr": "fora do escritório"},
                {"t": "on a business trip", "p": "ɒn ə ˈbɪznəs trɪp", "tr": "em viagem de negócios"}
            ]
        },
        "DAY 3: Drills + Time Expressions": {
            "Vocabulary": [
                {"t": "yesterday", "p": "ˈjestərdeɪ", "tr": "ontem"},
                {"t": "last week", "p": "lɑːst wiːk", "tr": "semana passada"},
                {"t": "last Friday", "p": "lɑːst ˈfraɪdeɪ", "tr": "última sexta-feira"},
                {"t": "two days ago", "p": "tuː deɪz əˈɡoʊ", "tr": "dois dias atrás"},
                {"t": "yesterday morning", "p": "ˈjestərdeɪ ˈmɔːrnɪŋ", "tr": "ontem de manhã"},
                {"t": "yesterday afternoon", "p": "ˈjestərdeɪ ˌæftərˈnuːn", "tr": "ontem à tarde"},
                {"t": "at that time", "p": "æt ðæt taɪm", "tr": "naquele momento"},
                {"t": "on Monday", "p": "ɒn ˈmʌndeɪ", "tr": "na segunda-feira"},
                {"t": "at 3 PM", "p": "æt θriː piː em", "tr": "às 15h"},
                {"t": "in 2023", "p": "ɪn ˈtwenti ˈtwenti θriː", "tr": "em 2023"},
                {"t": "a week ago", "p": "ə wiːk əˈɡoʊ", "tr": "uma semana atrás"},
                {"t": "last month", "p": "lɑːst mʌnθ", "tr": "mês passado"}
            ]
        },
        "DAY 4: Audios 1-4": {
            "Vocabulary": [
                {"t": "conference", "p": "ˈkɒnfərəns", "tr": "conferência"},
                {"t": "presentation", "p": "ˌpreznˈteɪʃn", "tr": "apresentação"},
                {"t": "sales team", "p": "seɪlz tiːm", "tr": "equipe de vendas"},
                {"t": "financial reports", "p": "faɪˈnænʃl rɪˈpɔːrts", "tr": "relatórios financeiros"},
                {"t": "voicemail", "p": "ˈvɔɪsmeɪl", "tr": "caixa de mensagens"},
                {"t": "data center", "p": "ˈdeɪtə ˈsentər", "tr": "centro de dados"},
                {"t": "server emergency", "p": "ˈsɜːrvər iˈmɜːrdʒənsi", "tr": "emergência no servidor"},
                {"t": "production issue", "p": "prəˈdʌkʃn ˈɪʃuː", "tr": "problema de produção"},
                {"t": "loan meeting", "p": "loʊn ˈmiːtɪŋ", "tr": "reunião de empréstimo"},
                {"t": "on the road", "p": "ɒn ðə roʊd", "tr": "em campo / a caminho"},
                {"t": "scheduling conflict", "p": "ˈskedʒuːlɪŋ ˈkɒnflɪkt", "tr": "conflito de agenda"},
                {"t": "company-wide", "p": "ˈkʌmpəni waɪd", "tr": "para toda a empresa"}
            ]
        },
        "DAY 5: Personal Production": {
            "Vocabulary": [
                {"t": "whereabouts", "p": "ˈwerəbaʊts", "tr": "paradeiro"},
                {"t": "accountability", "p": "əˌkaʊntəˈbɪləti", "tr": "responsabilidade"},
                {"t": "justify", "p": "ˈdʒʌstɪfaɪ", "tr": "justificar"},
                {"t": "absence", "p": "ˈæbsəns", "tr": "ausência"},
                {"t": "explanation", "p": "ˌekspləˈneɪʃn", "tr": "explicação"},
                {"t": "location", "p": "loʊˈkeɪʃn", "tr": "localização"},
                {"t": "headquarters", "p": "ˈhedkwɔːrtərz", "tr": "sede da empresa"},
                {"t": "branch", "p": "bræntʃ", "tr": "filial"},
                {"t": "department", "p": "dɪˈpɑːrtmənt", "tr": "departamento"},
                {"t": "floor", "p": "flɔːr", "tr": "andar"},
                {"t": "boardroom", "p": "ˈbɔːrdruːm", "tr": "sala executiva"},
                {"t": "factory", "p": "ˈfæktri", "tr": "fábrica"}
            ]
        }
    }
}

# --- LÓGICA DO MOTOR ---
st.sidebar.title("🚜 Talk Agribusiness")
aula_sel = st.sidebar.selectbox("Escolha a Aula:", list(data.keys()))
dia_sel = st.sidebar.selectbox("Escolha o Dia:", list(data[aula_sel].keys()))

lista_cards = data[aula_sel][dia_sel]["Vocabulary"]

# Estado de Sessão para Navegação e Flip
idx_key = f"{aula_sel}_{dia_sel}_idx"
flipped_key = f"{aula_sel}_{dia_sel}_flipped"

if idx_key not in st.session_state:
    st.session_state[idx_key] = 0
if flipped_key not in st.session_state:
    st.session_state[flipped_key] = False

idx = st.session_state[idx_key]
card = lista_cards[idx]

# --- INTERFACE ---
st.title("Flashcards de Pronúncia")
st.caption(f"Foco: {dia_sel}")

# Container do Flashcard
with st.container(border=True):
    if not st.session_state[flipped_key]:
        # FRENTE DO CARD
        st.markdown(f"<h1 style='text-align: center; font-size: 65px; height: 150px; display: flex; align-items: center; justify-content: center;'>{card['t']}</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; color: gray;'>/{card['p']}/</p>", unsafe_allow_html=True)
        
        if st.button("🔄 VER TRADUÇÃO (FLIP)", type="primary", use_container_width=True):
            st.session_state[flipped_key] = True
            st.rerun()
    else:
        # VERSO DO CARD (FLIPPED)
        st.markdown(f"<h1 style='text-align: center; font-size: 50px; color: #2E7D32; height: 150px;'>{card['tr']}</h1>", unsafe_allow_html=True)
        st.write("")
        if st.button("⬅️ VER TERMO EM INGLÊS", use_container_width=True):
            st.session_state[flipped_key] = False
            st.rerun()

    # Botão de Áudio (Sempre disponível)
    if st.button("🔊 OUVIR PRONÚNCIA", use_container_width=True):
        tts = gTTS(text=card['t'], lang='en')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        st.audio(fp, format='audio/mp3')

# Navegação Inferior
col1, col2, col3 = st.columns([1,2,1])
with col1:
    if st.button("Anterior", use_container_width=True) and idx > 0:
        st.session_state[idx_key] -= 1
        st.session_state[flipped_key] = False
        st.rerun()
with col3:
    if st.button("Próximo", use_container_width=True) and idx < len(lista_cards) - 1:
        st.session_state[idx_key] += 1
        st.session_state[flipped_key] = False
        st.rerun()

# Barra de Progresso Profissional
st.divider()
st.progress((idx + 1) / len(lista_cards))
st.write(f"Card {idx + 1} de {len(lista_cards)}")
