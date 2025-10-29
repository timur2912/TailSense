"""
Компонент для выбора симптомов.
"""

import streamlit as st

def show_symptom_selector():
    """
    Отображает интерфейс выбора симптомов.
    
    Returns:
        list: Список выбранных симптомов
    """
    
    # Инициализация состояния если еще не было
    if 'selected_symptoms' not in st.session_state:
        st.session_state.selected_symptoms = []
    if 'custom_symptom' not in st.session_state:
        st.session_state.custom_symptom = ""
    
    # Список популярных симптомов по категориям
    symptom_categories = {
        "🌡️ Общее состояние": [
            "Повышенная температура",
            "Пониженная температура", 
            "Вялость, апатия",
            "Потеря аппетита",
            "Повышенная жажда"
        ],
        "🩺 Дыхательная система": [
            "Кашель",
            "Чихание",
            "Затрудненное дыхание",
            "Хрипы",
            "Выделения из носа"
        ],
        "🍽️ Пищеварение": [
            "Рвота",
            "Диарея",
            "Запор",
            "Отказ от еды",
            "Повышенный аппетит"
        ],
        "👁️ Внешние признаки": [
            "Выделения из глаз",
            "Слезотечение",
            "Зуд, расчесы",
            "Выпадение шерсти",
            "Изменение цвета слизистых"
        ],
        "🏃 Поведение": [
            "Беспокойство",
            "Агрессивность",
            "Хромота",
            "Дрожь",
            "Скрытность"
        ]
    }
    
    # Получаем текущие выбранные симптомы из session_state
    current_symptoms = st.session_state.selected_symptoms.copy()
    
    # Отображаем симптомы по категориям
    for category, symptoms in symptom_categories.items():
        with st.expander(category, expanded=True):
            for symptom in symptoms:
                # Проверяем, выбран ли симптом
                is_selected = symptom in current_symptoms
                
                if st.checkbox(symptom, 
                              value=is_selected, 
                              key=f"symptom_checkbox_{symptom}"):
                    # Добавляем симптом если его еще нет
                    if symptom not in current_symptoms:
                        current_symptoms.append(symptom)
                else:
                    # Удаляем симптом если он был убран
                    if symptom in current_symptoms:
                        current_symptoms.remove(symptom)
    
    st.markdown("---")
    
    # Поле для ввода собственного симптома
    st.markdown("**Добавить собственный симптом:**")
    custom_symptom = st.text_input(
        "Опишите симптом",
        placeholder="Например: странные звуки, необычное поведение...",
        key="custom_symptom_input",
        value=st.session_state.custom_symptom
    )
    
    # Обрабатываем собственный симптом
    if custom_symptom.strip():
        custom_clean = custom_symptom.strip()
        # Добавляем собственный симптом если его еще нет
        if custom_clean not in current_symptoms and custom_clean != st.session_state.custom_symptom:
            current_symptoms.append(custom_clean)
        st.session_state.custom_symptom = custom_clean
    elif st.session_state.custom_symptom and st.session_state.custom_symptom in current_symptoms:
        # Удаляем собственный симптом если поле очищено
        current_symptoms.remove(st.session_state.custom_symptom)
        st.session_state.custom_symptom = ""
    
    # Обновляем session_state
    st.session_state.selected_symptoms = current_symptoms
    
    # Показываем выбранные симптомы
    if current_symptoms:
        st.markdown("### ✅ Выбранные симптомы:")
        for i, symptom in enumerate(current_symptoms, 1):
            st.markdown(f"{i}. {symptom}")
    else:
        st.info("Выберите симптомы из списка выше или добавьте собственный")
    
    return current_symptoms

def show_symptom_summary(symptoms):
    """
    Отображает сводку выбранных симптомов.
    
    Args:
        symptoms (list): Список симптомов
    """
    if not symptoms:
        st.warning("Симптомы не выбраны")
        return
    
    st.markdown("### 🩺 Выбранные симптомы:")
    
    # Группируем симптомы для лучшего отображения
    symptom_text = ", ".join(symptoms)
    
    st.info(f"**Всего симптомов:** {len(symptoms)}")
    st.markdown(f"**Список:** {symptom_text}")

def get_symptom_severity_color(symptom):
    """
    Определяет цвет для симптома на основе его потенциальной серьезности.
    
    Args:
        symptom (str): Название симптома
        
    Returns:
        str: CSS цвет
    """
    # Критические симптомы
    critical_symptoms = [
        "затрудненное дыхание", "высокая температура", "судороги", 
        "потеря сознания", "кровотечение"
    ]
    
    # Серьезные симптомы
    serious_symptoms = [
        "рвота", "диарея", "отказ от еды", "вялость", "хромота"
    ]
    
    symptom_lower = symptom.lower()
    
    if any(critical in symptom_lower for critical in critical_symptoms):
        return "#ff4444"  # Красный
    elif any(serious in symptom_lower for serious in serious_symptoms):
        return "#ff9900"  # Оранжевый
    else:
        return "#4CAF50"  # Зеленый
