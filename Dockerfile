# Используем официальное slim-изображение Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Устанавливаем необходимые пакеты
RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx libglib2.0-0 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Копируем файл зависимостей в контейнер
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем пакет tf-keras
RUN pip install tf-keras

# Копируем весь код вашего проекта в контейнер
COPY . .

# Указываем команду по умолчанию для запуска приложения
CMD ["python", "main.py"]


