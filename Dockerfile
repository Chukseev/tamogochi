# Используем базовый образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY . /app

# Создаём виртуальное окружение
RUN python -m venv /app/venv

# Активируем виртуальное окружение и устанавливаем зависимости
RUN /app/venv/bin/pip install --no-cache-dir -r requirements.txt

# Указываем PATH к виртуальному окружению
ENV PATH="/app/venv/bin:$PATH"

# По умолчанию, если не переопределено, запускаем bash
CMD ["bash"]