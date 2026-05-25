import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup
import re

# Токен бота
TOKEN = "8798099753:AAEPS5NrlwGHyQI-ftPdK4tozQDlK1mLDR8"
bot = telebot.TeleBot(TOKEN)

# Словарь для хранения состояний пользователей
user_states = {}

def convert_decimal_to_binary_web(decimal_number):
    """
    Парсинг сайта для конвертации десятичного числа в двоичное
    Используем сайт rapidtables.com
    """
    try:
        # URL для конвертации
        url = f"https://www.rapidtables.com/convert/number/decimal-to-binary.html?x={decimal_number}"
        
        # Отправляем GET запрос
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            # Парсим HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Ищем результат конвертации
            # На сайте результат находится в элементе с id="result"
            result_element = soup.find('input', {'id': 'y'})
            
            if result_element and result_element.get('value'):
                binary_result = result_element.get('value')
                return binary_result.strip()
            else:
                # Альтернативный поиск
                result_div = soup.find('div', class_='result')
                if result_div:
                    binary_text = result_div.get_text()
                    # Извлекаем двоичное число
                    match = re.search(r'[01]+', binary_text)
                    if match:
                        return match.group()
        
        return None
        
    except Exception as e:
        print(f"Ошибка при парсинге: {e}")
        return None

def convert_decimal_to_binary_local(decimal_number):
    try:
        num = int(decimal_number)
        if num == 0:
            return "0"
        
        binary = ""
        while num > 0:
            binary = str(num % 2) + binary
            num //= 2
        return binary
    except:
        return None

@bot.message_handler(commands=['start'])
def send_welcome(message):
    """
    Обработчик команды /start
    """
    user_name = message.from_user.first_name
    welcome_text = f"Привет, {user_name}!\n\n"
    welcome_text += "Я бот-конвертер десятичных чисел в двоичный код.\n"
    welcome_text += "Используй /help для получения дополнительной информации."
    
    # Создаем клавиатуру с кнопками
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_help = types.KeyboardButton('/help')
    btn_example = types.KeyboardButton('Пример')
    markup.add(btn_help, btn_example)
    
    bot.reply_to(message, welcome_text, reply_markup=markup)

@bot.message_handler(commands=['help'])
def send_help(message):
    """
    Обработчик команды /help
    """
    user_name = message.from_user.first_name
    help_text = f"Справка для {user_name}:\n\n"
    help_text += "Я конвертирую десятичные числа в двоичный код\n\n"
    help_text += "Доступные команды:\n"
    help_text += "/start - Начать работу с ботом\n"
    help_text += "/help - Показать эту справку\n"
    help_text += "/convert - Конвертировать число\n\n"
    help_text += "Как использовать:\n"
    help_text += "1. Отправь десятичное число\n"
    help_text += "2. Используй кнопку 'Конвертировать'\n"
    help_text += "3. Введи число после команды /convert\n\n"
    help_text += "Пример: отправь '42' и получишь '101010'\n\n"
    
    # Создаем inline клавиатуру
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_convert = types.InlineKeyboardButton('Конвертировать', callback_data='convert')
    btn_example = types.InlineKeyboardButton('Пример', callback_data='example')
    markup.add(btn_convert, btn_example)
    
    bot.reply_to(message, help_text, reply_markup=markup)

@bot.message_handler(commands=['convert'])
def convert_command(message):
    """
    Обработчик команды /convert
    """
    user_name = message.from_user.first_name
    msg = bot.reply_to(message, f"{user_name}, введите десятичное число для конвертации:")
    bot.register_next_step_handler(msg, process_convert_step)

def process_convert_step(message):
    """
    Обработка ввода числа
    """
    try:
        number = message.text.strip()
        
        # Проверяем, что введено число
        if not number.isdigit():
            bot.reply_to(message, "Пожалуйста, введите целое положительное число!")
            return
        
        # Отправляем сообщение о процессе конвертации
        processing_msg = bot.reply_to(message, "Выполняю конвертацию...")
        
        # Пробуем конвертировать через веб-сайт
        binary_result = convert_decimal_to_binary_web(number)
        
        if binary_result is None:
            binary_result = convert_decimal_to_binary_local(number)
        
        if binary_result is not None:
            # Формируем ответ
            result_text = f"Результат конвертации:\n\n"
            result_text += f"Десятичное число: {number}\n"
            result_text += f"Двоичный код: {binary_result}\n\n"
            result_text += "Хотите конвертировать еще? Отправьте новое число!"
            
            bot.edit_message_text(
                chat_id=processing_msg.chat.id,
                message_id=processing_msg.message_id,
                text=result_text
            )
        else:
            bot.edit_message_text(
                chat_id=processing_msg.chat.id,
                message_id=processing_msg.message_id,
                text="Не удалось выполнить конвертацию. Попробуйте другое число."
            )
            
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {str(e)}")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    """
    Обработчик inline кнопок
    """
    if call.data == 'convert':
        bot.answer_callback_query(call.id)
        msg = bot.send_message(call.message.chat.id, "Введите десятичное число:")
        bot.register_next_step_handler(msg, process_convert_step)
    
    elif call.data == 'example':
        bot.answer_callback_query(call.id)
        example_text = "Примеры конвертации:\n\n"
        example_text += "10 → 1010\n"
        example_text += "42 → 101010\n"
        example_text += "255 → 11111111\n"
        example_text += "100 → 1100100\n\n"
        example_text += "Отправьте свое число для конвертации!"
        bot.send_message(call.message.chat.id, example_text)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    """
    Обработчик текстовых сообщений
    """
    text = message.text.strip()
    user_name = message.from_user.first_name
    
    # Обработка кнопок
    if text == '/help':
        send_help(message)
    elif text == 'Пример':
        example_text = "Примеры конвертации:\n\n"
        example_text += "10 → 1010\n"
        example_text += "42 → 101010\n"
        example_text += "255 → 11111111\n"
        example_text += "100 → 1100100\n\n"
        example_text += "Отправьте свое число для конвертации!"
        bot.reply_to(message, example_text)
    else:
        # Проверяем, является ли текст числом
        if text.isdigit():
            # Автоматически конвертируем число
            process_convert_step(message)
        else:
            bot.reply_to(message, f"{user_name}, я понимаю только числа или команды.\n"
                                f"Отправьте число для конвертации или используйте /help")

# Запуск бота
if __name__ == "__main__":
    print("Бот запущен...")
    bot.infinity_polling()