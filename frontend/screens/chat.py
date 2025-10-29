"""
Экран чата с ИИ-ветеринаром.
"""

import streamlit as st
from components.chat_widget import show_chat_interface
from utils.api_client import send_message, reset_agent_session

def show_chat_screen():
    """Отображает экран чата с ветеринаром-помощником."""
    
    # Заголовок и информация о сессии
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.title("💬 Консультация с ветеринаром")
    
    with col2:
        st.markdown("### Действия")
        
        # Кнопка изменения настроек
        if st.button("⚙️ Изменить настройки", use_container_width=True):
            reset_agent_session()  # Сбрасываем сессию агента
            st.session_state.page = 2
            st.rerun()
        
        # Кнопка начать заново
        if st.button("🔄 Начать заново", use_container_width=True):
            # Очищаем данные сессии
            st.session_state.selected_animal = ""
            st.session_state.selected_symptoms = []
            st.session_state.chat_history = []
            reset_agent_session()  # Сбрасываем сессию агента
            st.session_state.page = 1
            st.rerun()
    
    st.markdown("---")
    
    # Проверяем, что у нас есть необходимые данные
    if not st.session_state.selected_animal or not st.session_state.selected_symptoms:
        st.error("❌ Не хватает данных для консультации. Пожалуйста, вернитесь к настройкам.")
        if st.button("⚙️ Перейти к настройкам"):
            st.session_state.page = 2
            st.rerun()
        return
    
    # Интерфейс чата
    show_chat_interface()
    
    # Поле ввода сообщения
    user_message = st.chat_input("Опишите проблему вашего питомца...")
    
    if user_message:
        # Добавляем сообщение пользователя в историю
        st.session_state.chat_history.append({
            "role": "user", 
            "content": user_message
        })
        
        # Получаем ответ от API (пока заглушка)
        try:
            with st.spinner("Ветеринар думает..."):
                response = send_message(
                    animal=st.session_state.selected_animal,
                    symptoms=st.session_state.selected_symptoms,
                    message=user_message,
                    history=st.session_state.chat_history
                )
                
                # Добавляем ответ ассистента в историю
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": response
                })
                
                # Перезагружаем страницу для обновления чата
                st.rerun()
                
        except Exception as e:
            st.error(f"Ошибка при получении ответа: {str(e)}")
    
    # Дополнительная информация
    with st.sidebar:
        st.markdown("### 📋 Информация о сессии")
        st.markdown(f"**Животное:** {st.session_state.selected_animal}")
        st.markdown(f"**Симптомы:** {len(st.session_state.selected_symptoms)}")
        st.markdown(f"**Сообщений в чате:** {len(st.session_state.chat_history)}")
        
        # Показываем session_id агента для отладки
        if 'agent_session_id' in st.session_state:
            st.caption(f"**Сессия агента:** {st.session_state.agent_session_id[:8]}...")
        else:
            st.caption("**Сессия агента:** не создана")
        
        st.markdown("---")
        
        # Статус подключения к ИИ-агенту
        from utils.api_client import get_api_status
        
        st.markdown("### 🔌 Статус ИИ-агента")
        api_status = get_api_status()
        
        if api_status["agent_connected"]:
            st.success("🟢 ИИ-ветеринар подключен")
        else:
            st.error("🔴 ИИ-ветеринар недоступен")
            st.caption("Используются резервные ответы")
        
        st.markdown("---")
        
        st.markdown("### ⚠️ Важное напоминание")
        st.warning("""
        Этот чат предоставляет только общие рекомендации. 
        При серьезных симптомах обязательно обратитесь к ветеринару!
        """)

