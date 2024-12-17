import telebot
import random
from randomtimestamp import randomtimestamp
from datetime import datetime

# Replace 'YOUR_BOT_TOKEN' with your bot's token from @BotFather
BOT_TOKEN = "7641333049:AAHRXsz0G9FqIykeqp-Se9llS4MN7ur7eDQ"
bot = telebot.TeleBot(BOT_TOKEN)

# Utility function to check if a parameter is an integer
def check_integer(params):
    try:
        int(params)
        return True
    except ValueError:
        return False

# Credit Card Generation Logic
class CC():
    CCDATA = {
        'amex': {'len_num': 15, 'len_cvv': 4, 'pre': [34, 37], 'remaining': 13},
        'discover': {'len_num': 16, 'len_cvv': 3, 'pre': [6001], 'remaining': 12},
        'mc': {'len_num': 16, 'len_cvv': 3, 'pre': [51, 55], 'remaining': 14},
        'visa13': {'len_num': 13, 'len_cvv': 3, 'pre': [4], 'remaining': 12},
        'visa16': {'len_num': 16, 'len_cvv': 3, 'pre': [4], 'remaining': 15},
    }

    def __init__(self):
        self.cc_type = None
        self.cc_len = None
        self.cc_num = None
        self.cc_cvv = None
        self.cc_exp = None
        self.cc_prefill = []

    def generate_cc_exp(self):
        self.cc_exp = randomtimestamp(start_year=datetime.now().year + 1, text=True, end_year=datetime.now().year + 3, pattern="%m-%Y")
    
    def generate_cc_cvv(self):
        length = self.CCDATA[self.cc_type]['len_cvv']
        self.cc_cvv = ''.join([str(random.randint(0, 9)) for _ in range(length)])

    def generate_cc_prefill(self):
        self.cc_prefill = random.choices(self.CCDATA[self.cc_type]['pre'])

    def generate_cc_num(self):
        remaining = self.CCDATA[self.cc_type]['remaining']
        working = self.cc_prefill + [random.randint(1, 9) for _ in range(remaining - 1)]
        check_offset = (len(working) + 1) % 2
        check_sum = 0
        for i, n in enumerate(working):
            if (i + check_offset) % 2 == 0:
                n_ = n * 2
                check_sum += n_ - 9 if n_ > 9 else n_
            else:
                check_sum += n
        self.cc_num = "".join(map(str, working + [10 - (check_sum % 10)]))

    def return_new_card(self):
        return {'cc_type': self.cc_type, 'cc_num': self.cc_num, 'cc_cvv': self.cc_cvv, 'cc_exp': self.cc_exp}

    def print_new_card(self):
        print(f'Type: {self.cc_type}\nNumber: {self.cc_num}\nCVV: {self.cc_cvv}\nExp: {self.cc_exp}\n{"-"*32}')


class CCNumGen():
    card_types = ['amex', 'discover', 'mc', 'visa13', 'visa16']

    def __init__(self, type='visa16', number=1):
        self.type = type
        self.num = number
        self.card_list = []
        if self.type not in self.card_types:
            print('Card type not recognized. Task ended.')
            return
        if not isinstance(self.num, int):
            print('Number of cards must be a whole number. Task ended.')
            return
        self.generate_cards()

    def generate_cards(self):
        for _ in range(self.num):
            new = CC()
            new.cc_type = self.type
            new.generate_cc_exp()
            new.generate_cc_cvv()
            new.generate_cc_prefill()
            new.generate_cc_num()
            self.card_list.append(new.return_new_card())
            new.print_new_card()

    def print_card_list(self):
        for card in self.card_list:
            print('------------------------------')
            for k, v in card.items():
                print(f'{k}: {v}')


# CC generation command handler
@bot.message_handler(commands=['cc_gen'])
def cc_gen_handler(message):
    chat_id = message.chat.id
    params = message.text.split()[1:]  # Extract parameters after the command
    
    if params:
        params = params[0]  # Assume the first parameter is the quantity
        if check_integer(params):
            quantity = int(params)
            if quantity <= 100:
                # Generate the cards using the CCNumGen class
                cc_gen = CCNumGen('visa16', quantity)  # You can change the card type as needed
                card_details = "\n".join([f"Type: {card['cc_type']}, Number: {card['cc_num']}, CVV: {card['cc_cvv']}, Exp: {card['cc_exp']}" for card in cc_gen.card_list])
                bot.send_message(chat_id, card_details)
            else:
                bot.send_message(chat_id, "You can only generate up to 100 cards.")
        else:
            bot.send_message(chat_id, "Only numbers are allowed.\n\nUse: `/cc_gen <number>`", parse_mode="Markdown")
    else:
        bot.send_message(chat_id, "Please provide a quantity.\n\nExample: `/cc_gen 30`", parse_mode="Markdown")

# Polling
print("Bot is running...")
bot.polling(none_stop=True)
