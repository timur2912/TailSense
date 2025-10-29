"""
API клиент для взаимодействия с ИИ-агентом ветеринар-помощника.
"""

import requests
import uuid
import time
from typing import List, Dict, Any
import streamlit as st

# Конфигурация API агента
import os

# Определяем URL агента в зависимости от окружения
AGENT_HOST = os.getenv("AGENT_HOST", "agent")  # agent - имя сервиса в docker-compose
AGENT_PORT = os.getenv("AGENT_PORT", "7860")

AGENT_API_CONFIG = {
    "url": f"http://{AGENT_HOST}:{AGENT_PORT}/api/v1/run/e68ff0eb-0690-43b7-acb6-c3e8ea8ecea1",
    "api_key": "sk-WFRz8a28DHL31Sr-qN0K8WFFnzKeeVaJJLq5RYAF7dg",
    "headers": {
        "Content-Type": "application/json",
        "x-api-key": "sk-WFRz8a28DHL31Sr-qN0K8WFFnzKeeVaJJLq5RYAF7dg"
    },
    "timeout": 60  # Таймаут в секундах
}

def send_message(animal: str, symptoms: List[str], message: str, history: List[Dict[str, Any]]) -> str:
    """
    Отправляет сообщение пользователя в ИИ-агент и получает ответ от ветеринара.
    
    Args:
        animal (str): Тип животного
        symptoms (List[str]): Список симптомов
        message (str): Сообщение пользователя
        history (List[Dict[str, Any]]): История чата
    
    Returns:
        str: Ответ от ИИ-ветеринара
    """
    
    # Формируем контекстное сообщение с информацией о животном и симптомах
    context_message = _build_context_message(animal, symptoms, message, history)
    
    try:
        # Отправляем запрос к ИИ-агенту
        response_text = _call_agent_api(context_message)
        return response_text
        
    except Exception as e:
        st.error(f"Ошибка при обращении к ИИ-агенту: {str(e)}")
        # Возвращаем заглушку в случае ошибки
        return _get_fallback_response(animal, symptoms, message)

def generate_mock_responses(animal: str, symptoms: List[str], message: str, history: List[Dict[str, Any]]) -> List[str]:
    """
    Генерирует набор заглушечных ответов в зависимости от контекста.
    
    Args:
        animal (str): Тип животного
        symptoms (List[str]): Список симптомов
        message (str): Сообщение пользователя
        history (List[Dict[str, Any]]): История чата
    
    Returns:
        List[str]: Список возможных ответов
    """
    
    # Базовые заглушки
    base_responses = [
        "Это заглушка-ответ от ИИ-ветеринара.",
        f"Понимаю вашу обеспокоенность по поводу {animal.lower()}. Это временный ответ-заглушка.",
        "Спасибо за подробное описание. Сейчас здесь заглушка, но скоро будет реальный ИИ-анализ."
    ]
    
    # Ответы в зависимости от симптомов
    if symptoms:
        symptom_responses = [
            f"Учитывая указанные симптомы ({', '.join(symptoms[:2])}{', и другие' if len(symptoms) > 2 else ''}), рекомендую следующее: [заглушка]",
            f"Симптомы, которые вы описали, могут указывать на несколько возможных причин. [Это заглушка - здесь будет реальный анализ]",
            "На основе симптомов могу предположить... [заглушка для будущего ИИ-анализа]"
        ]
        base_responses.extend(symptom_responses)
    
    # Ответы в зависимости от типа животного
    animal_specific = {
        "собака": [
            "У собак такие симптомы часто связаны с... [заглушка]",
            "Для собак в таких случаях обычно рекомендуется... [временная заглушка]"
        ],
        "кошка": [
            "Кошки склонны к... [заглушка - здесь будет экспертный анализ]",
            "У кошек это может быть признаком... [временный ответ]"
        ]
    }
    
    if animal.lower() in animal_specific:
        base_responses.extend(animal_specific[animal.lower()])
    
    # Ответы в зависимости от содержания сообщения
    message_lower = message.lower()
    
    if any(word in message_lower for word in ['когда', 'как долго', 'сколько']):
        base_responses.append("Относительно времени... [заглушка для временного анализа]")
    
    if any(word in message_lower for word in ['серьезно', 'опасно', 'срочно']):
        base_responses.append("⚠️ Если ситуация кажется серьезной, рекомендую немедленно обратиться к ветеринару. [Это заглушка, но совет актуален]")
    
    if 'лечение' in message_lower or 'что делать' in message_lower:
        base_responses.append("Рекомендуемые действия: [здесь будет персонализированный план лечения] - пока заглушка")
    
    return base_responses

