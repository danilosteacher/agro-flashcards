import streamlit as st
from gtts import gTTS
import io

# Configuração de Identidade Visual
st.set_page_config(page_title="Talk Agribusiness - Flashcards", page_icon="🚜", layout="centered")

# --- BANCO DE DADOS ATUALIZADO (Aula 14 com Frases de Exemplo) ---
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
        },
        "DAY 2: Grammar + Drills": {
            "Vocabulary": [
                {"t": "ready", "p": "ˈredi", "tr": "pronto/a", "ex": "The contract is ready for signing."},
                {"t": "on time", "p": "ɒn taɪm", "tr": "no horário", "ex": "The delivery arrived exactly on time."},
                {"t": "in the office", "p": "ɪn ðə ˈɒfɪs", "tr": "no escritório", "ex": "Is the CEO in the office today?"},
                {"t": "in the meeting", "p": "ɪn ðə ˈmiːtɪŋ", "tr": "na reunião", "ex": "She is in the meeting right now."},
                {"t": "at work", "p": "æt wɜːrk", "tr": "no trabalho", "ex": "He is currently at work in the lab."},
                {"t": "in the morning", "p": "ɪn ðə ˈmɔːrnɪŋ", "tr": "de manhã", "ex": "I check the prices in the morning."},
                {"t": "in the afternoon", "p": "ɪn ðə ˌæftərˈnuːn", "tr": "à tarde", "ex": "We can talk in the afternoon."},
                {"t": "manager", "p": "ˈmænɪdʒər", "tr": "gerente", "ex": "The farm manager is very experienced."},
                {"t": "colleague", "p": "ˈkɒliːɡ", "tr": "colega", "ex": "My colleague will help with the data."},
                {"t": "available by phone", "p": "əˈveɪləbl baɪ foʊn", "tr": "disponível por telefone", "ex": "The buyer is available by phone."},
                {"t": "out of office", "p": "aʊt əv ˈɒfɪs", "tr": "fora do escritório", "ex": "He is out of office until Monday."},
                {"t": "on a business trip", "p": "ɒn ə ˈbɪznəs trɪp", "tr": "em viagem de negócios", "ex": "Our director is on a business trip."}
            ]
        },
        "DAY 3: Drills + Time Expressions": {
            "Vocabulary": [
                {"t": "yesterday", "p": "ˈjestərdeɪ", "tr": "ontem", "ex": "We finished the soil analysis yesterday."},
                {"t": "last week", "p": "lɑːst wiːk", "tr": "semana passada", "ex": "The prices went up last week."},
                {"t": "last Friday", "p": "lɑːst ˈfraɪdeɪ", "tr": "última sexta-feira", "ex": "We closed the deal last Friday."},
                {"t": "two days ago", "p": "tuː deɪz əˈgoʊ", "tr": "dois dias atrás", "ex": "The technician was here two days ago."},
                {"t": "yesterday morning", "p": "ˈjestərdeɪ ˈmɔːrnɪŋ", "tr": "ontem de manhã", "ex": "I sent the email yesterday morning."},
                {"t": "yesterday afternoon", "p": "ˈjestərdeɪ ˌæftərˈnuːn", "tr": "ontem à tarde", "ex": "The rain started yesterday afternoon."},
                {"t": "at that time", "p": "æt ðæt taɪm", "tr": "naquele momento", "ex": "I wasn't in the city at that time."},
                {"t": "on Monday", "p": "ɒn ˈmʌndeɪ", "tr": "na segunda-feira", "ex": "The shipment leaves on Monday."},
                {"t": "at 3 PM", "p": "æt θriː piː em", "tr": "às 15h", "ex": "The conference starts at 3 PM."},
                {"t": "in 2023", "p": "ɪn ˈtwenti ˈtwenti θriː", "tr": "em 2023", "ex": "The company was founded in 2023."},
                {"t": "a week ago", "p": "ə wiːk əˈɡoʊ", "tr": "uma semana atrás", "ex": "I received the feedback a week ago."},
                {"t": "last month", "p": "lɑːst mʌnθ", "tr": "mês passado", "ex": "We achieved the goal last month."}
            ]
        },
        "DAY 4: Audios 1-4": {
            "Vocabulary": [
                {"t": "conference", "p": "ˈkɒnfərəns", "tr": "conferência", "ex": "I'm attending a conference on AgTech."},
                {"t": "presentation", "p": "ˌpreznˈteɪʃn", "tr": "apresentação", "ex": "Your presentation was very clear."},
                {"t": "sales team", "p": "seɪlz tiːm", "tr": "equipe de vendas", "ex": "The sales team is meeting the client."},
                {"t": "financial reports", "p": "faɪˈnænʃl rɪˈpɔːrts", "tr": "relatórios financeiros", "ex": "The financial reports are ready."},
                {"t": "voicemail", "p": "ˈvɔɪsmeɪl", "tr": "caixa de mensagens", "ex": "He left a message on my voicemail."},
                {"t": "data center", "p": "ˈdeɪtə ˈsentər", "tr": "centro de dados", "ex": "The data center is being upgraded."},
                {"t": "server emergency", "p": "ˈsɜːrvər iˈmɜːrdʒənsi", "tr": "emergência no servidor", "ex": "We had a server emergency at midnight."},
                {"t": "production issue", "p": "prəˈdʌkʃn ˈɪʃuː", "tr": "problema de produção", "ex": "There is a production issue at the plant."},
                {"t": "loan meeting", "p": "loʊn ˈmiːtɪŋ", "tr": "reunião de empréstimo", "ex": "The bank scheduled a loan meeting."},
                {"t": "on the road", "p": "ɒn ðə roʊd", "tr": "em campo / a caminho", "ex": "Our agronomist is on the road today."},
                {"t": "scheduling conflict", "p": "ˈskedʒuːlɪŋ ˈkɒnflɪkt", "tr": "conflito de agenda", "ex": "I have a scheduling conflict at 10 AM."},
                {"t": "company-wide", "p": "ˈkʌmpəni waɪd", "tr": "para toda a empresa", "ex": "This is a company-wide announcement."}
            ]
        },
        "DAY 5: Personal Production": {
            "Vocabulary": [
                {"t": "whereabouts", "p": "ˈwerəbaʊts", "tr": "paradeiro", "ex": "Do you know the driver's whereabouts?"},
                {"t": "accountability", "p": "əˌkaʊntəˈbɪləti", "tr": "responsabilidade", "ex": "Accountability is key in management."},
                {"t": "justify", "p": "ˈdʒʌstɪfaɪ", "tr": "justificar", "ex": "Can you justify the extra cost?"},
                {"t": "absence", "p": "ˈæbsəns", "tr": "ausência", "ex": "Her absence was due to health reasons."},
                {"t": "explanation", "p": "ˌekspləˈneɪʃn", "tr": "explicação", "ex": "I need a technical explanation for this."},
                {"t": "location", "p": "loʊˈkeɪʃn", "tr": "localização", "ex": "The farm is in a prime location."},
                {"t": "headquarters", "p": "ˈhedkwɔːrtərz", "tr": "sede da empresa", "ex": "The headquarters is in São Paulo."},
                {"t": "branch", "p": "bræntʃ", "tr": "filial", "ex": "We are opening a new branch in Mato Grosso."},
                {"t": "department", "p": "dɪˈpɑːrtmənt", "tr": "departamento", "ex": "Talk to the HR department."},
                {"t": "floor", "p": "flɔːr", "tr": "andar", "ex": "The meeting is on the third floor."},
                {"t": "boardroom", "p": "ˈbɔːrdruːm", "tr": "sala executiva", "ex": "The board is waiting in the boardroom."},
                {"t": "factory", "p": "ˈfæktri", "tr": "fábrica", "ex": "The fertilizer factory is operating well."}
            ]
        }
    }
}

