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
    }
}