def check_backend_connection() -> bool:
    """
    Проверяет доступность ИИ-агента.
    
    Returns:
        bool: True если агент доступен, False если нет
    """
    
    try:
        # Пробуем отправить простой тестовый запрос
        test_payload = {
            "output_type": "chat",
            "input_type": "chat",
            "input_value": "Тестовое соединение",
            "session_id": str(uuid.uuid4())
        }
        
        response = requests.post(
            AGENT_API_CONFIG["url"],
            json=test_payload,
            headers=AGENT_API_CONFIG["headers"],
            timeout=10  # Короткий таймаут для проверки
        )
        
        return response.status_code == 200
        
    except Exception:
        return False

def get_api_status() -> Dict[str, Any]:
    """
    Получает статус API агента.
    
    Returns:
        Dict[str, Any]: Информация о статусе API
    """
    
    is_connected = check_backend_connection()
    
    return {
        "status": "connected" if is_connected else "disconnected",
        "message": "ИИ-агент доступен" if is_connected else "ИИ-агент недоступен",
        "agent_connected": is_connected,
        "agent_url": AGENT_API_CONFIG["url"],
        "version": "1.0.0-agent"
    }

def _build_context_message(animal: str, symptoms: List[str], message: str, history: List[Dict[str, Any]]) -> str:
    """
    Формирует контекстное сообщение для ИИ-агента.
    
    Args:
        animal (str): Тип животного
        symptoms (List[str]): Список симптомов
        message (str): Сообщение пользователя
        history (List[Dict[str, Any]]): История чата
    
    Returns:
        str: Сформированное контекстное сообщение
    """
    
    # Формируем контекст с информацией о животном и симптомах
    context_parts = []
    
    if animal:
        context_parts.append(f"Животное: {animal}")
    
    if symptoms:
        symptoms_text = ", ".join(symptoms)
        context_parts.append(f"Наблюдаемые симптомы: {symptoms_text}")
    
    # Добавляем историю чата (последние несколько сообщений)
    if history:
        recent_history = history[-4:]  # Берем последние 4 сообщения для контекста
        context_parts.append("Предыдущие сообщения:")
        for msg in recent_history:
            role = "Пользователь" if msg["role"] == "user" else "Ветеринар"
            context_parts.append(f"{role}: {msg['content']}")
    
    # Добавляем текущий вопрос
    context_parts.append(f"Текущий вопрос: {message}")
    
    return "\n".join(context_parts)

def _call_agent_api(message: str) -> str:
    """
    Выполняет запрос к API ИИ-агента.
    
    Args:
        message (str): Сообщение для отправки агенту
    
    Returns:
        str: Ответ от агента
    
    Raises:
        requests.RequestException: Ошибка при выполнении запроса
        ValueError: Ошибка при парсинге ответа
    """
    
    # Получаем или создаем постоянный session_id для пользователя
    if 'agent_session_id' not in st.session_state:
        st.session_state.agent_session_id = str(uuid.uuid4())
    
    # Подготавливаем payload для API запроса
    payload = {
        "output_type": "chat",
        "input_type": "chat", 
        "input_value": message,
        "session_id": st.session_state.agent_session_id
    }
    
    # Выполняем запрос к API
    response = requests.post(
        AGENT_API_CONFIG["url"],
        json=payload,
        headers=AGENT_API_CONFIG["headers"],
        timeout=AGENT_API_CONFIG["timeout"]
    )
    
    # Проверяем статус ответа
    response.raise_for_status()
    
    # Парсим JSON ответа
    resp_json = response.json()
    
    # Извлекаем текст ответа из структуры API
    try:
        answer_text = resp_json["outputs"][0]["outputs"][0]["results"]["message"]["data"]["text"]
        return answer_text
    except (KeyError, IndexError) as e:
        raise ValueError(f"Неожиданная структура ответа API: {e}")

def _get_fallback_response(animal: str, symptoms: List[str], message: str) -> str:
    """
    Возвращает заглушку-ответ в случае ошибки API.
    
    Args:
        animal (str): Тип животного
        symptoms (List[str]): Список симптомов
        message (str): Сообщение пользователя
    
    Returns:
        str: Заглушка-ответ
    """
    
    fallback_responses = [
        f"Извините, временно не могу обработать ваш запрос о {animal.lower()}. Пожалуйста, попробуйте позже.",
        "Произошла ошибка подключения к ИИ-ветеринару. Попробуйте перезагрузить страницу или обратитесь позже.",
        f"К сожалению, не удается получить консультацию по симптомам: {', '.join(symptoms[:3])}. Рекомендую обратиться к ветеринару напрямую."
    ]
    
    return fallback_responses[0]

def reset_agent_session():
    """
    Сбрасывает сессию агента, создавая новый session_id.
    Используется при начале новой консультации.
    """
    if 'agent_session_id' in st.session_state:
        del st.session_state.agent_session_id

