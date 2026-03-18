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
"Aula 1: Verb To Be & Introductions": {

    "DAY 1": {
        "Vocabulary": [
            {"t": "I am", "p": "aɪ æm", "tr": "eu sou/estou", "ex": "I am ready."},
            {"t": "You are", "p": "juː ɑːr", "tr": "você é/está", "ex": "You are my colleague."},
            {"t": "I am from", "p": "", "tr": "eu sou de", "ex": "I am from Brazil."},
            {"t": "You are from", "p": "", "tr": "você é de", "ex": "You are from Argentina."},
            {"t": "name", "p": "neɪm", "tr": "nome", "ex": "My name is John."},
            {"t": "profession", "p": "", "tr": "profissão", "ex": "My profession is engineer."},
            {"t": "country", "p": "", "tr": "país", "ex": "Brazil is my country."},
            {"t": "My name is...", "p": "", "tr": "meu nome é...", "ex": "My name is Carlos."},
            {"t": "Where are you from?", "p": "", "tr": "de onde você é?", "ex": "Where are you from?"},
            {"t": "a manager", "p": "", "tr": "um gerente", "ex": "I am a manager."},
            {"t": "a coordinator", "p": "", "tr": "um coordenador(a)", "ex": "She is a coordinator."},
            {"t": "Nice to meet you", "p": "", "tr": "prazer em conhecê-lo(a)", "ex": "Nice to meet you!"},
            {"t": "Nice to meet you too", "p": "", "tr": "prazer também", "ex": "Nice to meet you too!"},
            {"t": "What is your name?", "p": "", "tr": "qual é o seu nome?", "ex": "What is your name?"},
            {"t": "my", "p": "", "tr": "meu/minha", "ex": "My name is Ana."},
            {"t": "your", "p": "", "tr": "seu/sua", "ex": "Your name is Pedro."}
        ]
    },

    "DAY 2": {
        "Vocabulary": [
            {"t": "an engineer", "p": "", "tr": "engenheiro(a)", "ex": "He is an engineer."},
            {"t": "a consultant", "p": "", "tr": "consultor(a)", "ex": "She is a consultant."},
            {"t": "a director", "p": "", "tr": "diretor(a)", "ex": "He is a director."},
            {"t": "an analyst", "p": "", "tr": "analista", "ex": "I am an analyst."},
            {"t": "an accountant", "p": "", "tr": "contador(a)", "ex": "She is an accountant."},
            {"t": "Brazil", "p": "", "tr": "Brasil", "ex": "I am from Brazil."},
            {"t": "Brazilian", "p": "", "tr": "brasileiro(a)", "ex": "I am Brazilian."},
            {"t": "USA / United States", "p": "", "tr": "Estados Unidos", "ex": "He is from the USA."},
            {"t": "American", "p": "", "tr": "americano(a)", "ex": "She is American."},
            {"t": "Argentina", "p": "", "tr": "Argentina", "ex": "They are from Argentina."},
            {"t": "Argentinian", "p": "", "tr": "argentino(a)", "ex": "He is Argentinian."},
            {"t": "Mexico", "p": "", "tr": "México", "ex": "She is from Mexico."},
            {"t": "Mexican", "p": "", "tr": "mexicano(a)", "ex": "He is Mexican."},
            {"t": "Canada", "p": "", "tr": "Canadá", "ex": "They are from Canada."},
            {"t": "Canadian", "p": "", "tr": "canadense", "ex": "She is Canadian."},
            {"t": "Spain", "p": "", "tr": "Espanha", "ex": "He is from Spain."},
            {"t": "Spanish", "p": "", "tr": "espanhol(a)", "ex": "She is Spanish."},
            {"t": "Portugal", "p": "", "tr": "Portugal", "ex": "I am from Portugal."},
            {"t": "Portuguese", "p": "", "tr": "português(a)", "ex": "He is Portuguese."}
        ]
    },

    "DAY 3": {
        "Vocabulary": [
            {"t": "@ (at)", "p": "", "tr": "arroba", "ex": "Use at in email."},
            {"t": ". (dot)", "p": "", "tr": "ponto", "ex": "Dot com."},
            {"t": "_ (underscore)", "p": "", "tr": "underline", "ex": "Use underscore."},
            {"t": "- (dash)", "p": "", "tr": "hífen", "ex": "Use dash."},
            {"t": "email", "p": "", "tr": "e-mail", "ex": "My email is..."},
            {"t": "address", "p": "", "tr": "endereço", "ex": "What is your address?"},
            {"t": "surname", "p": "", "tr": "sobrenome", "ex": "My surname is Silva."},
            {"t": "phone number", "p": "", "tr": "número de telefone", "ex": "My phone number is..."},
            {"t": "How do you spell?", "p": "", "tr": "como se soletra?", "ex": "How do you spell your name?"},
            {"t": "am not", "p": "", "tr": "não sou/estou", "ex": "I am not a manager."},
            {"t": "aren't", "p": "", "tr": "não é/não está", "ex": "You aren't ready."},
            {"t": "Are you?", "p": "", "tr": "você é/está?", "ex": "Are you ready?"}
        ]
    },

    "DAY 4": {
        "Vocabulary": [
            {"t": "city", "p": "", "tr": "cidade", "ex": "My city is Campinas."},
            {"t": "company", "p": "", "tr": "empresa", "ex": "I work in a company."},
            {"t": "meeting", "p": "", "tr": "reunião", "ex": "We have a meeting."},
            {"t": "agribusiness", "p": "", "tr": "agronegócio", "ex": "I work with agribusiness."},
            {"t": "happy", "p": "", "tr": "feliz", "ex": "I am happy."},
            {"t": "sad", "p": "", "tr": "triste", "ex": "She is sad."},
            {"t": "Thank you", "p": "", "tr": "obrigado(a)", "ex": "Thank you!"},
            {"t": "Please", "p": "", "tr": "por favor", "ex": "Help me, please."},
            {"t": "Spell it, please", "p": "", "tr": "soletre, por favor", "ex": "Spell it, please."}
        ]
    },

    "DAY 5": {
        "Vocabulary": [
            {"t": "here", "p": "", "tr": "aqui", "ex": "I am here."},
            {"t": "information", "p": "", "tr": "informação", "ex": "This is important information."},
            {"t": "I am a teacher", "p": "", "tr": "eu sou professor", "ex": "I am a teacher."},
            {"t": "You are an analyst", "p": "", "tr": "você é analista", "ex": "You are an analyst."},
            {"t": "I am from Portugal", "p": "", "tr": "eu sou de Portugal", "ex": "I am from Portugal."},
            {"t": "You are from Mexico", "p": "", "tr": "você é do México", "ex": "You are from Mexico."},
            {"t": "Are you a coordinator?", "p": "", "tr": "você é um coordenador?", "ex": "Are you a coordinator?"},
            {"t": "I am not a manager", "p": "", "tr": "eu não sou gerente", "ex": "I am not a manager."},
            {"t": "You aren't a consultant", "p": "", "tr": "você não é consultor", "ex": "You aren't a consultant."}
        ]
    }
},

