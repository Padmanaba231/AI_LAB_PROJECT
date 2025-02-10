import streamlit as st
import requests

# Konfigurasi API Gemini
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent"
API_KEY = os.getenv("API_KEY")   # Ganti dengan API Key Anda

# Konteks tentang BISINDO
BISINDO_CONTEXT = (
    "Anda adalah chatbot yang ahli dalam menjelaskan Bahasa Isyarat Indonesia (BISINDO). "
    "BISINDO adalah bahasa isyarat yang digunakan oleh komunitas Tuli di Indonesia untuk berkomunikasi. "
    "Anda hanya akan menjawab pertanyaan pengguna yang berkaitan tentang BISINDO. "
    "Jawab dengan bahasa yang ringkas dan mudah dimengerti."
)

def send_message_to_gemini(api_url, api_key, user_message, context):
    headers = {'Content-Type': 'application/json'}
    data = {"contents": [{"parts": [{"text": f"{context}\n\nPertanyaan pengguna: {user_message}"}]}]}
    try:
        response = requests.post(f"{api_url}?key={api_key}", headers=headers, json=data)
        response_data = response.json()
        candidates = response_data.get('candidates', [])
        if candidates:
            return candidates[0].get('content', {}).get('parts', [{}])[0].get('text', '') or "Maaf, bot tidak dapat memberikan balasan."
        return "Maaf, bot tidak dapat memberikan balasan."
    except requests.exceptions.RequestException as e:
        return f"Terjadi kesalahan saat menghubungi API: {str(e)}"

def chatbot_bisindo():
    st.title("Chatbot BISINDO")

    # Inisialisasi sesi untuk menyimpan riwayat percakapan
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Render riwayat percakapan
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input pengguna
    if user_input := st.chat_input("Tanyakan sesuatu tentang BISINDO..."):
        # Tambahkan input pengguna ke riwayat
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Proses respons dari Gemini
        with st.chat_message("assistant"):
            bot_message_placeholder = st.empty()
            bot_message_placeholder.markdown("Sedang menjawab...")
            bot_reply = send_message_to_gemini(API_URL, API_KEY, user_input, BISINDO_CONTEXT)
            bot_message_placeholder.markdown(bot_reply)

        # Tambahkan respons bot ke riwayat
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        
