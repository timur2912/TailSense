FROM langflowai/langflow:latest

# рабочая папка
WORKDIR /app

# создаём папки
RUN mkdir -p /app/flows
RUN mkdir -p /app/langflow-config-dir

# копируем только env файл
COPY docker.env /app/.env

# задаём переменные окружения
ENV LANGFLOW_LOAD_FLOWS_PATH=/app/flows
ENV LANGFLOW_CONFIG_DIR=/app/langflow-config-dir
# другие ENV можно задать через docker.env

# открываем порт
EXPOSE 7860

# запускаем LangFlow в режим только backend-API
CMD ["langflow", "run", "--env-file", "/app/.env", "--host", "0.0.0.0", "--port", "7860"]
