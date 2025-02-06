import streamlit as st
from homepage import homepage
from chatbot import chatbot_bisindo

# Halaman navigasi
home_page = st.Page(homepage, title="Home", icon=":material/home:")
chatbot_page = st.Page(chatbot_bisindo, title="Chatbot BISINDO", icon=":material/chat:")

# Daftar halaman
pg = st.navigation({
    "Menu": [home_page, chatbot_page],
})

pg.run()
