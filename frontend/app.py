"""
Главный файл Streamlit приложения для ветеринар-помощника.
Осуществляет навигацию между экранами.
"""

import streamlit as st

from screens.about import show_about_screen
from screens.configurator import show_configurator_screen
from screens.chat import show_chat_screen

# Настройка страницы
st.set_page_config(
    page_title="VetChat - Ветеринар Помощник",
    page_icon="🐾",
    layout="centered"
)

# Инициализация состояния сессии
if "page" not in st.session_state:
    st.session_state.page = 1

if "selected_animal" not in st.session_state:
    st.session_state.selected_animal = ""

if "selected_symptoms" not in st.session_state:
    st.session_state.selected_symptoms = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "custom_animal" not in st.session_state:
    st.session_state.custom_animal = ""

if "custom_symptom" not in st.session_state:
    st.session_state.custom_symptom = ""

# Навигация между экранами
def main():
    """Основная функция навигации по экранам."""
    
    if st.session_state.page == 1:
        show_about_screen()
    elif st.session_state.page == 2:
        show_configurator_screen()
    elif st.session_state.page == 3:
        show_chat_screen()
    else:
        # Если что-то пошло не так, возвращаемся на главную
        st.session_state.page = 1
        show_about_screen()

if __name__ == "__main__":
    main()