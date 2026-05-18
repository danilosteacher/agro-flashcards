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
# CSS CUSTOMIZADO
# -------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Remove Streamlit default padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 720px;
    }

    /* Hide Streamlit header/footer */
    header[data-testid="stHeader"] { display: none; }
    footer { display: none; }
    #MainMenu { display: none; }

    /* ---- Sidebar ---- */
    [data-testid="stSidebar"] {
        background: #0d1117;
        border-right: 1px solid #1e2530;
    }
    [data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }
    [data-testid="stSidebar"] .stSelectbox label {
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #64748b !important;
        margin-bottom: 4px;
    }
    [data-testid="stSidebar"] [data-baseweb="select"] > div {
        background: #1a2233 !important;
        border: 1px solid #2a3548 !important;
        border-radius: 10px !important;
        color: #e2e8f0 !important;
    }
    [data-testid="stSidebar"] [data-baseweb="select"] > div:hover {
        border-color: #3b82f6 !important;
    }

    /* Sidebar title */
    .sidebar-logo {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 0 0 24px 0;
        border-bottom: 1px solid #1e2530;
        margin-bottom: 20px;
    }
    .sidebar-logo-icon {
        width: 36px;
        height: 36px;
        background: linear-gradient(135deg, #3b82f6, #1d4ed8);
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
    }
    .sidebar-logo-text {
        font-weight: 700;
        font-size: 15px;
        color: #f8fafc;
        line-height: 1.2;
    }
    .sidebar-logo-sub {
        font-size: 11px;
        color: #64748b;
        font-weight: 400;
    }

    /* ---- Main area header ---- */
    .page-header {
        margin-bottom: 28px;
    }
    .page-title {
        font-size: 22px;
        font-weight: 700;
        color: #0f172a;
        letter-spacing: -0.3px;
        margin: 0 0 4px 0;
    }
    .page-subtitle {
        font-size: 13px;
        color: #64748b;
        font-weight: 400;
        margin: 0;
    }

    /* ---- Progress bar ---- */
    .progress-wrap {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 24px;
    }
    .progress-track {
        flex: 1;
        height: 4px;
        background: #e2e8f0;
        border-radius: 99px;
        overflow: hidden;
    }
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #3b82f6, #1d4ed8);
        border-radius: 99px;
        transition: width 0.4s ease;
    }
    .progress-label {
        font-size: 12px;
        font-weight: 600;
        color: #94a3b8;
        white-space: nowrap;
    }

    /* ---- Flashcard ---- */
    .flashcard {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 20px;
        padding: 48px 40px;
        text-align: center;
        min-height: 260px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 12px;
        margin-bottom: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 8px 24px rgba(0,0,0,0.04);
        position: relative;
        overflow: hidden;
    }
    .flashcard::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, #3b82f6, #8b5cf6);
    }
    .card-term {
        font-size: 42px;
        font-weight: 700;
        color: #0f172a;
        letter-spacing: -1px;
        line-height: 1.2;
        margin: 0;
    }
    .card-term-long {
        font-size: 22px;
        font-weight: 600;
        color: #0f172a;
        letter-spacing: -0.3px;
        line-height: 1.4;
        margin: 0;
    }
    .card-phonetic {
        font-size: 16px;
        color: #94a3b8;
        font-weight: 400;
        margin: 0;
        font-style: italic;
    }
    .card-flip-hint {
        font-size: 12px;
        color: #cbd5e1;
        font-weight: 500;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin-top: 8px;
    }

    /* Flashcard — back side */
    .flashcard-back {
        background: #f8faff;
        border-color: #dbeafe;
    }
    .flashcard-back::before {
        background: linear-gradient(90deg, #10b981, #3b82f6);
    }
    .card-translation {
        font-size: 28px;
        font-weight: 700;
        color: #1e40af;
        letter-spacing: -0.3px;
        margin: 0;
    }
    .card-translation-long {
        font-size: 18px;
        font-weight: 600;
        color: #1e40af;
        line-height: 1.4;
        margin: 0;
    }
    .card-example-label {
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #94a3b8;
        margin: 8px 0 4px 0;
    }
    .card-example {
        font-size: 17px;
        color: #334155;
        font-weight: 400;
        font-style: italic;
        line-height: 1.5;
        margin: 0;
        max-width: 480px;
    }

    /* ---- Buttons ---- */
    .stButton > button {
        border-radius: 12px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        transition: all 0.18s ease !important;
        border: 1.5px solid !important;
        padding: 10px 20px !important;
        height: auto !important;
        line-height: 1.4 !important;
    }

    /* Primary buttons (reveal/back) */
    div[data-testid="stVerticalBlock"] > div:nth-child(1) .stButton > button,
    .reveal-btn .stButton > button {
        background: #1d4ed8 !important;
        color: #ffffff !important;
        border-color: #1d4ed8 !important;
        width: 100% !important;
        padding: 14px 24px !important;
        font-size: 15px !important;
        border-radius: 14px !important;
    }
    div[data-testid="stVerticalBlock"] > div:nth-child(1) .stButton > button:hover {
        background: #1e40af !important;
        border-color: #1e40af !important;
        transform: translateY(-1px);
    }

    /* Audio button */
    .audio-btn .stButton > button {
        background: transparent !important;
        color: #3b82f6 !important;
        border-color: #bfdbfe !important;
        width: 100% !important;
    }
    .audio-btn .stButton > button:hover {
        background: #eff6ff !important;
        border-color: #93c5fd !important;
    }

    /* Nav buttons */
    .nav-btn .stButton > button {
        background: transparent !important;
        color: #475569 !important;
        border-color: #e2e8f0 !important;
        width: 100% !important;
        padding: 12px 20px !important;
    }
    .nav-btn .stButton > button:hover {
        background: #f1f5f9 !important;
        border-color: #cbd5e1 !important;
        color: #0f172a !important;
    }
    .nav-btn .stButton > button:disabled {
        opacity: 0.35 !important;
        cursor: not-allowed !important;
    }

    /* ---- Badge / day chip ---- */
    .day-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #eff6ff;
        color: #1d4ed8;
        font-size: 12px;
        font-weight: 600;
        padding: 5px 12px;
        border-radius: 99px;
        border: 1px solid #bfdbfe;
        margin-bottom: 16px;
    }

    /* ---- Divider ---- */
    hr {
        border: none;
        border-top: 1px solid #f1f5f9;
        margin: 24px 0 !important;
    }

    /* Hide default streamlit progress */
    .stProgress { display: none; }
