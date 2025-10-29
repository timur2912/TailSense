"""
Компонент для выбора животного.
"""

import streamlit as st

def show_animal_selector():
    """
    Отображает интерфейс выбора животного.
    
    Returns:
        str: Название выбранного животного или пустая строка
    """
    
    # Инициализация состояния если еще не было
    if 'selected_animal' not in st.session_state:
        st.session_state.selected_animal = ""
    
    # Список популярных животных
    popular_animals = [
        ("🐕", "Собака"),
        ("🐱", "Кошка"),
        ("🐦", "Птица"),
        ("🐰", "Кролик"),
        ("🐄", "КРС (корова/бык)"),
        ("🐴", "Лошадь")
    ]
    
    st.markdown("**Выберите из популярных животных:**")
    
    # Создаем сетку кнопок для животных
    cols = st.columns(3)
    
    for i, (emoji, animal_name) in enumerate(popular_animals):
        col = cols[i % 3]
        with col:
            # Подсвечиваем выбранное животное
            button_type = "primary" if st.session_state.selected_animal == animal_name else "secondary"
            if st.button(f"{emoji} {animal_name}", 
                        key=f"animal_{i}", 
                        use_container_width=True, 
                        type=button_type):
                st.session_state.selected_animal = animal_name
                st.rerun()
    
    st.markdown("---")
    
    # Поле для ввода собственного животного
    st.markdown("**Или введите своё животное:**")
    custom_animal = st.text_input(
        "Название животного",
        placeholder="Например: хомяк, игуана, коза...",
        key="custom_animal_input",
        value=st.session_state.selected_animal if st.session_state.selected_animal not in [animal[1] for animal in popular_animals] else ""
    )
    
    # Если введено собственное животное, сохраняем его
    if custom_animal.strip() and custom_animal.strip() != st.session_state.selected_animal:
        st.session_state.selected_animal = custom_animal.strip()
    
    return st.session_state.selected_animal

def show_animal_card(animal_name):
    """
    Отображает карточку выбранного животного.
    
    Args:
        animal_name (str): Название животного
    """
    if not animal_name:
        return
        
    # Определяем эмодзи для животного
    animal_emoji_map = {
        "собака": "🐕",
        "кошка": "🐱",
        "птица": "🐦",
        "кролик": "🐰",
        "крс (корова/бык)": "🐄",
        "корова": "🐄",
        "бык": "🐄",
        "лошадь": "🐴"
    }
    
    emoji = animal_emoji_map.get(animal_name.lower(), "🐾")
    
    # Карточка животного
    with st.container():
        st.markdown(f"""
        <div style="
            padding: 20px;
            border-radius: 10px;
            border: 2px solid #e0e0e0;
            background-color: #f8f9fa;
            text-align: center;
        ">
            <h2>{emoji}</h2>
            <h3>{animal_name}</h3>
        </div>
        """, unsafe_allow_html=True)
