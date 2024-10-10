import telebot
from googletrans import Translator  # Используем Google Translate для более точного перевода
import os
from together import Together
import base64

# Токен вашего Телеграм-бота
TELEGRAM_TOKEN = "7737309294:AAEgcT3WpfvwCDSnioca7h5SyCn96wT-UL8"

# API-ключ для сайта генерации изображений
TOGETHER_API_KEY = "c3a5a9e3be41ece304da897df43050b45b7d7a22819475bdaf6ad0b6e23f24a9"

# Инициализация клиентов
bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = Together(api_key=TOGETHER_API_KEY)
translator = Translator()

# Обработчик для получения текстовых сообщений
@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_text(message):
    # Перевод текста на английский с помощью Google Translate
    translated = translator.translate(message.text, src='ru', dest='en')
    prompt_in_english = translated.text

    # Отправка запроса на сайт для генерации изображения с улучшенными параметрами
    response = client.images.generate(
        prompt=prompt_in_english,
        model="black-forest-labs/FLUX.1-schnell",
        width=1024,
        height=768,
        steps=10,  # Увеличим количество шагов для повышения качества
        n=1,
        response_format="b64_json"
    )

    # Получение изображения из ответа
    image_data = response.data[0].b64_json
    
    # Декодирование изображения из base64
    image_bytes = base64.b64decode(image_data)
    
    # Сохранение изображения во временный файл
    image_filename = "generated_image.png"
    with open(image_filename, "wb") as img_file:
        img_file.write(image_bytes)

    # Отправка изображения обратно пользователю
    with open(image_filename, "rb") as img:
        bot.send_photo(message.chat.id, img)

# Запуск бота
bot.polling()
