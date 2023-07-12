import openai
import telebot
import time
from threading import Thread

from math_bot_settings import API_SECRET_KEY, FEED_MY_BABY_TOKEN

openai.api_key = API_SECRET_KEY
bot = telebot.TeleBot(FEED_MY_BABY_TOKEN)
bot.set_webhook()


class ChatApp:
    def __init__(self):
        self.messages = [
            {"role": "system", "content": """Task: You're a cool teacher explaining the Pythagorean theorem to school kids using friendly slang.
                                1.explain the theory of Pythagorean theorem;
                                2.ensure if the student understood it;
                                3.test his knowledge with task he need to solve.
                                1 unit = 1 centimeter = 10 millimeters = 0.01 meter"""},
        ]
        self.user_id = 0

    def chat(self, message):
        self.messages.append({"role": "user", "content": message})
        response = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages = self.messages,
            max_tokens = 1024
        )
        self.messages.append({"role": "assistant", "content": response["choices"][0]["message"]["content"]})
        return response["choices"][0]["message"]["content"]

class Remainder:
    def __init__(self):
        self.start = time.time()
        self.user_id =0

    def check_chat(self, checkpoint):
        if float(checkpoint) - float(self.start) > 180:
            print ('Time to wake up!')
            bot.send_message(self.user_id, 'Buy an elephant!🐘🐘🐘')
            self.start = time.time()

@bot.message_handler(commands = ['start', 'hello'])
def send_start(message):
    bot_chat.user_id = message.from_user.id
    chat_remainder.user_id = message.from_user.id
    text = """👋 Hello! Let's learn the Pythagorean theorem! Let's do it right now! Are u ready?"""""
    bot.send_message(message.from_user.id, text)

def waking_up():
    while True:
        chat_remainder.check_chat(float(time.time()))
        time.sleep(60)

@bot.message_handler(func=lambda message: True, content_types=["text"])
def send_msg_to_chatgpt(message):
    #print (bot_chat.messages)
    answer = bot_chat.chat(message.text)
    bot.send_message(message.from_user.id, answer)
    chat_remainder.start = time.time()

if __name__ == "__main__":
    bot_chat = ChatApp()
    chat_remainder= Remainder()

    t = Thread(target=waking_up)
    t.start()

    bot.infinity_polling()
