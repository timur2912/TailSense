# Используем официальный образ Python 3.10 slim для уменьшения размера
FROM python:3.10-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файл requirements.txt для установки зависимостей
COPY requirements.txt .

# Устанавливаем системные зависимости (curl для healthcheck)
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем все файлы приложения в контейнер
COPY . .

# Создаем непривилегированного пользователя для запуска приложения
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app
USER app

# Экспонируем порт 8501 (стандартный порт Streamlit)
EXPOSE 8501

# Проверка здоровья контейнера
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Команда запуска Streamlit приложения
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true", "--server.fileWatcherType=polling", "--browser.gatherUsageStats=false"]
