"""
Экран конфигурации: выбор животного и симптомов.
"""

import streamlit as st
from components.animal_card import show_animal_selector
from components.symptom_selector import show_symptom_selector

def show_configurator_screen():
    """Отображает экран конфигуратора для выбора животного и симптомов."""
    
    st.title("🔧 Настройка консультации")
    st.markdown("Пожалуйста, выберите вашего питомца и укажите симптомы для получения персональных рекомендаций.")
    
    st.markdown("---")
    
    # Выбор животного
    st.subheader("1️⃣ Выберите животное")
    selected_animal = show_animal_selector()
    
    if selected_animal:
        st.success(f"Выбрано: {selected_animal}")
        
        st.markdown("---")
        
        # Выбор симптомов
        st.subheader("2️⃣ Укажите симптомы")
        selected_symptoms = show_symptom_selector()
        
        st.markdown("---")
        
        # Кнопки навигации
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("⬅️ Назад", use_container_width=True):
                st.session_state.page = 1
                st.rerun()
        
        with col3:
            # Проверяем, что выбрано хотя бы одно животное и один симптом
            if selected_symptoms:
                if st.button("💬 Перейти к чату", use_container_width=True, type="primary"):
                    # Данные уже сохранены в session_state компонентами
                    st.session_state.page = 3
                    st.rerun()
            else:
                st.button("💬 Перейти к чату", use_container_width=True, disabled=True)
                st.caption("Выберите хотя бы один симптом для продолжения")
    