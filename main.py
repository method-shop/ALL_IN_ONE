import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import subprocess  # To run the external Python scripts

# Replace 'YOUR_BOT_TOKEN' with your bot's token from @BotFather
BOT_TOKEN = "YOUR_BOT_TOKEN"
bot = telebot.TeleBot(BOT_TOKEN)

# Start command handler
@bot.message_handler(commands=['start'])
def start_handler(message):
    chat_id = message.chat.id
    # Welcome message
    welcome_text = f"Welcome to the bot, {message.from_user.first_name}! Choose an option below:"
    
    # Inline keyboard with multiple buttons
    markup = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton("ID", callback_data="get_id"),
        InlineKeyboardButton("CC GEN", callback_data="cc_gen"),
        InlineKeyboardButton("MUSIC", callback_data="music"),
        InlineKeyboardButton("IMAGE GENERATE", callback_data="image_generate"),
        InlineKeyboardButton("GPT", callback_data="gpt"),
    ]
    markup.add(*buttons)  # Add buttons to the markup
    
    # Send welcome message with inline buttons
    bot.send_message(chat_id, welcome_text, reply_markup=markup)

# Callback query handler
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call: CallbackQuery):
    try:
        if call.data == "get_id":
            # Run get_id.py script
            result = subprocess.run(['python', 'get_id.py'], capture_output=True, text=True)
            bot.send_message(call.message.chat.id, result.stdout)  # Send the output of the script
            
        elif call.data == "cc_gen":
            # Run cc_gen.py script
            result = subprocess.run(['python', 'cc_gen.py'], capture_output=True, text=True)
            bot.send_message(call.message.chat.id, result.stdout)  # Send the output of the script
            
        elif call.data == "music":
            # Run music.py script
            result = subprocess.run(['python', 'music.py'], capture_output=True, text=True)
            bot.send_message(call.message.chat.id, result.stdout)  # Send the output of the script
            
        elif call.data == "image_generate":
            # Run image_generate.py script
            result = subprocess.run(['python', 'image_generate.py'], capture_output=True, text=True)
            bot.send_message(call.message.chat.id, result.stdout)  # Send the output of the script
            
        elif call.data == "gpt":
            # Run gpt.py script
            result = subprocess.run(['python', 'gpt.py'], capture_output=True, text=True)
            bot.send_message(call.message.chat.id, result.stdout)  # Send the output of the script
            
        else:
            bot.send_message(call.message.chat.id, "Unknown command. Please try again!")

    except Exception as e:
        bot.send_message(call.message.chat.id, f"An error occurred: {str(e)}")

# Polling
print("Bot is running...")
bot.polling()
