import os
import streamlit as st
from supabase import create_client
from groq import Groq
from dotenv import load_dotenv

# 1. Carrega as chaves do arquivo .env
load_dotenv()

SUPABASE_URL = "https://ofsvcqkyssbqanvmsykj.supabase.co"
SUPABASE_KEY = os.getenv("SUPABASE_KEY") # Adicione esta chave no seu .env também!
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# 2. Inicializa as conexões
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
client = Groq(api_key=GROQ_API_KEY)

# --- CONFIGURAÇÃO VISUAL ---
st.set_page_config(page_title="Chico Mentor", layout="wide", page_icon="🧠")

st.markdown("""
    <style>
    .card-mestre { background: white; padding: 25px; border-radius: 15px; 
                   box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 25px; 
                   border-left: 10px solid #27ae60; }
    .idioma-row { display: grid; grid-template-columns: 1fr 3fr 2fr 0.5fr; gap: 15px; 
                  padding: 12px 0; border-bottom: 1px solid #f0f0f0; align-items: center; }
    .fonetica { color: #888; font-style: italic; font-size: 0.9em; }
    .stChatFloatingInputContainer { bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# --- LÓGICA DE USUÁRIO (SIMULADA PARA O DASHBOARD) ---
# Em produção, usaremos st.experimental_user ou o Auth do Supabase
user_id = "jordan_teste" 

# --- DASHBOARD PRINCIPAL ---
st.title("🧠 Dashboard de Autonomia")
st.subheader("Sua Biblioteca de Conquistas Poliglotas")

# Exibe o contador de energia
st.info("⚡ Você tem 10 faíscas diárias. O reset ocorre à meia-noite.")

# Busca os Cards no Banco
try:
    cards_db = supabase.table("mentoria_cards").select("*").order("criado_em", desc=True).execute()
    
    if not cards_db.data:
        st.write("O Chico está aguardando sua primeira frase no chat ao lado! ➡️")
    
    for card in cards_db.data:
        with st.container():
            st.markdown(f"""
            <div class="card-mestre">
                <small style="color: #27ae60;">Frase Original:</small>
                <h3 style="margin-top: 0;">{card['frase_original']}</h3>
                <div class="idioma-row"><b>🇺🇸 Inglês</b> <span>{card['en_texto']}</span> <span class="fonetica">[{card['en_fonetica']}]</span> 🔊</div>
                <div class="idioma-row"><b>🇪🇸 Espanhol</b> <span>{card['es_texto']}</span> <span class="fonetica">[{card['es_fonetica']}]</span> 🔊</div>
                <div class="idioma-row"><b>🇫🇷 Francês</b> <span>{card['fr_texto']}</span> <span class="fonetica">[{card['fr_fonetica']}]</span> 🔊</div>
                <div class="idioma-row"><b>🇮🇹 Italiano</b> <span>{card['it_texto']}</span> <span class="fonetica">[{card['it_fonetica']}]</span> 🔊</div>
            </div>
            """, unsafe_allow_html=True)
except Exception as e:
    st.error(f"Erro ao carregar cards: {e}")

# --- CHAT FLUTUANTE (OPÇÃO A - NA SIDEBAR) ---
with st.sidebar:
    st.header("💬 Conversar com o Chico")
    st.write("Descreva uma situação ou frase em Português.")
    
    prompt_usuario = st.chat_input("Diga algo ao Chico...")

    if prompt_usuario:
        with st.spinner("O Chico está conectando os nexos..."):
            # O sistema pede à Groq para gerar a resposta no formato exato que você quer
            instrucao = """
            Aja como o CHICO (Mentor Freire/Bodmer). 
            Retorne APENAS um JSON com os campos: 
            en_texto, en_fonetica, es_texto, es_fonetica, fr_texto, fr_fonetica, it_texto, it_fonetica.
            Baseie a fonética na pronúncia brasileira simplificada.
            """
            
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": instrucao},
                    {"role": "user", "content": prompt_usuario}
                ],
                model="llama-3.3-70b-versatile",
                response_format={"type": "json_object"} # Garante que a IA responda dados limpos
            )
            
            import json
            res = json.loads(chat_completion.choices[0].message.content)
            
            # Salva o novo card no Supabase automaticamente
            supabase.table("mentoria_cards").insert({
                "frase_original": prompt_usuario,
                "en_texto": res['en_texto'], "en_fonetica": res['en_fonetica'],
                "es_texto": res['es_texto'], "es_fonetica": res['es_fonetica'],
                "fr_texto": res['fr_texto'], "fr_fonetica": res['fr_fonetica'],
                "it_texto": res['it_texto'], "it_fonetica": res['it_fonetica']
            }).execute()
            
            st.success("Novo card gerado! Verifique seu Dashboard.")
            st.rerun()