</style>
""", unsafe_allow_html=True)

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
"Método T.A.L.K - Week 1": {

    "DAY 1": {
        "Vocabulary": [
            {"t": "agronomist", "p": "əˈɡrɑːnəmɪst", "tr": "agrônomo/agrônoma", "ex": "She is an agronomist."},
            {"t": "veterinarian", "p": "ˌvetərɪˈneriən", "tr": "veterinário/veterinária", "ex": "He is a veterinarian."},
            {"t": "sales manager", "p": "seɪlz ˈmænɪdʒər", "tr": "gerente de vendas", "ex": "He is the sales manager."},
            {"t": "coordinator", "p": "koʊˈɔːrdɪneɪtər", "tr": "coordenador/coordenadora", "ex": "She is a coordinator."},
            {"t": "at the farm", "p": "æt ðə fɑːrm", "tr": "na fazenda", "ex": "He is at the farm today."},
            {"t": "at the office", "p": "æt ðə ˈɑːfɪs", "tr": "no escritório", "ex": "She is at the office."},
            {"t": "in the field", "p": "ɪn ðə fiːld", "tr": "no campo", "ex": "He is in the field."},
            {"t": "busy", "p": "ˈbɪzi", "tr": "ocupado/ocupada", "ex": "She is busy right now."},
            {"t": "ready", "p": "ˈredi", "tr": "pronto/pronta", "ex": "He is ready for the meeting."},
            {"t": "This is", "p": "ðɪs ɪz", "tr": "Este/Esta é (para apresentar alguém)", "ex": "This is Ana. She is an agronomist."}
        ]
    },
    "DAY 2": {
        "Vocabulary": [
            {"t": "technical analyst", "p": "ˈteknɪkl ˈænəlɪst", "tr": "analista técnico/a", "ex": "She is a technical analyst."},
            {"t": "field representative", "p": "fiːld ˌreprɪˈzentətɪv", "tr": "representante de campo", "ex": "He is a field representative."},
            {"t": "consultant", "p": "kənˈsʌltənt", "tr": "consultor/consultora", "ex": "He is a consultant."},
            {"t": "director", "p": "dəˈrektər", "tr": "diretor/diretora", "ex": "She is the director."},
            {"t": "at the branch", "p": "æt ðə bræntʃ", "tr": "na filial", "ex": "He is at the branch today."},
            {"t": "at the headquarters", "p": "æt ðə ˈhedkwɔːrtərz", "tr": "na matriz / sede", "ex": "They are at the headquarters."},
            {"t": "available", "p": "əˈveɪləbl", "tr": "disponível", "ex": "She is available for the meeting."},
            {"t": "in training", "p": "ɪn ˈtreɪnɪŋ", "tr": "em treinamento", "ex": "They are in training."},
            {"t": "These are", "p": "ðiːz ɑːr", "tr": "Estes/Estas são (para apresentar 2+ pessoas)", "ex": "These are Ana and Pedro."},
            {"t": "They are / They're", "p": "ðeɪ ɑːr / ðer", "tr": "Eles/Elas são / estão", "ex": "They are agronomists. They're ready."}
        ]
    },
    "DAY 3": {
        "Vocabulary": [
            {"t": "Is he...?", "p": "ɪz hiː", "tr": "Ele é / está...?", "ex": "Is he the manager?"},
            {"t": "Is she...?", "p": "ɪz ʃiː", "tr": "Ela é / está...?", "ex": "Is she at the farm?"},
            {"t": "Are they...?", "p": "ɑːr ðeɪ", "tr": "Eles/Elas são / estão...?", "ex": "Are they available?"},
            {"t": "Yes, he is.", "p": "jes hiː ɪz", "tr": "Sim, ele é / está.", "ex": "Is he ready? Yes, he is."},
            {"t": "Yes, she is.", "p": "jes ʃiː ɪz", "tr": "Sim, ela é / está.", "ex": "Is she the analyst? Yes, she is."},
            {"t": "No, he isn't.", "p": "noʊ hiː ˈɪznt", "tr": "Não, ele não é / está.", "ex": "Is he at the office? No, he isn't."},
            {"t": "No, they aren't.", "p": "noʊ ðeɪ ˈɑːrnt", "tr": "Não, eles/elas não são / estão.", "ex": "Are they ready? No, they aren't."},
            {"t": "and", "p": "ænd", "tr": "e (para adicionar informação)", "ex": "She is busy and she is at the farm."},
            {"t": "but", "p": "bʌt", "tr": "mas (para contrastar)", "ex": "He is busy, but he is ready."},
            {"t": "on a business trip", "p": "ɑːn ə ˈbɪznəs trɪp", "tr": "em viagem de trabalho", "ex": "She is on a business trip today."}
        ]
    },
    "DAY 4": {
        "Vocabulary": [
            {"t": "morning briefing", "p": "ˈmɔːrnɪŋ ˈbriːfɪŋ", "tr": "reunião matinal / briefing", "ex": "We have a morning briefing today."},
            {"t": "client", "p": "ˈklaɪənt", "tr": "cliente", "ex": "She is with the client."},
            {"t": "project", "p": "ˈprɑːdʒekt", "tr": "projeto", "ex": "He is ready for the project."},
            {"t": "in training", "p": "ɪn ˈtreɪnɪŋ", "tr": "em treinamento", "ex": "They are in training."},
            {"t": "fair", "p": "fer", "tr": "feira de negócios", "ex": "New Partners at the Fair."},
            {"t": "partner", "p": "ˈpɑːrtnər", "tr": "sócio / parceiro de negócios", "ex": "He is a partner from the USA."},
            {"t": "representative", "p": "ˌreprɪˈzentətɪv", "tr": "representante", "ex": "They are representatives."},
            {"t": "headquarters", "p": "ˈhedkwɔːrtərz", "tr": "matriz / sede da empresa", "ex": "They are from the headquarters."},
            {"t": "assistant", "p": "əˈsɪstənt", "tr": "assistente", "ex": "These are the assistants."},
            {"t": "Welcome to...", "p": "ˈwelkəm tuː", "tr": "Bem-vindo/a a...", "ex": "Welcome to the farm!"}
        ]
    },
    "DAY 5": {
        "Vocabulary": [
            {"t": "This is [name]. He/She is a [cargo].", "p": "", "tr": "Ao apresentar um colega individualmente", "ex": "This is Ana. She is a manager."},
            {"t": "These are [name] and [name]. They are [cargo].", "p": "", "tr": "Ao apresentar dois colegas juntos", "ex": "These are Ana and Pedro. They are engineers."},
            {"t": "He/She is from [city/team].", "p": "", "tr": "Ao dar a origem ou equipe da pessoa", "ex": "He is from the operations team."},
            {"t": "He/She is busy, but he/she is ready.", "p": "", "tr": "Ao mostrar disponibilidade apesar de ocupado", "ex": "She is busy, but she is ready."},
            {"t": "Is he/she available for the meeting?", "p": "", "tr": "Ao perguntar sobre disponibilidade", "ex": "Is he available for the meeting?"},
            {"t": "No, he/she isn't. He/She is at the farm.", "p": "", "tr": "Ao informar que alguém não está disponível", "ex": "No, she isn't. She is at the farm."},
            {"t": "They are ready for the project.", "p": "", "tr": "Ao confirmar que a equipe está pronta", "ex": "They are ready for the project."},
            {"t": "He/She is our specialist.", "p": "", "tr": "Ao destacar a expertise de um colega", "ex": "He is our specialist."},
            {"t": "They are from the [sales/technical/operations] team.", "p": "", "tr": "Ao indicar o departamento", "ex": "They are from the sales team."},
            {"t": "He/She is the right person for your project.", "p": "", "tr": "Ao recomendar um colega a um parceiro", "ex": "She is the right person for your project."}
        ]
    }
},
    "Método T.A.L.K - Week 2": {
    "DAY 1": {
        "Vocabulary": [
            {"t": "agronomist", "p": "əˈɡrɑːnəmɪst", "tr": "agrônomo/agrônoma", "ex": "She is an agronomist."},
            {"t": "veterinarian", "p": "ˌvetərɪˈneriən", "tr": "veterinário/veterinária", "ex": "He is a veterinarian."},
            {"t": "sales manager", "p": "seɪlz ˈmænɪdʒər", "tr": "gerente de vendas", "ex": "He is the sales manager."},
            {"t": "coordinator", "p": "koʊˈɔːrdɪneɪtər", "tr": "coordenador/coordenadora", "ex": "She is a coordinator."},
            {"t": "at the farm", "p": "æt ðə fɑːrm", "tr": "na fazenda", "ex": "He is at the farm today."},
            {"t": "at the office", "p": "æt ðə ˈɑːfɪs", "tr": "no escritório", "ex": "She is at the office."},
            {"t": "in the field", "p": "ɪn ðə fiːld", "tr": "no campo", "ex": "He is in the field."},
            {"t": "busy", "p": "ˈbɪzi", "tr": "ocupado/ocupada", "ex": "She is busy right now."},
            {"t": "ready", "p": "ˈredi", "tr": "pronto/pronta", "ex": "He is ready for the meeting."},
            {"t": "This is", "p": "ðɪs ɪz", "tr": "Este/Esta é (para apresentar alguém)", "ex": "This is Ana. She is an agronomist."}
        ]
    },
    "DAY 2": {
        "Vocabulary": [
            {"t": "technical analyst", "p": "ˈteknɪkl ˈænəlɪst", "tr": "analista técnico/a", "ex": "She is a technical analyst."},
            {"t": "field representative", "p": "fiːld ˌreprɪˈzentətɪv", "tr": "representante de campo", "ex": "He is a field representative."},
            {"t": "consultant", "p": "kənˈsʌltənt", "tr": "consultor/consultora", "ex": "He is a consultant."},
            {"t": "director", "p": "dəˈrektər", "tr": "diretor/diretora", "ex": "She is the director."},
            {"t": "at the branch", "p": "æt ðə bræntʃ", "tr": "na filial", "ex": "He is at the branch today."},
            {"t": "at the headquarters", "p": "æt ðə ˈhedkwɔːrtərz", "tr": "na matriz / sede", "ex": "They are at the headquarters."},
            {"t": "available", "p": "əˈveɪləbl", "tr": "disponível", "ex": "She is available for the meeting."},
            {"t": "in training", "p": "ɪn ˈtreɪnɪŋ", "tr": "em treinamento", "ex": "They are in training."},
            {"t": "These are", "p": "ðiːz ɑːr", "tr": "Estes/Estas são (para apresentar 2+ pessoas)", "ex": "These are Ana and Pedro."},
            {"t": "They are / They're", "p": "ðeɪ ɑːr / ðer", "tr": "Eles/Elas são / estão", "ex": "They are agronomists. They're ready."}
        ]
    },
    "DAY 3": {
        "Vocabulary": [
            {"t": "Is he...?", "p": "ɪz hiː", "tr": "Ele é / está...?", "ex": "Is he the manager?"},
            {"t": "Is she...?", "p": "ɪz ʃiː", "tr": "Ela é / está...?", "ex": "Is she at the farm?"},
            {"t": "Are they...?", "p": "ɑːr ðeɪ", "tr": "Eles/Elas são / estão...?", "ex": "Are they available?"},
            {"t": "Yes, he is.", "p": "jes hiː ɪz", "tr": "Sim, ele é / está.", "ex": "Is he ready? Yes, he is."},
            {"t": "Yes, she is.", "p": "jes ʃiː ɪz", "tr": "Sim, ela é / está.", "ex": "Is she the analyst? Yes, she is."},
            {"t": "No, he isn't.", "p": "noʊ hiː ˈɪznt", "tr": "Não, ele não é / está.", "ex": "Is he at the office? No, he isn't."},
            {"t": "No, they aren't.", "p": "noʊ ðeɪ ˈɑːrnt", "tr": "Não, eles/elas não são / estão.", "ex": "Are they ready? No, they aren't."},
            {"t": "and", "p": "ænd", "tr": "e (para adicionar informação)", "ex": "She is busy and she is at the farm."},
            {"t": "but", "p": "bʌt", "tr": "mas (para contrastar)", "ex": "He is busy, but he is ready."},
            {"t": "on a business trip", "p": "ɑːn ə ˈbɪznəs trɪp", "tr": "em viagem de trabalho", "ex": "She is on a business trip today."}
        ]
    },
    "DAY 4": {
        "Vocabulary": [
            {"t": "morning briefing", "p": "ˈmɔːrnɪŋ ˈbriːfɪŋ", "tr": "reunião matinal / briefing", "ex": "We have a morning briefing today."},
            {"t": "client", "p": "ˈklaɪənt", "tr": "cliente", "ex": "She is with the client."},
            {"t": "project", "p": "ˈprɑːdʒekt", "tr": "projeto", "ex": "He is ready for the project."},
            {"t": "in training", "p": "ɪn ˈtreɪnɪŋ", "tr": "em treinamento", "ex": "They are in training."},
            {"t": "fair", "p": "fer", "tr": "feira de negócios", "ex": "New Partners at the Fair."},
            {"t": "partner", "p": "ˈpɑːrtnər", "tr": "sócio / parceiro de negócios", "ex": "He is a partner from the USA."},
            {"t": "representative", "p": "ˌreprɪˈzentətɪv", "tr": "representante", "ex": "They are representatives."},
            {"t": "headquarters", "p": "ˈhedkwɔːrtərz", "tr": "matriz / sede da empresa", "ex": "They are from the headquarters."},
            {"t": "assistant", "p": "əˈsɪstənt", "tr": "assistente", "ex": "These are the assistants."},
            {"t": "Welcome to...", "p": "ˈwelkəm tuː", "tr": "Bem-vindo/a a...", "ex": "Welcome to the farm!"}
        ]
    },
    "DAY 5": {
        "Vocabulary": [
            {"t": "This is [name]. He/She is a [cargo].", "p": "", "tr": "Ao apresentar um colega individualmente", "ex": "This is Ana. She is a manager."},
            {"t": "These are [name] and [name]. They are [cargo].", "p": "", "tr": "Ao apresentar dois colegas juntos", "ex": "These are Ana and Pedro. They are engineers."},
            {"t": "He/She is from [city/team].", "p": "", "tr": "Ao dar a origem ou equipe da pessoa", "ex": "He is from the operations team."},
            {"t": "He/She is busy, but he/she is ready.", "p": "", "tr": "Ao mostrar disponibilidade apesar de ocupado", "ex": "She is busy, but she is ready."},
            {"t": "Is he/she available for the meeting?", "p": "", "tr": "Ao perguntar sobre disponibilidade", "ex": "Is he available for the meeting?"},
            {"t": "No, he/she isn't. He/She is at the farm.", "p": "", "tr": "Ao informar que alguém não está disponível", "ex": "No, she isn't. She is at the farm."},
            {"t": "They are ready for the project.", "p": "", "tr": "Ao confirmar que a equipe está pronta", "ex": "They are ready for the project."},
            {"t": "He/She is our specialist.", "p": "", "tr": "Ao destacar a expertise de um colega", "ex": "He is our specialist."},
            {"t": "They are from the [sales/technical/operations] team.", "p": "", "tr": "Ao indicar o departamento", "ex": "They are from the sales team."},
            {"t": "He/She is the right person for your project.", "p": "", "tr": "Ao recomendar um colega a um parceiro", "ex": "She is the right person for your project."}
        ]
    }
},

"Método T.A.L.K - Week 3": {
     
    "DAY 1": {
        "Vocabulary": [
            {"t": "available", "p": "əˈveɪləbl", "tr": "disponível", "ex": "The manager is available now."},
            {"t": "in a meeting", "p": "ɪn ə ˈmiːtɪŋ", "tr": "em uma reunião", "ex": "She is in a meeting with the client."},
            {"t": "on vacation", "p": "ɑːn veɪˈkeɪʃn", "tr": "de férias", "ex": "He is on vacation this week."},
            {"t": "in the office", "p": "ɪn ðə ˈɑːfɪs", "tr": "no escritório", "ex": "They are in the office."},
            {"t": "at home", "p": "æt hoʊm", "tr": "em casa", "ex": "I am working at home today."},
            {"t": "sales coordinator", "p": "seɪlz koʊˈɔːrdɪneɪtər", "tr": "coordenador(a) de vendas", "ex": "He is the new sales coordinator."},
            {"t": "engineer", "p": "ˌendʒɪˈnɪr", "tr": "engenheiro(a)", "ex": "She is an engineer."},
            {"t": "manager", "p": "ˈmænɪdʒər", "tr": "gerente", "ex": "The manager is in the field."},
            {"t": "boss", "p": "bɑːs", "tr": "chefe", "ex": "My boss is at a conference."},
            {"t": "team", "p": "tiːm", "tr": "equipe", "ex": "Our team is very busy."},
            {"t": "supervisor", "p": "ˈsuːpərvaɪzər", "tr": "supervisor(a)", "ex": "He is the shift supervisor."},
            {"t": "excited", "p": "ɪkˈsaɪtɪd", "tr": "animado(a)", "ex": "We are excited about the project."},
            {"t": "now", "p": "naʊ", "tr": "agora", "ex": "I am available now."},
            {"t": "right now", "p": "raɪt naʊ", "tr": "neste exato momento", "ex": "She is in a meeting right now."},
            {"t": "extension", "p": "ɪkˈstenʃn", "tr": "ramal", "ex": "My extension is 104."},
            {"t": "She is", "p": "ʃiː ɪz", "tr": "Ela é / está", "ex": "She is ready."},
            {"t": "He is", "p": "hiː ɪz", "tr": "Ele é / está", "ex": "He is in the office."},
            {"t": "They are", "p": "ðeɪ ɑːr", "tr": "Eles(as) são / estão", "ex": "They are at the farm."},
            {"t": "This is", "p": "ðɪs ɪz", "tr": "Este/Esta é", "ex": "This is my manager."}
        ]
    },
    "DAY 2": {
        "Vocabulary": [
            {"t": "He is not", "p": "hiː ɪz nɑːt", "tr": "Ele não é / não está", "ex": "He is not available."},
            {"t": "She is not", "p": "ʃiː ɪz nɑːt", "tr": "Ela não é / não está", "ex": "She is not in the office."},
            {"t": "They are not", "p": "ðeɪ ɑːr nɑːt", "tr": "Eles(as) não são / não estão", "ex": "They are not on vacation."},
            {"t": "Is she?", "p": "ɪz ʃiː", "tr": "Ela é / está?", "ex": "Is she the new engineer?"},
            {"t": "Is he?", "p": "ɪz hiː", "tr": "Ele é / está?", "ex": "Is he in a meeting?"},
            {"t": "Are they?", "p": "ɑːr ðeɪ", "tr": "Eles(as) são / estão?", "ex": "Are they ready for the event?"},
            {"t": "agronomist", "p": "əˈɡrɑːnəmɪst", "tr": "agrônomo(a)", "ex": "She is an agronomist."},
            {"t": "veterinarian", "p": "ˌvetərɪˈneriən", "tr": "veterinário(a)", "ex": "He is a veterinarian."},
            {"t": "sales team", "p": "seɪlz tiːm", "tr": "equipe de vendas", "ex": "They are on the sales team."},
            {"t": "finance team", "p": "ˈfaɪnæns tiːm", "tr": "equipe financeira", "ex": "She is in the finance team."},
            {"t": "logistics team", "p": "loʊˈdʒɪstɪks tiːm", "tr": "equipe de logística", "ex": "He is on the logistics team."},
            {"t": "operations team", "p": "ˌɑːpəˈreɪʃnz tiːm", "tr": "equipe de operações", "ex": "They work in the operations team."},
            {"t": "HR team", "p": "eɪtʃ ɑːr tiːm", "tr": "equipe de RH (Recursos Humanos)", "ex": "Please contact the HR team."},
            {"t": "agribusiness sector", "p": "ˈæɡrɪˌbɪznəs ˈsektər", "tr": "setor de agronegócio", "ex": "We work in the agribusiness sector."},
            {"t": "legal team", "p": "ˈliːɡl tiːm", "tr": "equipe jurídica", "ex": "The contract is with the legal team."},
            {"t": "IT team", "p": "aɪ tiː tiːm", "tr": "equipe de TI", "ex": "Call the IT team for help."},
            {"t": "at a conference", "p": "æt ə ˈkɑːnfərəns", "tr": "em uma conferência", "ex": "The manager is at a conference."},
            {"t": "on a business trip", "p": "ɑːn ə ˈbɪznəs trɪp", "tr": "em viagem de negócios", "ex": "She is on a business trip."},
            {"t": "at an event", "p": "æt ən ɪˈvent", "tr": "em um evento", "ex": "They are at an event today."},
            {"t": "happy", "p": "ˈhæpi", "tr": "feliz", "ex": "We are happy with the results."},
            {"t": "excited", "p": "ɪkˈsaɪtɪd", "tr": "animado(a)", "ex": "He is excited about the project."},
            {"t": "tired", "p": "ˈtaɪərd", "tr": "cansado(a)", "ex": "She is tired after the trip."},
            {"t": "ready", "p": "ˈredi", "tr": "pronto(a)", "ex": "They are ready to start."}
        ]
    },
    "DAY 3": {
        "Vocabulary": [
            {"t": "ten", "p": "ten", "tr": "10", "ex": "We have ten clients."},
            {"t": "eleven", "p": "ɪˈlevn", "tr": "11", "ex": "The meeting is at eleven."},
            {"t": "twelve", "p": "twelv", "tr": "12", "ex": "There are twelve boxes."},
            {"t": "thirteen", "p": "θɜːrˈtiːn", "tr": "13", "ex": "We need thirteen chairs."},
            {"t": "fourteen", "p": "fɔːrˈtiːn", "tr": "14", "ex": "He is in room fourteen."},
            {"t": "fifteen", "p": "fɪfˈtiːn", "tr": "15", "ex": "Wait fifteen minutes."},
            {"t": "sixteen", "p": "sɪkˈstiːn", "tr": "16", "ex": "The date is the sixteenth."},
            {"t": "seventeen", "p": "ˌsevnˈtiːn", "tr": "17", "ex": "Extension seventeen."},
            {"t": "eighteen", "p": "eɪˈtiːn", "tr": "18", "ex": "Eighteen people are in the team."},
            {"t": "nineteen", "p": "naɪnˈtiːn", "tr": "19", "ex": "Order number nineteen."},
            {"t": "twenty", "p": "ˈtwenti", "tr": "20", "ex": "We received twenty emails."},
            {"t": "twenty-one", "p": "ˈtwenti wʌn", "tr": "21", "ex": "Twenty-one days left."},
            {"t": "twenty-two", "p": "ˈtwenti tuː", "tr": "22", "ex": "Room twenty-two."},
            {"t": "twenty-five", "p": "ˈtwenti faɪv", "tr": "25", "ex": "Twenty-five attendees."},
            {"t": "thirty", "p": "ˈθɜːrti", "tr": "30", "ex": "He is thirty years old."},
            {"t": "week", "p": "wiːk", "tr": "semana", "ex": "This week is very busy."},
            {"t": "today", "p": "təˈdeɪ", "tr": "hoje", "ex": "The event is today."},
            {"t": "Monday", "p": "ˈmʌndeɪ", "tr": "segunda-feira", "ex": "The meeting is on Monday."},
            {"t": "Tuesday", "p": "ˈtuːzdeɪ", "tr": "terça-feira", "ex": "He is available on Tuesday."},
            {"t": "Wednesday", "p": "ˈwenzdeɪ", "tr": "quarta-feira", "ex": "She travels on Wednesday."},
            {"t": "Thursday", "p": "ˈθɜːrzdeɪ", "tr": "quinta-feira", "ex": "The briefing is on Thursday."},
            {"t": "Friday", "p": "ˈfraɪdeɪ", "tr": "sexta-feira", "ex": "Deadline is on Friday."},
            {"t": "Saturday", "p": "ˈsætərdeɪ", "tr": "sábado", "ex": "They don't work on Saturday."},
            {"t": "Sunday", "p": "ˈsʌndeɪ", "tr": "domingo", "ex": "Sunday is a day off."}
        ]
    },
    "DAY 4": {
        "Vocabulary": [
            {"t": "He works in [department]", "p": "", "tr": "Ele trabalha em [departamento]", "ex": "He works in logistics."},
            {"t": "She works in [department]", "p": "", "tr": "Ela trabalha em [departamento]", "ex": "She works in HR."},
            {"t": "My extension is...", "p": "", "tr": "Meu ramal é...", "ex": "My extension is 205."},
            {"t": "The meeting is on [day]", "p": "", "tr": "A reunião é na [dia]", "ex": "The meeting is on Tuesday."},
            {"t": "He is available on [day]", "p": "", "tr": "Ele está disponível na [dia]", "ex": "He is available on Friday."},
            {"t": "She is in room [number]", "p": "", "tr": "Ela está na sala [número]", "ex": "She is in room twelve."},
            {"t": "The conference is on floor [number]", "p": "", "tr": "A conferência é no andar [número]", "ex": "The conference is on floor ten."},
            {"t": "Is he available on [day]?", "p": "", "tr": "Ele está disponível na [dia]?", "ex": "Is he available on Monday?"},
            {"t": "They are on the [department] team", "p": "", "tr": "Eles estão na equipe de [departamento]", "ex": "They are on the sales team."},
            {"t": "floor", "p": "flɔːr", "tr": "andar", "ex": "The office is on the third floor."},
            {"t": "Who is...?", "p": "huː ɪz", "tr": "Quem é...?", "ex": "Who is the new manager?"},
            {"t": "Where is...?", "p": "wer ɪz", "tr": "Onde está...?", "ex": "Where is the meeting room?"},
            {"t": "Who are they?", "p": "huː ɑːr ðeɪ", "tr": "Quem são eles/elas?", "ex": "Who are they? They are the consultants."},
            {"t": "Where are they...?", "p": "wer ɑːr ðeɪ", "tr": "Onde eles/elas estão...?", "ex": "Where are they right now?"},
            {"t": "Where are [person 1] and [person 2]?", "p": "", "tr": "Onde estão [pessoa 1] e [pessoa 2]?", "ex": "Where are John and Mary?"}
        ]
    },
    "DAY 5": {
        "Vocabulary": [
            {"t": "Who is your manager?", "p": "", "tr": "Quem é seu gerente?", "ex": "Who is your manager? Is it Ana?"},
            {"t": "Where is your manager right now?", "p": "", "tr": "Onde está seu gerente agora?", "ex": "Where is your manager right now? He is at the farm."},
            {"t": "Is your manager available?", "p": "", "tr": "Seu gerente está disponível?", "ex": "Is your manager available for a call?"},
            {"t": "Who is on your team?", "p": "", "tr": "Quem está na sua equipe?", "ex": "Who is on your team this quarter?"},
            {"t": "What department are they in?", "p": "", "tr": "Em qual departamento eles estão?", "ex": "What department are they in? IT or Legal?"},
            {"t": "Are they busy today?", "p": "", "tr": "Eles estão ocupados hoje?", "ex": "Are they busy today with the export process?"},
            {"t": "Is your manager on vacation this week?", "p": "", "tr": "Seu gerente está de férias esta semana?", "ex": "Is your manager on vacation this week? I need his signature."},
            {"t": "Who is at the conference?", "p": "", "tr": "Quem está na conferência?", "ex": "Who is at the conference representing the company?"},
            {"t": "What is your extension?", "p": "", "tr": "Qual é o seu ramal?", "ex": "What is your extension? I'll call you back."},
            {"t": "Is he busy today?", "p": "", "tr": "Ele está ocupado hoje?", "ex": "Is he busy today? I need to talk to him."},
            {"t": "Is she available now?", "p": "", "tr": "Ela está disponível agora?", "ex": "Is she available now for a quick meeting?"},
            {"t": "Are they at the conference?", "p": "", "tr": "Eles estão na conferência?", "ex": "Are they at the conference or in the office?"},
            {"t": "They aren't on vacation.", "p": "", "tr": "Eles não estão de férias.", "ex": "They aren't on vacation, they are on a business trip."},
            {"t": "She isn't a manager.", "p": "", "tr": "Ela não é gerente.", "ex": "She isn't a manager, she is an analyst."},
            {"t": "They aren't at work, they are at home today.", "p": "", "tr": "Eles não estão no trabalho, estão em casa hoje.", "ex": "They aren't at work, they are at home today."}
        ]
    }
},
    
"Método T.A.L.K - Week 4": {
    "DAY 1": {
        "Vocabulary": [
            {"t": "eat", "p": "iːt", "tr": "comer", "ex": "I eat lunch at the canteen."},
            {"t": "beans", "p": "biːnz", "tr": "feijão", "ex": "I eat rice and beans."},
            {"t": "rice", "p": "raɪs", "tr": "arroz", "ex": "We eat rice every day."},
            {"t": "meat", "p": "miːt", "tr": "carne", "ex": "He eats meat for dinner."},
            {"t": "eggs", "p": "eɡz", "tr": "ovos", "ex": "I eat eggs for breakfast."},
            {"t": "yogurt", "p": "ˈjoʊɡərt", "tr": "iogurte", "ex": "She eats yogurt in the morning."},
            {"t": "fruit", "p": "fruːt", "tr": "fruta / frutas", "ex": "I eat fruit before work."},
            {"t": "vegetables", "p": "ˈvedʒtəblz", "tr": "vegetais / legumes", "ex": "We eat vegetables for lunch."},
            {"t": "granola bar", "p": "ɡrəˈnoʊlə bɑːr", "tr": "barra de cereal/granola", "ex": "I eat a granola bar during my coffee break."},
            {"t": "grilled chicken", "p": "ɡrɪld ˈtʃɪkɪn", "tr": "frango grelhado", "ex": "I prefer grilled chicken."},
            {"t": "drink", "p": "drɪŋk", "tr": "beber", "ex": "I drink water."},
            {"t": "coffee", "p": "ˈkɔːfi", "tr": "café", "ex": "I drink coffee at work."},
            {"t": "water", "p": "ˈwɔːtər", "tr": "água", "ex": "I drink water every day."},
            {"t": "work", "p": "wɜːrk", "tr": "trabalhar", "ex": "I work long hours."},
            {"t": "study", "p": "ˈstʌdi", "tr": "estudar", "ex": "I study English."},
            {"t": "at the office", "p": "æt ðə ˈɑːfɪs", "tr": "no escritório", "ex": "I work at the office."},
            {"t": "overtime", "p": "ˈoʊvərtaɪm", "tr": "hora extra", "ex": "I work overtime on Fridays."},
            {"t": "long hours", "p": "lɔːŋ ˈaʊərz", "tr": "muitas horas / longas jornadas", "ex": "Managers work long hours."},
            {"t": "at a farm", "p": "æt ə fɑːrm", "tr": "em uma fazenda", "ex": "He works at a farm."}
        ]
    },
    "DAY 2": {
        "Vocabulary": [
            {"t": "I don't eat", "p": "aɪ doʊnt iːt", "tr": "Eu não como", "ex": "I don't eat meat."},
            {"t": "I don't drink", "p": "aɪ doʊnt drɪŋk", "tr": "Eu não bebo", "ex": "I don't drink soda."},
            {"t": "Do you eat?", "p": "du ju iːt", "tr": "Você come?", "ex": "Do you eat vegetables?"},
            {"t": "Do you drink?", "p": "du ju drɪŋk", "tr": "Você bebe?", "ex": "Do you drink coffee?"},
            {"t": "have breakfast", "p": "hæv ˈbrekfəst", "tr": "tomar café da manhã", "ex": "I have breakfast at home."},
            {"t": "have lunch", "p": "hæv lʌntʃ", "tr": "almoçar", "ex": "I have lunch at noon."},
            {"t": "have dinner", "p": "hæv ˈdɪnər", "tr": "jantar", "ex": "I have dinner with my family."},
            {"t": "study", "p": "ˈstʌdi", "tr": "estudar", "ex": "I study at night."},
            {"t": "at noon", "p": "æt nuːn", "tr": "ao meio-dia", "ex": "We have a meeting at noon."},
            {"t": "at lunchtime", "p": "æt ˈlʌntʃtaɪm", "tr": "na hora do almoço", "ex": "I rest at lunchtime."},
            {"t": "at home", "p": "æt hoʊm", "tr": "em casa", "ex": "I eat dinner at home."},
            {"t": "at 3pm", "p": "æt θriː piː em", "tr": "às 15h", "ex": "The event is at 3pm."},
            {"t": "after work", "p": "ˈæftər wɜːrk", "tr": "depois do trabalho", "ex": "I study English after work."},
            {"t": "before work", "p": "bɪˈfɔːr wɜːrk", "tr": "antes do trabalho", "ex": "I drink coffee before work."},
            {"t": "every day", "p": "ˈevri deɪ", "tr": "todos os dias", "ex": "I work every day."},
            {"t": "on weekends", "p": "ɑːn ˈwiːkendz", "tr": "nos finais de semana", "ex": "I don't work on weekends."},
            {"t": "coffee break", "p": "ˈkɔːfi breɪk", "tr": "pausa para o café", "ex": "We have a coffee break at 10 AM."},
            {"t": "a snack", "p": "ə snæk", "tr": "um lanche", "ex": "I eat a snack in the afternoon."},
            {"t": "canteen", "p": "kænˈtiːn", "tr": "refeitório / cantina", "ex": "I have lunch at the canteen."},
            {"t": "in the morning", "p": "ɪn ðə ˈmɔːrnɪŋ", "tr": "de manhã", "ex": "I study in the morning."},
            {"t": "in the afternoon", "p": "ɪn ði ˌæftərˈnuːn", "tr": "de tarde", "ex": "The meeting is in the afternoon."},
            {"t": "at night", "p": "æt naɪt", "tr": "de noite", "ex": "I sleep at night."},
            {"t": "weekdays", "p": "ˈwiːkdeɪz", "tr": "dias de semana", "ex": "I work on weekdays."}
        ]
    },
    "DAY 3": {
        "Vocabulary": [
            {"t": "I study", "p": "aɪ ˈstʌdi", "tr": "Eu estudo", "ex": "I study every day."},
            {"t": "I don't study", "p": "aɪ doʊnt ˈstʌdi", "tr": "Eu não estudo", "ex": "I don't study at night."},
            {"t": "Do you study?", "p": "du ju ˈstʌdi", "tr": "Você estuda?", "ex": "Do you study English?"},
            {"t": "English", "p": "ˈɪŋɡlɪʃ", "tr": "Inglês", "ex": "I speak English."},
            {"t": "Spanish", "p": "ˈspænɪʃ", "tr": "Espanhol", "ex": "Do you study Spanish?"},
            {"t": "Portuguese", "p": "ˌpɔːrtʃʊˈɡiːz", "tr": "Português", "ex": "I speak Portuguese."},
            {"t": "at school", "p": "æt skuːl", "tr": "na escola", "ex": "I study at school."},
            {"t": "with my co-workers", "p": "wɪð maɪ ˈkoʊ wɜːrkərz", "tr": "com meus colegas de trabalho", "ex": "I have lunch with my co-workers."},
            {"t": "with my friends", "p": "wɪð maɪ frendz", "tr": "com meus amigos", "ex": "I study with my friends."},
            {"t": "with my family", "p": "wɪð maɪ ˈfæməli", "tr": "com minha família", "ex": "I have dinner with my family."},
            {"t": "alone", "p": "əˈloʊn", "tr": "sozinho(a)", "ex": "I prefer to work alone."},
            {"t": "milk", "p": "mɪlk", "tr": "leite", "ex": "I drink milk."},
            {"t": "tea", "p": "tiː", "tr": "chá", "ex": "She drinks tea in the afternoon."},
            {"t": "beer", "p": "bɪr", "tr": "cerveja", "ex": "We drink beer on weekends."},
            {"t": "juice", "p": "dʒuːs", "tr": "suco", "ex": "I drink orange juice."},
            {"t": "soda", "p": "ˈsoʊdə", "tr": "refrigerante", "ex": "I don't drink soda."},
            {"t": "chocolate", "p": "ˈtʃɑːklət", "tr": "chocolate", "ex": "I eat chocolate."},
            {"t": "chicken", "p": "ˈtʃɪkɪn", "tr": "frango", "ex": "I eat chicken for lunch."},
            {"t": "pasta", "p": "ˈpɑːstə", "tr": "massa / macarrão", "ex": "Do you eat pasta?"},
            {"t": "at the restaurant", "p": "æt ðə ˈrestrɑːnt", "tr": "no restaurante", "ex": "We have dinner at the restaurant."},
            {"t": "toast", "p": "toʊst", "tr": "torrada", "ex": "I eat toast for breakfast."},
            {"t": "jam", "p": "dʒæm", "tr": "geleia", "ex": "I like toast and jam."},
            {"t": "for breakfast", "p": "fɔːr ˈbrekfəst", "tr": "no café da manhã", "ex": "I eat eggs for breakfast."},
            {"t": "for lunch", "p": "fɔːr lʌntʃ", "tr": "no almoço", "ex": "I eat rice and beans for lunch."},
            {"t": "for dinner", "p": "fɔːr ˈdɪnər", "tr": "no jantar", "ex": "I eat meat for dinner."}
        ]
    },
    "DAY 4": {
        "Vocabulary": [
            {"t": "ranch", "p": "ræntʃ", "tr": "fazenda / rancho", "ex": "I work at a large ranch."},
            {"t": "co-workers", "p": "ˈkoʊ wɜːrkərz", "tr": "colegas de trabalho", "ex": "My co-workers are busy."},
            {"t": "after", "p": "ˈæftər", "tr": "depois", "ex": "I rest after the meeting."},
            {"t": "before", "p": "bɪˈfɔːr", "tr": "antes", "ex": "I need the report before noon."},
            {"t": "after work", "p": "ˈæftər wɜːrk", "tr": "depois do trabalho", "ex": "I go home after work."},
            {"t": "before work", "p": "bɪˈfɔːr wɜːrk", "tr": "antes do trabalho", "ex": "I study English before work."},
            {"t": "routine", "p": "ruːˈtiːn", "tr": "rotina", "ex": "My routine is busy."},
            {"t": "busy", "p": "ˈbɪzi", "tr": "ocupado / agitado", "ex": "I have a busy routine."},
            {"t": "snack bar", "p": "snæk bɑːr", "tr": "lanchonete", "ex": "We eat at the snack bar."},
            {"t": "work long hours", "p": "wɜːrk lɔːŋ ˈaʊərz", "tr": "trabalhar longas horas", "ex": "Managers work long hours."},
            {"t": "In the morning I eat toast and jam for breakfast at home.", "p": "", "tr": "De manhã, eu como torrada e geleia no café da manhã em casa.", "ex": "In the morning I eat toast and jam for breakfast at home."},
            {"t": "I work at an agribusiness office.", "p": "", "tr": "Eu trabalho em um escritório de agronegócio.", "ex": "I work at an agribusiness office."},
            {"t": "I have lunch at the canteen with the team.", "p": "", "tr": "Eu almoço no refeitório com a equipe.", "ex": "I have lunch at the canteen with the team."},
            {"t": "My routine is busy, but I love it!", "p": "", "tr": "Minha rotina é agitada, mas eu adoro!", "ex": "My routine is busy, but I love it!"},
            {"t": "After work, I eat dinner at home.", "p": "", "tr": "Depois do trabalho, eu janto em casa.", "ex": "After work, I eat dinner at home."},
            {"t": "I work at a large ranch.", "p": "", "tr": "Eu trabalho em uma grande fazenda.", "ex": "I work at a large ranch."},
            {"t": "I eat fruit or a granola bar.", "p": "", "tr": "Eu como fruta ou uma barra de cereal.", "ex": "I eat fruit or a granola bar."}
        ]
    },
    "DAY 5": {
        "Vocabulary": [
            {"t": "Do you drink coffee at work?", "p": "", "tr": "Você bebe café no trabalho?", "ex": "Do you drink coffee at work?"},
            {"t": "I drink coffee at work.", "p": "", "tr": "Eu bebo café no trabalho.", "ex": "I drink coffee at work."},
            {"t": "I don't drink coffee at work.", "p": "", "tr": "Eu não bebo café no trabalho.", "ex": "I don't drink coffee at work."},
            {"t": "What do you eat for lunch?", "p": "", "tr": "O que você come no almoço?", "ex": "What do you eat for lunch?"},
            {"t": "I eat rice for lunch.", "p": "", "tr": "Eu como arroz no almoço.", "ex": "I eat rice for lunch."},
            {"t": "You eat beans for dinner.", "p": "", "tr": "Você come feijão no jantar.", "ex": "You eat beans for dinner."},
            {"t": "When do you study English?", "p": "", "tr": "Quando você estuda inglês?", "ex": "When do you study English?"},
            {"t": "I study English at noon.", "p": "", "tr": "Eu estudo inglês ao meio-dia.", "ex": "I study English at noon."},
            {"t": "You study English before work.", "p": "", "tr": "Você estuda inglês antes do trabalho.", "ex": "You study English before work."},
            {"t": "What do you drink in the morning?", "p": "", "tr": "O que você bebe de manhã?", "ex": "What do you drink in the morning?"},
            {"t": "I drink milk in the morning for breakfast.", "p": "", "tr": "Eu bebo leite de manhã no café da manhã.", "ex": "I drink milk in the morning for breakfast."},
            {"t": "You don't drink milk and water in the morning.", "p": "", "tr": "Você não bebe leite e água de manhã.", "ex": "You don't drink milk and water in the morning."},
            {"t": "Do you work overtime?", "p": "", "tr": "Você faz hora extra?", "ex": "Do you work overtime?"},
            {"t": "I work overtime.", "p": "", "tr": "Eu faço hora extra.", "ex": "I work overtime."},
            {"t": "I don't work overtime.", "p": "", "tr": "Eu não faço hora extra.", "ex": "I don't work overtime."},
            {"t": "I work long hours.", "p": "", "tr": "Eu trabalho longas horas.", "ex": "I work long hours."},
            {"t": "You don't work long hours.", "p": "", "tr": "Você não trabalha longas horas.", "ex": "You don't work long hours."},
            {"t": "I study English at night.", "p": "", "tr": "Eu estudo inglês de noite.", "ex": "I study English at night."},
            {"t": "Where do you study English?", "p": "", "tr": "Onde você estuda inglês?", "ex": "Where do you study English?"},
            {"t": "I study English at Talk It Easy.", "p": "", "tr": "Eu estudo inglês na Talk It Easy.", "ex": "I study English at Talk It Easy."}
        ]
    }
},

    "Método T.A.L.K - Week 5": {
    "DAY 1": {
        "Vocabulary": [
            {"t": "warehouse", "p": "ˈwerhaʊs", "tr": "armazém / galpão", "ex": "The grain is stored in the warehouse."},
            {"t": "laboratory", "p": "ˈlæbrətɔːri", "tr": "laboratório", "ex": "The soil samples are at the laboratory."},
            {"t": "parking lot", "p": "ˈpɑːrkɪŋ lɑːt", "tr": "estacionamento", "ex": "The truck is in the parking lot."},
            {"t": "lobby", "p": "ˈlɑːbi", "tr": "saguão / recepção", "ex": "Wait for the client in the lobby."},
            {"t": "airport", "p": "ˈerpɔːrt", "tr": "aeroporto", "ex": "The director is arriving at the airport."},
            {"t": "late", "p": "leɪt", "tr": "atrasado/a", "ex": "The fertilizer shipment is late this week."},
            {"t": "early", "p": "ˈɜːrli", "tr": "adiantado / cedo", "ex": "He arrived early for the morning briefing."},
            {"t": "on time", "p": "ɑːn taɪm", "tr": "no horário / pontual", "ex": "Everything was delivered on time."},
            {"t": "available", "p": "əˈveɪləbl", "tr": "disponível", "ex": "Is the agronomist available for a call?"},
            {"t": "unavailable", "p": "ˌʌnəˈveɪləbl", "tr": "indisponível", "ex": "The manager is unavailable right now."},
            {"t": "online", "p": "ˈɑːnlaɪn", "tr": "online / conectado", "ex": "The tracking system is back online."},
            {"t": "offline", "p": "ˈɔːflaɪn", "tr": "offline / desconectado", "ex": "The server is offline for maintenance."},
            {"t": "meeting room", "p": "ˈmiːtɪŋ ruːm", "tr": "sala de reuniões", "ex": "They are waiting in the meeting room."}
        ]
    },
    "DAY 2": {
        "Vocabulary": [
            {"t": "report", "p": "rɪˈpɔːrt", "tr": "relatório", "ex": "I need to review the quarterly report."},
            {"t": "document", "p": "ˈdɑːkjʊmənt", "tr": "documento", "ex": "Please sign this export document."},
            {"t": "file", "p": "faɪl", "tr": "arquivo", "ex": "Send me the logistics file via email."},
            {"t": "laptop", "p": "ˈlæptɑːp", "tr": "notebook / laptop", "ex": "Open your laptop for the presentation."},
            {"t": "tablet", "p": "ˈtæblət", "tr": "tablet", "ex": "The field representative uses a tablet."},
            {"t": "notebook", "p": "ˈnoʊtbʊk", "tr": "caderno / bloco de notas", "ex": "Write the client details in your notebook."},
            {"t": "pen", "p": "pen", "tr": "caneta", "ex": "Do you have a pen to sign the contract?"},
            {"t": "steak", "p": "steɪk", "tr": "bife / carne", "ex": "He ordered a steak at the restaurant."},
            {"t": "fish", "p": "fɪʃ", "tr": "peixe", "ex": "I prefer fish for lunch."},
            {"t": "sandwich", "p": "ˈsændwɪtʃ", "tr": "sanduíche", "ex": "I will eat a quick sandwich during the break."},
            {"t": "soup", "p": "suːp", "tr": "sopa", "ex": "The soup at the hotel is very good."},
            {"t": "dessert", "p": "dɪˈzɜːrt", "tr": "sobremesa", "ex": "Fruit is a healthy dessert."},
            {"t": "juice", "p": "dʒuːs", "tr": "suco", "ex": "I drink orange juice for breakfast."}
        ]
    },
    "DAY 3": {
        "Vocabulary": [
            {"t": "supplier", "p": "səˈplaɪər", "tr": "fornecedor", "ex": "Contact the main seed supplier."},
            {"t": "client", "p": "ˈklaɪənt", "tr": "cliente", "ex": "The client wants a project update."},
            {"t": "shipment", "p": "ˈʃɪpmənt", "tr": "carregamento / remessa", "ex": "Track the shipment right now."},
            {"t": "delivery", "p": "dɪˈlɪvəri", "tr": "entrega", "ex": "The delivery is scheduled for Monday."},
            {"t": "inventory", "p": "ˈɪnvəntɔːri", "tr": "inventário / estoque", "ex": "Check the warehouse inventory."},
            {"t": "stock", "p": "stɑːk", "tr": "estoque", "ex": "We have new equipment in stock."},
            {"t": "production", "p": "prəˈdʌkʃn", "tr": "produção", "ex": "The production team works long hours."},
            {"t": "quality", "p": "ˈkwɑːləti", "tr": "qualidade", "ex": "We focus on quality control."},
            {"t": "schedule", "p": "ˈskedʒuːl", "tr": "cronograma / agenda", "ex": "Review the schedule before the meeting."},
            {"t": "delay", "p": "dɪˈleɪ", "tr": "atraso", "ex": "There is a delay in the operations department."},
            {"t": "order", "p": "ˈɔːrdər", "tr": "pedido", "ex": "Place the order for the new machinery."},
            {"t": "supervisor", "p": "ˈsuːpərvaɪzər", "tr": "supervisor/a", "ex": "The supervisor is at the ranch."},
            {"t": "assistant", "p": "əˈsɪstənt", "tr": "assistente", "ex": "Speak with my assistant for information."}
        ]
    },
    "DAY 4": {
        "Vocabulary": [
            {"t": "I am at the warehouse and I work long hours today.", "p": "", "tr": "Eu estou no armazém e trabalho muitas horas hoje.", "ex": "Context: Explaining routine to a colleague."},
            {"t": "You are a supplier and you drink coffee with the manager.", "p": "", "tr": "Você é um fornecedor e bebe café com o gerente.", "ex": "Context: Observing a business meeting."},
            {"t": "I am ready for the meeting, but I don't have the report.", "p": "", "tr": "Estou pronto para a reunião, mas não tenho o relatório.", "ex": "Context: Reporting an issue before starting."},
            {"t": "This is the new laptop. It is for the production team.", "p": "", "tr": "Este é o novo notebook. É para a equipe de produção.", "ex": "Context: Distributing company equipment."},
            {"t": "I am early for the delivery, so I have a coffee break now.", "p": "", "tr": "Estou adiantado para a entrega, então farei uma pausa para o café agora.", "ex": "Context: Managing downtime productively."}
        ]
    },
    "DAY 5": {
        "Vocabulary": [
            {"t": "Are you a supervisor? Do you work at the headquarters?", "p": "", "tr": "Você é um supervisor? Você trabalha na matriz?", "ex": "Conversation practice: Verifying positions."},
            {"t": "Where is the client? Do you have the document for the client?", "p": "", "tr": "Onde está o cliente? Você tem o documento para o cliente?", "ex": "Conversation practice: Handling paperwork."},
            {"t": "When is the meeting? Do you have the schedule?", "p": "", "tr": "Quando é a reunião? Você tem o cronograma?", "ex": "Conversation practice: Time management."},
            {"t": "Who are they? Do they work in the laboratory?", "p": "", "tr": "Quem são eles? Eles trabalham no laboratório?", "ex": "Conversation practice: Identifying the team."},
            {"t": "What do you eat at the airport? Are you hungry?", "p": "", "tr": "O que você come no aeroporto? Você está com fome?", "ex": "Conversation practice: Small talk before business travel."}
        ]
    }
},
    
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
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div class="sidebar-logo-icon">🚜</div>
        <div>
            <div class="sidebar-logo-text">Talk Agribusiness</div>
            <div class="sidebar-logo-sub">Flashcard System</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    aula_sel = st.selectbox("Módulo", list(data.keys()), label_visibility="visible")
    dia_sel = st.selectbox("Dia", list(data[aula_sel].keys()), label_visibility="visible")

    lista_cards = data[aula_sel][dia_sel]["Vocabulary"]
    total = len(lista_cards)

    st.markdown("---")
    st.markdown(f"""
    <div style="font-size:12px; color:#475569; line-height:1.8;">
        <div style="margin-bottom:4px;">📚 <b style="color:#e2e8f0">{total}</b> cards neste dia</div>
    </div>
    """, unsafe_allow_html=True)

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
total = len(lista_cards)
pct = (idx + 1) / total

# -------------------------
# HEADER
# -------------------------
st.markdown(f"""
<div class="page-header">
    <div class="day-badge">📅 {dia_sel}</div>
    <p class="page-title">Flashcards de Vocabulário</p>
    <p class="page-subtitle">{aula_sel}</p>
