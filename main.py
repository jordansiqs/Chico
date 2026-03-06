import streamlit as st
from supabase import create_client
from groq import Groq

# 1. Conexão Segura (Lendo do secrets.toml)
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.set_page_config(page_title="Chico Mentor", layout="wide")

# 2. Interface (Dashboard)
st.title("🧠 Chico Mentor: Autonomia Poliglota")
st.info("⚡ Você tem 10 faíscas diárias. O reset ocorre à meia-noite.")

# 3. Chat Flutuante (Sidebar)
with st.sidebar:
    st.header("💬 Conversar com o Chico")
    pergunta = st.chat_input("Diga algo em Português...")
    if pergunta:
        st.write(f"O Chico está processando: {pergunta}")
        # Aqui entra a lógica da Groq que já testamos
