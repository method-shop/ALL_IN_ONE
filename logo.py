import telebot
import requests
import json
import os

#####    BY @ziddi_shop
#####    https://t.me/ziddi_shop

# Bot token setup
token = "7641333049:AAHRXsz0G9FqIykeqp-Se9llS4MN7ur7eDQ"
bot = telebot.TeleBot(token)

if not os.path.exists('images'):
    os.makedirs('images')

user_queries = {}

@bot.message_handler(commands=['start'])
def start(message):
    welcome_text = "Welcome! Enter a text to convert it to a logo (in English only).\nBY @ziddi_shop"

    keyboard = telebot.types.InlineKeyboardMarkup()
    button = telebot.types.InlineKeyboardButton(text="Bot Developer's Channel", url="https://t.me/ziddi_shop")
    keyboard.add(button)

    bot.send_message(message.chat.id, welcome_text, reply_markup=keyboard)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    text = message.text

    if chat_id in user_queries:
        try:
            number_of_logos = int(text)

            if number_of_logos > 0:
                query = user_queries[chat_id]
                bot.reply_to(message, f"Great! {number_of_logos} logos are being created using the text '{query}'. Please wait...")

                headers = {
                    'accept': '*/*',
                    'accept-language': 'en-US,en;q=0.9,ar;q=0.8',
                    'priority': 'u=1, i',
                    'referer': 'https://host-ali.serv00.net/logo/logo.html',
                    'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
                }

                params = {
                    'name': query,
                }

                response = requests.get('https://host-ali.serv00.net/logo/apilogo.php', params=params, headers=headers)

                if response.status_code == 200:
                    try:
                        data = json.loads(response.text)
                        links = [item['logo'] for item in data[:number_of_logos]]

                        for index, link in enumerate(links):
                            try:
                                img_response = requests.get(link)
                                img_response.raise_for_status()  # Raise exception if there is an error in image download
                                img_filename = f'images/image_{index + 1}.jpg'  # Name the image based on its order
                                with open(img_filename, 'wb') as img_file:
                                    img_file.write(img_response.content)

                                # Send the image to Telegram
                                with open(img_filename, 'rb') as img_file:
                                    bot.send_photo(chat_id, img_file)

                                print(f"Image downloaded and sent: {img_filename}")

                            except requests.RequestException as e:
                                print(f"Failed to download image from the link: {link}. Error: {e}")

                    except json.JSONDecodeError:
                        bot.reply_to(message, "Failed to decode JSON data.")
                else:
                    bot.reply_to(message, f"Failed to fetch data. Response code: {response.status_code}")

                del user_queries[chat_id]

            else:
                bot.reply_to(message, "The number must be greater than zero. Please try again.")
        except ValueError:
            bot.reply_to(message, "Please enter a valid integer.")
    else:
        user_queries[chat_id] = text
        bot.reply_to(message, "Thank you! Now, enter the number of logos you want.")

bot.polling()
