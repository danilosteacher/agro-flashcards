import streamlit as st
from gtts import gTTS
import io

# Configuração de Página Premium
st.set_page_config(page_title="Talk Agribusiness | Flashcards", page_icon="🚜", layout="centered")

# --- ESTILIZAÇÃO CSS (UX/UI Otimizado) ---
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

# --- BANCO DE DADOS COMPLETO (Aulas 14 e 15) ---
data = {
    "Aula 14: Corporate & Logistics": {
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
        ],
        "DAY 3: Drills + Time Expressions": [
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
        ],
        "DAY 4: Audios 1-4": [
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
        ],
        "DAY 5: Personal Production": [
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
    },
    "Aula 15: Past & Projects": {
        "DAY 1: Monday Meeting": [
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
        ],
        "DAY 2: Grammar & Logistics": [
            {"t": "check → checked", "p": "tʃekt", "tr": "verificar / verificou", "ex": "I checked the inventory levels."},
            {"t": "present → presented", "p": "prɪˈzentɪd", "tr": "apresentar / apresentou", "ex": "He presented the data at the seminar."},
            {"t": "visit → visited", "p": "ˈvɪzɪtɪd", "tr": "visitar / visitou", "ex": "The agronomist visited the farm."},
            {"t": "explain → explained", "p": "ɪkˈspleɪnd", "tr": "explicar / explicou", "ex": "The technician explained how the sensor works."},
            {"t": "discuss → discussed", "p": "dɪˈskʌst", "tr": "discutir / discutiu", "ex": "We discussed the strategy for next year."},
            {"t": "complete → completed", "p": "kəmˈpliːtɪd", "tr": "completar / completou", "ex": "They completed the training yesterday."},
            {"t": "confirm → confirmed", "p": "kənˈfɜːrmd", "tr": "confirmar / confirmou", "ex": "She confirmed the flight to the summit."},
            {"t": "schedule → scheduled", "p": "ˈskedʒuːld", "tr": "agendar / agendou", "ex": "I scheduled the meeting for Monday."},
            {"t": "presentation", "p": "ˌpreznˈteɪʃn", "tr": "apresentação", "ex": "The presentation lasted one hour."},
            {"t": "supplier", "p": "səˈplaɪər", "tr": "fornecedor", "ex": "Contact the supplier for more fertilizer."},
            {"t": "deadline", "p": "ˈdedlaɪn", "tr": "prazo", "ex": "The deadline for the proposal is Friday."},
            {"t": "contract", "p": "ˈkɒntrækt", "tr": "contrato", "ex": "Sign the contract and send it back."}
        ],
        "DAY 3: Time & Pronunciation": [
            {"t": "yesterday", "p": "ˈjestərdeɪ", "tr": "ontem", "ex": "The prices dropped yesterday."},
            {"t": "yesterday morning", "p": "ˈjestərdeɪ ˈmɔːrnɪŋ", "tr": "ontem de manhã", "ex": "I was in the lab yesterday morning."},
            {"t": "yesterday afternoon", "p": "ˈjestərdeɪ ˌæftərˈnuːn", "tr": "ontem à tarde", "ex": "The rain started yesterday afternoon."},
            {"t": "last week", "p": "lɑːst wiːk", "tr": "semana passada", "ex": "We received the shipment last week."},
            {"t": "last Friday", "p": "lɑːst ˈfraɪdeɪ", "tr": "última sexta-feira", "ex": "We closed the deal last Friday."},
            {"t": "two days ago", "p": "tuː deɪz əˈgoʊ", "tr": "dois dias atrás", "ex": "The shipment arrived two days ago."},
            {"t": "a week ago", "p": "ə wiːk əˈɡoʊ", "tr": "uma semana atrás", "ex": "The audit finished a week ago."},
            {"t": "last month", "p": "lɑːst mʌnθ", "tr": "mês passado", "ex": "Our sales hit a record last month."},
            {"t": "this morning", "p": "ðɪs ˈmɔːrnɪŋ", "tr": "esta manhã", "ex": "The power went out this morning."},
            {"t": "on Monday", "p": "ɒn ˈmʌndeɪ", "tr": "na segunda-feira", "ex": "I have a flight on Monday."},
            {"t": "before lunch", "p": "bɪˈfɔːr lʌntʃ", "tr": "antes do almoço", "ex": "Can we talk before lunch?"},
            {"t": "on time", "p": "ɒn taɪm", "tr": "no horário", "ex": "The bus arrived exactly on time."}
        ],
        "DAY 4: Audio & Operations": [
            {"t": "clean → cleaned", "p": "kliːnd", "tr": "limpar / limpou", "ex": "We cleaned the tractor after use."},
            {"t": "watch → watched", "p": "wɒtʃt", "tr": "assistir / assistiu", "ex": "I watched the market news."},
            {"t": "want → wanted", "p": "ˈwɒntɪd", "tr": "querer / quis", "ex": "They wanted a bigger discount."},
            {"t": "rest → rested", "p": "ˈrestɪd", "tr": "descansar / descansou", "ex": "The team rested after the harvest."},
            {"t": "sales report", "p": "seɪlz rɪˈpɔːrt", "tr": "relatório de vendas", "ex": "Check the sales report for Q1."},
            {"t": "proposal", "p": "prəˈpəʊzəl", "tr": "proposta", "ex": "The client accepted our proposal."},
            {"t": "delivery", "p": "dɪˈlɪvəri", "tr": "entrega", "ex": "Expect the delivery by noon."},
            {"t": "order", "p": "ˈɔːrdər", "tr": "pedido", "ex": "Place an order for more seeds."},
            {"t": "voicemail", "p": "ˈvɔɪsmeɪl", "tr": "caixa de mensagens", "ex": "I left a voicemail for the director."},
            {"t": "update", "p": "ʌpˈdeɪt", "tr": "atualização", "ex": "The software update is mandatory."},
            {"t": "document", "p": "ˈdɒkjʊmənt", "tr": "documento", "ex": "Don't forget to sign the document."},
            {"t": "kickoff meeting", "p": "ˈkɪkɒf ˈmiːtɪŋ", "tr": "reunião de início", "ex": "The kickoff meeting is tomorrow."}
        ],
        "DAY 5: Professional Practice": [
            {"t": "I finished it before lunch", "p": "bɪˈfɔːr lʌntʃ", "tr": "terminei antes do almoço", "ex": "Good news: I finished it before lunch."},
            {"t": "I emailed it to everyone", "p": "ˈeɪmeɪld ɪt", "tr": "enviei para todos", "ex": "Check your inbox, I emailed it to everyone."},
            {"t": "I called three clients", "p": "kɔːld θriː", "tr": "liguei para três clientes", "ex": "I called three clients this morning."},
            {"t": "We completed everything", "p": "kəmˈpliːtɪd", "tr": "completamos tudo", "ex": "We completed everything on the list."},
            {"t": "The project is ready", "p": "ˈredi", "tr": "o projeto está pronto", "ex": "The project is ready for launch."},
            {"t": "Good job!", "p": "ɡʊd dʒɒb", "tr": "bom trabalho!", "ex": "You fixed the issue. Good job!"},
            {"t": "Great teamwork!", "p": "ɡreɪt ˈtiːmwɜːrk", "tr": "ótimo trabalho em equipe!", "ex": "We delivered on time. Great teamwork!"},
            {"t": "They loved it!", "p": "lʌvd ɪt", "tr": "eles adoraram!", "ex": "I showed them the demo and they loved it!"},
            {"t": "We worked together", "p": "wɜːrkt təˈɡeðər", "tr": "trabalhamos juntos", "ex": "We worked together at the previous company."},
            {"t": "follow-up meeting", "p": "ˈfɒləʊʌp ˈmiːtɪŋ", "tr": "reunião de acompanhamento", "ex": "Let's schedule a follow-up meeting."},
            {"t": "on time", "p": "ɒn taɪm", "tr": "no prazo / no horário", "ex": "Everything is on time."},
            {"t": "task", "p": "tɑːsk", "tr": "tarefa", "ex": "Your next task is to verify the sensors."}
        ]
    }
}

