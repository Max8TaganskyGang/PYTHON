from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from deepface import DeepFace
import os

# Ваш токен Telegram Bot
TOKEN = "7815133819:AAH_v3RvL2Njy0TcoA6an_9wHO74wxqGbgM"


# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Привет! Отправь мне фото, и я постараюсь определить пол человека на нём.")


# Обработчик изображений
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    import traceback  # Для отладки ошибок
    photo = update.message.photo[-1]  # Получаем фото с максимальным разрешением
    file = await context.bot.get_file(photo.file_id)
    file_path = f"{photo.file_id}.jpg"
    await file.download_to_drive(file_path)

    try:
        # Анализ изображения
        analysis = DeepFace.analyze(img_path=file_path, actions=['gender'], enforce_detection=False)

        # Отладочный вывод результата
        print("Результат анализа:", analysis)

        # Извлечение информации о поле
        if 'gender' in analysis:
            gender_info = analysis['gender']
            if isinstance(gender_info, dict):
                predicted_gender = max(gender_info, key=gender_info.get)
                await update.message.reply_text(f"Пол определён: {predicted_gender}")
            else:
                await update.message.reply_text(f"Пол определён: {gender_info}")
        elif isinstance(analysis, list) and 'gender' in analysis[0]:
            # Если результат в списке
            gender_info = analysis[0]['gender']
            predicted_gender = max(gender_info, key=gender_info.get)
            await update.message.reply_text(f"Пол определён: {predicted_gender}")
        else:
            await update.message.reply_text("Не удалось найти информацию о поле. Попробуйте другое фото.")
    except Exception as e:
        # Логирование ошибок
        print("Ошибка анализа:")
        traceback.print_exc()
        await update.message.reply_text("Не удалось определить пол. Попробуйте другое фото.")
    finally:
        # Удаляем временный файл
        if os.path.exists(file_path):
            os.remove(file_path)


# Главная функция
def main():
    # Создаем приложение
    application = Application.builder().token(TOKEN).build()

    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    # Запускаем приложение
    application.run_polling()


if __name__ == '__main__':
    main()
