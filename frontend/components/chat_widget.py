"""
Компонент чата для отображения истории сообщений.
"""

import streamlit as st
from datetime import datetime

def show_chat_interface():
    """
    Отображает интерфейс чата с историей сообщений.
    """
    
    # Контейнер для сообщений чата
    chat_container = st.container()
    
    with chat_container:
        # Если нет истории, показываем приветственное сообщение
        if not st.session_state.chat_history:
            show_welcome_message()
        else:
            # Отображаем все сообщения из истории
            for message in st.session_state.chat_history:
                show_message(message["role"], message["content"])

def show_welcome_message():
    """Отображает приветственное сообщение от ветеринара."""
    
    with st.chat_message("assistant"):
        st.markdown("""
        👋 **Здравствуйте! Я ваш ИИ-ветеринар.**
        
        Я готов помочь вам разобраться с состоянием вашего питомца. 
        
        **Что я вижу из ваших настроек:**
        """)
        
        # Показываем информацию о выбранном животном и симптомах
        if st.session_state.selected_animal:
            st.markdown(f"🐾 **Животное:** {st.session_state.selected_animal}")
        
        if st.session_state.selected_symptoms:
            symptoms_text = ", ".join(st.session_state.selected_symptoms)
            st.markdown(f"🩺 **Симптомы:** {symptoms_text}")
        
        st.markdown("""
        **Как я могу помочь:**
        - Расскажите подробнее о симптомах
        - Опишите, когда они начались
        - Уточните поведение животного
        - Задайте любые вопросы о здоровье питомца
        
        💬 *Опишите проблему в поле ввода ниже...*
        """)

def show_message(role, content):
    """
    Отображает одно сообщение в чате.
    
    Args:
        role (str): Роль отправителя ("user" или "assistant")
        content (str): Содержимое сообщения
    """
    
    with st.chat_message(role):
        if role == "user":
            # Сообщение пользователя
            st.markdown(content)
        else:
            # Сообщение ассистента с дополнительным форматированием
            st.markdown(content)
            
            # Добавляем время отправки для сообщений ассистента
            current_time = datetime.now().strftime("%H:%M")
            st.caption(f"Отправлено в {current_time}")

def show_chat_stats():
    """Отображает статистику чата в боковой панели."""
    
    if st.session_state.chat_history:
        user_messages = len([msg for msg in st.session_state.chat_history if msg["role"] == "user"])
        assistant_messages = len([msg for msg in st.session_state.chat_history if msg["role"] == "assistant"])
        
        st.sidebar.markdown("### 📊 Статистика чата")
        st.sidebar.metric("Ваших сообщений", user_messages)
        st.sidebar.metric("Ответов ветеринара", assistant_messages)

def clear_chat_history():
    """Очищает историю чата."""
    st.session_state.chat_history = []

def export_chat_history():
    """
    Экспортирует историю чата в текстовый формат.
    
    Returns:
        str: Отформатированная история чата
    """
    if not st.session_state.chat_history:
        return "История чата пуста"
    
    export_text = f"""
КОНСУЛЬТАЦИЯ ВЕТЕРИНАРА
======================

Животное: {st.session_state.selected_animal}
Симптомы: {', '.join(st.session_state.selected_symptoms)}
Дата: {datetime.now().strftime('%d.%m.%Y %H:%M')}

ИСТОРИЯ СООБЩЕНИЙ:
==================

"""
    
    for i, message in enumerate(st.session_state.chat_history, 1):
        role_name = "ПОЛЬЗОВАТЕЛЬ" if message["role"] == "user" else "ВЕТЕРИНАР"
        export_text += f"{i}. {role_name}:\n{message['content']}\n\n"
    
    return export_text

def show_chat_actions():
    """Отображает дополнительные действия для чата."""
    
    if st.session_state.chat_history:
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📥 Экспорт чата"):
                chat_export = export_chat_history()
                st.download_button(
                    label="💾 Скачать историю",
                    data=chat_export,
                    file_name=f"vet_consultation_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                    mime="text/plain"
                )
        
        with col2:
            if st.button("🗑️ Очистить чат"):
                clear_chat_history()
                st.rerun()