# --- LÓGICA DO MOTOR ---
st.sidebar.markdown("## 🚜 Talk Agribusiness")
st.sidebar.markdown("---")
aula_sel = st.sidebar.selectbox("Módulo:", list(data.keys()))
dia_sel = st.sidebar.selectbox("Dia de Estudo:", list(data[aula_sel].keys()))

lista_cards = data[aula_sel][dia_sel]

# Controle de Sessão
idx_key = f"{aula_sel}_{dia_sel}_idx"
flipped_key = f"{aula_sel}_{dia_sel}_flipped"

if idx_key not in st.session_state: st.session_state[idx_key] = 0
if flipped_key not in st.session_state: st.session_state[flipped_key] = False

idx = st.session_state[idx_key]
card = lista_cards[idx]

# --- INTERFACE ---
st.title("Agro Executive Flashcards")
st.write(f"Sessão: {aula_sel} | {dia_sel}")

with st.container():
    st.markdown('<div class="flashcard-container">', unsafe_allow_html=True)
    
    if not st.session_state[flipped_key]:
        st.markdown(f"<h1 style='font-size: 55px; height: 140px; display: flex; align-items: center; justify-content: center;'>{card['t']}</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: #6c757d; font-size: 20px;'>/{card.get('p', '')}/</p>", unsafe_allow_html=True)
        
        if st.button("🔄 REVELAR CONTEÚDO", type="primary"):
            st.session_state[flipped_key] = True
            st.rerun()
    else:
        st.markdown(f"<h2 style='color: #28a745; height: 100px; display: flex; align-items: center; justify-content: center;'>{card['tr']}</h2>", unsafe_allow_html=True)
        st.divider()
        st.markdown(f"**Exemplo de uso:**")
        st.write(f"*{card.get('ex', '')}*")
        
        if st.button("⬅️ VOLTAR"):
            st.session_state[flipped_key] = False
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

if st.button("🔊 OUVIR PRONÚNCIA"):
    texto_audio = card['t'].split('→')[-1].strip()
    tts = gTTS(text=texto_audio, lang='en')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    st.audio(fp, format='audio/mp3')

col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    if st.button("ANTERIOR") and idx > 0:
        st.session_state[idx_key] -= 1
        st.session_state[flipped_key] = False
        st.rerun()
with col3:
    if st.button("PRÓXIMO") and idx < len(lista_cards) - 1:
        st.session_state[idx_key] += 1
        st.session_state[flipped_key] = False
        st.rerun()

progresso = (idx + 1) / len(lista_cards)
st.progress(progresso)
st.markdown(f"<p style='text-align: center;'>Progresso: {idx + 1} de {len(lista_cards)}</p>", unsafe_allow_html=True)
