import telebot
from telebot.types import CallbackQuery
import requests
from io import BytesIO

# Replace 'YOUR_BOT_TOKEN' with your bot's token from @BotFather
BOT_TOKEN = "7641333049:AAHRXsz0G9FqIykeqp-Se9llS4MN7ur7eDQ"
bot = telebot.TeleBot(BOT_TOKEN)

# Callback query handler
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call: CallbackQuery):
    if call.data == "get_id":
        user = call.from_user
        user_id = user.id
        first_name = user.first_name
        last_name = user.last_name if user.last_name else ""
        username = f"@{user.username}" if user.username else "No username"
        
        # Create the Monopoly Style Message
        monopoly_style_message = f"""
        🏠 **Monopoly Profile Card** 🏠

        📛 **User ID**: {user_id}
        🏷️ **Name**: {first_name} {last_name}
        📝 **Username**: {username}
        
        💬 **Bio**: {user.bio if hasattr(user, 'bio') and user.bio else "No bio available."}
        
        🎲 *You are in the game of Telegram Monopoly!* 🎲
        """

        # Ensure the message is not empty
        if monopoly_style_message.strip():
            # Send the formatted Monopoly profile message
            bot.send_message(call.message.chat.id, monopoly_style_message)
        else:
            bot.send_message(call.message.chat.id, "Sorry, we couldn't fetch your profile data.")

        # Send profile picture (if available)
        try:
            profile_photos = bot.get_user_profile_photos(user_id, limit=1)
            if profile_photos.total_count > 0:
                # Fetch the profile picture URL
                file_id = profile_photos.photos[0][0].file_id
                file = bot.get_file(file_id)
                file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file.file_path}"
                
                # Send profile picture
                response = requests.get(file_url)
                img = BytesIO(response.content)
                img.name = f"profile_pic_{user_id}.jpg"
                bot.send_photo(call.message.chat.id, img)
            else:
                bot.send_message(call.message.chat.id, "No profile picture found.")
        except Exception as e:
            bot.send_message(call.message.chat.id, f"An error occurred while fetching the profile picture: {str(e)}")

# Polling
print("Bot is running...")
bot.polling(none_stop=True)