"Aula 2: People & Work Context": {

    "DAY 1": {
        "Vocabulary": [
            {"t": "available", "p": "", "tr": "disponível", "ex": "He is available now."},
            {"t": "in a meeting", "p": "", "tr": "em reunião", "ex": "She is in a meeting."},
            {"t": "on vacation", "p": "", "tr": "de férias", "ex": "He is on vacation."},
            {"t": "in the office", "p": "", "tr": "no escritório", "ex": "She is in the office."},
            {"t": "at home", "p": "", "tr": "em casa", "ex": "They are at home."},
            {"t": "sales coordinator", "p": "", "tr": "coordenador de vendas", "ex": "He is a sales coordinator."},
            {"t": "engineer", "p": "", "tr": "engenheiro", "ex": "She is an engineer."},
            {"t": "manager", "p": "", "tr": "gerente", "ex": "He is a manager."},
            {"t": "boss", "p": "", "tr": "chefe", "ex": "She is my boss."},
            {"t": "team", "p": "", "tr": "equipe", "ex": "This is my team."},
            {"t": "supervisor", "p": "", "tr": "supervisor", "ex": "He is the supervisor."},
            {"t": "excited", "p": "", "tr": "animado", "ex": "I am excited."},
            {"t": "now", "p": "", "tr": "agora", "ex": "I am busy now."},
            {"t": "right now", "p": "", "tr": "agora mesmo", "ex": "She is in a meeting right now."},
            {"t": "extension", "p": "", "tr": "ramal", "ex": "My extension is 123."},
            {"t": "She is", "p": "", "tr": "ela é/está", "ex": "She is ready."},
            {"t": "He is", "p": "", "tr": "ele é/está", "ex": "He is available."},
            {"t": "They are", "p": "", "tr": "eles são/estão", "ex": "They are busy."},
            {"t": "This is", "p": "", "tr": "este/esta é", "ex": "This is my manager."}
        ]
    },

    "DAY 2": {
        "Vocabulary": [
            {"t": "He is not", "p": "", "tr": "ele não é/está", "ex": "He is not available."},
            {"t": "She is not", "p": "", "tr": "ela não é/está", "ex": "She is not here."},
            {"t": "They are not", "p": "", "tr": "eles não são/estão", "ex": "They are not ready."},
            {"t": "Is she?", "p": "", "tr": "ela é/está?", "ex": "Is she available?"},
            {"t": "Is he?", "p": "", "tr": "ele é/está?", "ex": "Is he busy?"},
            {"t": "Are they?", "p": "", "tr": "eles são/estão?", "ex": "Are they at work?"},
            {"t": "agronomist", "p": "", "tr": "agrônomo", "ex": "He is an agronomist."},
            {"t": "veterinarian", "p": "", "tr": "veterinário", "ex": "She is a veterinarian."},
            {"t": "sales team", "p": "", "tr": "equipe de vendas", "ex": "I am in the sales team."},
            {"t": "finance team", "p": "", "tr": "equipe financeira", "ex": "She is in the finance team."},
            {"t": "logistics team", "p": "", "tr": "equipe de logística", "ex": "He is in the logistics team."},
            {"t": "operations team", "p": "", "tr": "equipe de operações", "ex": "They are in operations."},
            {"t": "HR team", "p": "", "tr": "recursos humanos", "ex": "She works in HR."},
            {"t": "agribusiness sector", "p": "", "tr": "setor do agronegócio", "ex": "I work in agribusiness."},
            {"t": "legal team", "p": "", "tr": "equipe jurídica", "ex": "He is in the legal team."},
            {"t": "IT team", "p": "", "tr": "equipe de TI", "ex": "She is in IT."},
            {"t": "at a conference", "p": "", "tr": "em uma conferência", "ex": "They are at a conference."},
            {"t": "on a business trip", "p": "", "tr": "em viagem de negócios", "ex": "He is on a business trip."},
            {"t": "at an event", "p": "", "tr": "em um evento", "ex": "She is at an event."},
            {"t": "happy", "p": "", "tr": "feliz", "ex": "I am happy."},
            {"t": "excited", "p": "", "tr": "animado", "ex": "They are excited."},
            {"t": "tired", "p": "", "tr": "cansado", "ex": "He is tired."},
            {"t": "ready", "p": "", "tr": "pronto", "ex": "She is ready."}
        ]
    },

    "DAY 3": {
        "Vocabulary": [
            {"t": "ten", "p": "", "tr": "dez", "ex": "Ten people are here."},
            {"t": "eleven", "p": "", "tr": "onze", "ex": "Eleven workers."},
            {"t": "twelve", "p": "", "tr": "doze", "ex": "Twelve months."},
            {"t": "thirteen", "p": "", "tr": "treze", "ex": "Thirteen days."},
            {"t": "fourteen", "p": "", "tr": "quatorze", "ex": "Fourteen teams."},
            {"t": "fifteen", "p": "", "tr": "quinze", "ex": "Fifteen minutes."},
            {"t": "sixteen", "p": "", "tr": "dezesseis", "ex": "Sixteen employees."},
            {"t": "seventeen", "p": "", "tr": "dezessete", "ex": "Seventeen clients."},
            {"t": "eighteen", "p": "", "tr": "dezoito", "ex": "Eighteen calls."},
            {"t": "nineteen", "p": "", "tr": "dezenove", "ex": "Nineteen emails."},
            {"t": "twenty", "p": "", "tr": "vinte", "ex": "Twenty people."},
            {"t": "twenty-one", "p": "", "tr": "vinte e um", "ex": "Twenty-one days."},
            {"t": "twenty-two", "p": "", "tr": "vinte e dois", "ex": "Twenty-two workers."},
            {"t": "twenty-five", "p": "", "tr": "vinte e cinco", "ex": "Twenty-five meetings."},
            {"t": "thirty", "p": "", "tr": "trinta", "ex": "Thirty days."},
            {"t": "week", "p": "", "tr": "semana", "ex": "This week is busy."},
            {"t": "today", "p": "", "tr": "hoje", "ex": "Today is Monday."},
            {"t": "Monday", "p": "", "tr": "segunda-feira", "ex": "Meeting on Monday."},
            {"t": "Tuesday", "p": "", "tr": "terça-feira", "ex": "Call on Tuesday."},
            {"t": "Wednesday", "p": "", "tr": "quarta-feira", "ex": "Event on Wednesday."},
            {"t": "Thursday", "p": "", "tr": "quinta-feira", "ex": "Trip on Thursday."},
            {"t": "Friday", "p": "", "tr": "sexta-feira", "ex": "Deadline Friday."},
            {"t": "Saturday", "p": "", "tr": "sábado", "ex": "Work on Saturday."},
            {"t": "Sunday", "p": "", "tr": "domingo", "ex": "Rest on Sunday."}
        ]
    },

    "DAY 4": {
        "Vocabulary": [
            {"t": "He works in", "p": "", "tr": "ele trabalha em", "ex": "He works in logistics."},
            {"t": "She works in", "p": "", "tr": "ela trabalha em", "ex": "She works in finance."},
            {"t": "My extension is", "p": "", "tr": "meu ramal é", "ex": "My extension is 456."},
            {"t": "The meeting is on", "p": "", "tr": "a reunião é na", "ex": "The meeting is on Monday."},
            {"t": "He is available on", "p": "", "tr": "ele está disponível na", "ex": "He is available on Tuesday."},
            {"t": "She is in room", "p": "", "tr": "ela está na sala", "ex": "She is in room 10."},
            {"t": "The conference is on floor", "p": "", "tr": "a conferência é no andar", "ex": "The conference is on floor 2."},
            {"t": "Is he available on", "p": "", "tr": "ele está disponível na?", "ex": "Is he available on Friday?"},
            {"t": "They are on the team", "p": "", "tr": "eles estão na equipe", "ex": "They are on the finance team."},
            {"t": "floor", "p": "", "tr": "andar", "ex": "Second floor."},
            {"t": "Who is", "p": "", "tr": "quem é", "ex": "Who is your manager?"},
            {"t": "Where is", "p": "", "tr": "onde está", "ex": "Where is he?"},
            {"t": "Who are they?", "p": "", "tr": "quem são eles?", "ex": "Who are they?"},
            {"t": "Where are they?", "p": "", "tr": "onde eles estão?", "ex": "Where are they?"}
        ]
    },

    "DAY 5": {
        "Vocabulary": [
            {"t": "Who is your manager?", "p": "", "tr": "quem é seu gerente?", "ex": "Who is your manager?"},
            {"t": "Where is your manager right now?", "p": "", "tr": "onde está seu gerente agora?", "ex": "Where is your manager right now?"},
            {"t": "Is your manager available?", "p": "", "tr": "seu gerente está disponível?", "ex": "Is your manager available?"},
            {"t": "Who is on your team?", "p": "", "tr": "quem está na sua equipe?", "ex": "Who is on your team?"},
            {"t": "What department are they in?", "p": "", "tr": "em qual departamento eles estão?", "ex": "What department are they in?"},
            {"t": "Are they busy today?", "p": "", "tr": "eles estão ocupados hoje?", "ex": "Are they busy today?"},
            {"t": "Is your manager on vacation?", "p": "", "tr": "seu gerente está de férias?", "ex": "Is your manager on vacation?"},
            {"t": "Who is at the conference?", "p": "", "tr": "quem está na conferência?", "ex": "Who is at the conference?"},
            {"t": "What is your extension?", "p": "", "tr": "qual é seu ramal?", "ex": "What is your extension?"},
            {"t": "Is he busy today?", "p": "", "tr": "ele está ocupado hoje?", "ex": "Is he busy today?"},
            {"t": "Is she available now?", "p": "", "tr": "ela está disponível agora?", "ex": "Is she available now?"},
            {"t": "Are they at the conference?", "p": "", "tr": "eles estão na conferência?", "ex": "Are they at the conference?"},
            {"t": "They aren't on vacation", "p": "", "tr": "eles não estão de férias", "ex": "They aren't on vacation."},
            {"t": "She isn't a manager", "p": "", "tr": "ela não é gerente", "ex": "She isn't a manager."},
            {"t": "They aren't at work", "p": "", "tr": "eles não estão no trabalho", "ex": "They aren't at work today."}
        ]
    }
},
"Bridge 1: What Do You Like?": {

    "DAY 1": {
        "Vocabulary": [
            {"t": "like", "p": "", "tr": "gostar", "ex": "I like movies."},
            {"t": "want", "p": "", "tr": "querer", "ex": "I want to study."},
            {"t": "need", "p": "", "tr": "precisar", "ex": "I need to arrive early."},
            {"t": "prefer", "p": "", "tr": "preferir", "ex": "I prefer to work from home."},
            {"t": "watch", "p": "", "tr": "assistir", "ex": "I like to watch series."},
            {"t": "visit", "p": "", "tr": "visitar", "ex": "I want to visit the farm."},
            {"t": "study", "p": "", "tr": "estudar", "ex": "I need to study English."},
            {"t": "work", "p": "", "tr": "trabalhar", "ex": "I prefer to work at home."},
            {"t": "rest", "p": "", "tr": "descansar", "ex": "I want to rest today."},
            {"t": "go", "p": "", "tr": "ir", "ex": "I go to the office."},
            {"t": "arrive", "p": "", "tr": "chegar", "ex": "I arrive at the farm early."},
            {"t": "come", "p": "", "tr": "vir", "ex": "I come to work every day."}
        ]
    },

    "DAY 2": {
        "Vocabulary": [
            {"t": "office", "p": "", "tr": "escritório", "ex": "I go to the office in the morning."},
            {"t": "home", "p": "", "tr": "casa", "ex": "I prefer to work from home."},
            {"t": "farm", "p": "", "tr": "fazenda", "ex": "I like to visit the farm."},
            {"t": "park", "p": "", "tr": "parque", "ex": "I go to the park with my son."},
            {"t": "mall", "p": "", "tr": "shopping", "ex": "I want to go to the mall."},
            {"t": "movies", "p": "", "tr": "cinema", "ex": "I like to go to the movies."},
            {"t": "church", "p": "", "tr": "igreja", "ex": "I go to church with my family."},
            {"t": "downtown", "p": "", "tr": "centro", "ex": "I like to go downtown."},
            {"t": "mother", "p": "", "tr": "mãe", "ex": "I go with my mother."},
            {"t": "father", "p": "", "tr": "pai", "ex": "I visit my father."},
            {"t": "brother", "p": "", "tr": "irmão", "ex": "I study with my brother."},
            {"t": "sister", "p": "", "tr": "irmã", "ex": "I go with my sister."}
        ]
    },

    "DAY 3": {
        "Vocabulary": [
            {"t": "wife", "p": "", "tr": "esposa", "ex": "I go with my wife."},
            {"t": "husband", "p": "", "tr": "marido", "ex": "She goes with her husband."},
            {"t": "son", "p": "", "tr": "filho", "ex": "I go with my son."},
            {"t": "daughter", "p": "", "tr": "filha", "ex": "I go with my daughter."},
            {"t": "leave", "p": "", "tr": "sair", "ex": "I leave at 6 PM."},
            {"t": "start", "p": "", "tr": "começar", "ex": "I start work early."},
            {"t": "finish", "p": "", "tr": "terminar", "ex": "I finish at 5 PM."},
            {"t": "don't", "p": "", "tr": "não", "ex": "I don't like to work on weekends."},
            {"t": "doesn't", "p": "", "tr": "não (3ª pessoa)", "ex": "She doesn't want to go."},
            {"t": "do", "p": "", "tr": "auxiliar", "ex": "Do you like English?"},
            {"t": "where", "p": "", "tr": "onde", "ex": "Where do you go?"},
            {"t": "what", "p": "", "tr": "o que", "ex": "What do you like?"}
        ]
    },

    "DAY 4": {
        "Vocabulary": [
            {"t": "happy", "p": "", "tr": "feliz", "ex": "I am happy."},
            {"t": "excited", "p": "", "tr": "animado", "ex": "I am excited."},
            {"t": "tired", "p": "", "tr": "cansado", "ex": "I am tired."},
            {"t": "busy", "p": "", "tr": "ocupado", "ex": "I am busy today."},
            {"t": "free", "p": "", "tr": "livre", "ex": "I am free."},
            {"t": "ready", "p": "", "tr": "pronto", "ex": "I am ready."},
            {"t": "worried", "p": "", "tr": "preocupado", "ex": "I am worried."},
            {"t": "nervous", "p": "", "tr": "nervoso", "ex": "I am nervous."},
            {"t": "sad", "p": "", "tr": "triste", "ex": "I am sad."},
            {"t": "available", "p": "", "tr": "disponível", "ex": "I am available."},
            {"t": "on weekends", "p": "", "tr": "nos fins de semana", "ex": "I rest on weekends."},
            {"t": "in the morning", "p": "", "tr": "de manhã", "ex": "I work in the morning."}
        ]
    },

    "DAY 5": {
        "Vocabulary": [
            {"t": "colleague", "p": "", "tr": "colega", "ex": "I work with my colleague."},
            {"t": "client", "p": "", "tr": "cliente", "ex": "I visit my client."},
            {"t": "team", "p": "", "tr": "equipe", "ex": "I work with my team."},
            {"t": "meeting", "p": "", "tr": "reunião", "ex": "I have a meeting."},
            {"t": "schedule", "p": "", "tr": "agenda", "ex": "I have a full schedule."},
            {"t": "business trip", "p": "", "tr": "viagem de negócios", "ex": "I am on a business trip."},
            {"t": "international", "p": "", "tr": "internacional", "ex": "International clients."},
            {"t": "every day", "p": "", "tr": "todos os dias", "ex": "I study every day."},
            {"t": "on Mondays", "p": "", "tr": "às segundas", "ex": "I work on Mondays."},
            {"t": "after work", "p": "", "tr": "depois do trabalho", "ex": "I rest after work."},
            {"t": "early", "p": "", "tr": "cedo", "ex": "I arrive early."},
            {"t": "at home", "p": "", "tr": "em casa", "ex": "I work at home."}
        ]
    }
}
    
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