</div>
""", unsafe_allow_html=True)

# Progress bar
st.markdown(f"""
<div class="progress-wrap">
    <div class="progress-track">
        <div class="progress-fill" style="width:{pct*100:.1f}%"></div>
    </div>
    <span class="progress-label">{idx+1} / {total}</span>
</div>
""", unsafe_allow_html=True)

# -------------------------
# FLASHCARD
# -------------------------
termo = card['t']
is_long = len(termo) > 30
term_class = "card-term-long" if is_long else "card-term"

if not st.session_state[flip_key]:
    phonetic_html = f'<p class="card-phonetic">/{card.get("p", "")}/</p>' if card.get("p") else ""
    st.markdown(f"""
    <div class="flashcard">
        <p class="{term_class}">{termo}</p>
        {phonetic_html}
        <p class="card-flip-hint">↓ clique para revelar</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔄  Revelar tradução & exemplo", use_container_width=True):
        st.session_state[flip_key] = True
        st.rerun()

else:
    tr = card['tr']
    ex = card['ex']
    tr_class = "card-translation-long" if len(tr) > 35 else "card-translation"

    st.markdown(f"""
    <div class="flashcard flashcard-back">
        <p class="{tr_class}">{tr}</p>
        <p class="card-example-label">Exemplo</p>
        <p class="card-example">"{ex}"</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("⬅️  Voltar ao termo", use_container_width=True):
        st.session_state[flip_key] = False
        st.rerun()

# -------------------------
# ÁUDIO
# -------------------------
col_audio, _ = st.columns([1, 2])
with col_audio:
    if st.button("🔊  Ouvir pronúncia", use_container_width=True):
        texto_limpo = card["t"].split("→")[-1].strip()
        audio_bytes = gerar_audio(texto_limpo)
        tocar_audio(audio_bytes)

# -------------------------
# NAVEGAÇÃO
# -------------------------
st.markdown("<hr>", unsafe_allow_html=True)

col1, col_mid, col3 = st.columns([1, 2, 1])

with col1:
    disabled_prev = idx == 0
    if st.button("← Anterior", use_container_width=True, disabled=disabled_prev):
        st.session_state[idx_key] -= 1
        st.session_state[flip_key] = False
        st.rerun()

with col_mid:
    dots = ""
    for i in range(min(total, 10)):
        mapped = int(i * total / min(total, 10))
        active = mapped == idx
        color = "#1d4ed8" if active else "#e2e8f0"
        dots += f'<span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:{color};margin:0 3px;"></span>'
    if total > 10:
        dots += f'<span style="font-size:11px;color:#94a3b8;margin-left:4px;">+{total-10}</span>'
    st.markdown(f'<div style="text-align:center;padding-top:8px;">{dots}</div>', unsafe_allow_html=True)

with col3:
    disabled_next = idx >= total - 1
    if st.button("Próximo →", use_container_width=True, disabled=disabled_next):
        st.session_state[idx_key] += 1
        st.session_state[flip_key] = False
        st.rerun()
