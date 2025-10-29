"""
Экран приветствия и информации о приложении.
"""

import streamlit as st

def show_about_screen():
    """Отображает экран приветствия About."""
    
    # Заголовок и логотип
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Отображаем логотип
        try:
            st.image("assets/logo.png", width=400, use_container_width=False)
        except:
            st.markdown("<h1 style='text-align: center;'>  TailSense</h1>", unsafe_allow_html=True)  # Fallback если логотип недоступен
        
        st.markdown("<h1 style='text-align: center;'>  🐾 TailSense</h1>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Описание приложения
    st.markdown("""
    ## Добро пожаловать в TailSense!
    
    **TailSense** — это ветеринарный помощник на основе ИИ, который поможет вам:
    
    🔍 **Быстро оценить симптомы** вашего питомца
    💡 **Получить рекомендации** по первой помощи
    
    """)
    
    st.warning("""
    ⚠️ **Важно**: Этот сервис не заменяет профессиональную ветеринарную помощь. 
    При серьезных симптомах обязательно обратитесь к ветеринару!
    """)
    
    st.markdown("---")
    
    # Кнопка начала работы
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 Начать", use_container_width=True, type="secondary"):
            st.session_state.page = 2
            st.rerun()
    
    # Дополнительная информация
    with st.expander("📖 Дополнительная информация"):
        st.markdown("""
        **О проекте TailSense:**
        
        Этот проект разработан для помощи фермерам и ветеринарам в понимании 
        состояния здоровья животных. Мы используем современные технологии ИИ 
        для анализа симптомов и предоставления рекомендаций.
        
        **Поддерживаемые животные:**
        - Собаки и кошки
        - Птицы
        - Кролики
        - Крупный рогатый скот
        - Другие домашние животные
        """)