# --- LÓGICA DO MOTOR ---
st.sidebar.title("🚜 Talk Agribusiness")
aula_sel = st.sidebar.selectbox("Escolha a Aula:", list(data.keys()))
dia_sel = st.sidebar.selectbox("Escolha o Dia:", list(data[aula_sel].keys()))

lista_cards = data[aula_sel][dia_sel]["Vocabulary"]

idx_key = f"{aula_sel}_{dia_sel}_idx"
flipped_key = f"{aula_sel}_{dia_sel}_flipped"

if idx_key not in st.session_state:
    st.session_state[idx_key] = 0
if flipped_key not in st.session_state:
    st.session_state[flipped_key] = False

idx = st.session_state[idx_key]
card = lista_cards[idx]

# --- INTERFACE ---
st.title("Flashcards: Pronúncia & Contexto")
st.caption(f"Foco: {dia_sel}")

with st.container(border=True):
    if not st.session_state[flipped_key]:
        st.markdown(f"<h1 style='text-align: center; font-size: 65px; height: 160px; display: flex; align-items: center; justify-content: center;'>{card['t']}</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; color: gray; font-size: 20px;'>/{card['p']}/</p>", unsafe_allow_html=True)
        
        if st.button("🔄 REVELAR TRADUÇÃO & EXEMPLO", type="primary", use_container_width=True):
            st.session_state[flipped_key] = True
            st.rerun()
    else:
        st.markdown(f"<h2 style='text-align: center; color: #2E7D32;'>{card['tr']}</h2>", unsafe_allow_html=True)
        st.divider()
        st.markdown(f"**Exemplo de uso:**")
        st.write(f"*{card['ex']}*")
        st.write("")
        if st.button("⬅️ VOLTAR PARA O TERMO", use_container_width=True):
            st.session_state[flipped_key] = False
            st.rerun()

    if st.button("🔊 OUVIR PRONÚNCIA", use_container_width=True):
        tts = gTTS(text=card['t'], lang='en')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        st.audio(fp, format='audio/mp3')

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

st.divider()
st.progress((idx + 1) / len(lista_cards))
st.write(f"Card {idx + 1} de {len(lista_cards)}")
