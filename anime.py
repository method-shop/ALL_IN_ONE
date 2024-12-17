from flask import Flask
from threading import Thread
import telebot
import requests
import json
import time

app = Flask(__name__)

bot = telebot.TeleBot('7641333049:AAHRXsz0G9FqIykeqp-Se9llS4MN7ur7eDQ')
#made By Nepcoder@ziddi_shop
CHANNEL_USERNAME = '@ziddi_shop'

def send_generated_image(chat_id, image_url, message_id=None):
    if message_id:
        bot.edit_message_media(chat_id, message_id, media=telebot.types.InputMediaPhoto(image_url))
    else:
        caption = "AnimePic generated by @ziddi_shop BOT"
        bot.send_photo(chat_id, photo=image_url, caption=caption)
#made By Nepcoder@ziddi_shop
@bot.inline_handler(lambda query: True)
def inline_join(query):
    join_channel_text = "Join @ziddi_shop Channel"
    join_button = telebot.types.InlineKeyboardButton(text=join_channel_text, url=f"https://t.me/{CHANNEL_USERNAME}")
    inline_keyboard = telebot.types.InlineKeyboardMarkup().add(join_button)
    bot.answer_inline_query(query.id, results=[telebot.types.InlineQueryResultArticle('1', 'Join Channel', telebot.types.InputTextMessageContent(join_channel_text), reply_markup=inline_keyboard)])

@bot.message_handler(commands=['start', 'help'])
def start(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    try:
        member_info = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        if member_info.status not in ['member', 'administrator', 'creator']:
            join_channel_text = "Join @ziddi_shop Channel to access commands and get updates."
            join_button = telebot.types.InlineKeyboardButton(text="Join Channel", url=f"https://t.me/{CHANNEL_USERNAME}")
            inline_keyboard = telebot.types.InlineKeyboardMarkup().add(join_button)
            bot.send_message(chat_id, join_channel_text, reply_markup=inline_keyboard)
            return
        welcome_msg = (
            f"Welcome to the Anime Pic Generator Bot, {message.from_user.first_name}!  \n\n"
            "To generate a new random anime picture, use the command:\n\n"
            "/animepic"
        )
        bot.send_message(chat_id, welcome_msg)
    except telebot.apihelper.ApiException as e:
        print(f"API Exception: {e}")
        bot.send_message(chat_id, "Error checking membership. Please try again later or contact the bot administrator.")
#made By Nepcoder@ziddi_shop
@bot.message_handler(commands=['animepic'])
def animepic(message):
    try:
        user_id = message.from_user.id
        member_info = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        if member_info.status not in ['member', 'administrator', 'creator']:
            join_channel_text = "You must join @ziddi_shop Channel to access the AnimePic command. Join now and try again."
            join_button = telebot.types.InlineKeyboardButton(text="Join Channel", url=f"https://t.me/ziddi_shop")
            inline_keyboard = telebot.types.InlineKeyboardMarkup().add(join_button)
            bot.send_message(message.chat.id, join_channel_text, reply_markup=inline_keyboard)
            return
        api_url = f"https://animepic.apinepdev.workers.dev/?join={CHANNEL_USERNAME}&timestamp={int(time.time())}"
        response = requests.get(api_url)
        data = json.loads(response.text)
        image_url = data["url"]
        print(f"Generated Image URL: {image_url}")
        send_generated_image(message.chat.id, image_url)
    except Exception as e:
        print(f"Error: {e}")
        bot.send_message(message.chat.id, "Error generating image. Please try again later.")

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

if __name__ == "__main__":
    keep_alive()
    bot.polling(none_stop=True)

