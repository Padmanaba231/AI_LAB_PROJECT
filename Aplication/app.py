import os
import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv

# Konfigurasi API Gemini
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Buat konfigurasi model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 500,
    "response_mime_type": "text/plain",
}

# Inisialisasi model Gemini
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
)

# Prompt engineering: Chatbot asisten untuk orang tuli dan BISINDO
prompt = """You are an assistant designed to help people who are deaf and hard of hearing understand BISINDO (Bahasa Isyarat Indonesia) alphabet. 
Your responses should be simple, clear, and concise, providing information about the BISINDO alphabet, including its gestures, and how it can be learned. 
If a user asks about a letter, describe the sign language gesture for that letter.
You should also offer explanations on the use of BISINDO in everyday conversation in a friendly tone. Always respond in Indonesian language!"""

# Mulai sesi chat dengan prompt
chat_session = model.start_chat(
    history=[{"role": "model", "parts": prompt}]
)

# Menyimpan riwayat chat
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Fungsi untuk menampilkan pesan pada UI chatbot
def direct_chat(text, role):
    with st.chat_message(role):
        st.write(text)

# Fungsi untuk chatbot
def chatbot():
    st.header("Tampilan Chatbot")
    
    # Jika belum ada percakapan, bot memulai percakapan
    if len(st.session_state.chat_history) == 0:
        initial_message = "Halo! Saya siap membantu kamu memahami BISINDO (Bahasa Isyarat Indonesia). Ada yang ingin kamu pelajari hari ini? 😊"
        st.session_state.chat_history.append({"role": "assistant", "text": initial_message})
    
    # Tampilkan semua chat sebelumnya, kecuali prompt
    for message in st.session_state.chat_history:
        if message["role"] != "model":  # Pastikan prompt tidak ditampilkan
            direct_chat(message["text"], role=message["role"])

    # Input teks dari pengguna
    user_input = st.chat_input("Ketik sesuatu tentang BISINDO...")

    if user_input:
        # Simpan pesan pengguna ke riwayat chat
        st.session_state.chat_history.append({"role": "user", "text": user_input})

        # Kirim pesan ke model dan dapatkan respons
        response = chat_session.send_message(user_input)

        # Simpan respons dari Gemini ke riwayat chat
        st.session_state.chat_history.append({"role": "assistant", "text": response.text})
        
        # Tampilkan pesan baru
        direct_chat(user_input, role="user")
        direct_chat(response.text, role="assistant")

# Sidebar untuk navigasi
st.sidebar.title('Menu')
choice = st.sidebar.radio(label="Pilih Menu:", options=['index', 'chatbot'])

# Mengarahkan ke fungsi berdasarkan pilihan menu
if choice == "index":
    # Fungsi index bisa kosong atau diisi sesuai kebutuhan
    st.write("Menu utama kosong")
else:
    chatbot()
