#bot = ('5879800806:AAF61W_F76vbTR3SFa6_59syolJUPgf6Rhg')

import telebot
import openai
# admin_id = 5214644649
# openai.api_key = "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"
# api = '5879800806:AAF61W_F76vbTR3SFa6_59syolJUPgf6Rhg'


openai.api_key = "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"
api = '5879800806:AAF61W_F76vb3SFa6_59syolJUPgf6Rhg'
bot = telebot.TeleBot(api)


chatting_users = {}
channel_id = -1001753652819 # replace this with your channel ID

def rsp(question, engine):
    try:
        prompt = "Q: {qst}\nA:".format(qst=question)
        response = openai.Completion.create(
            engine=engine,
            prompt=prompt,
            max_tokens=500,
            n=1,
            stop=None,
            temperature=0.4,
        )
        return response.choices[0].text
    except Exception as e:
        return "Oopsie-daisy! It looks like I'm a bit tied up right now and can't answer your request. But don't worry, I'll get back to you soon!\nSend /start after a while...or \ncontact: @gladson1"


def check_user_in_channel(user_id):
    try:
        member = bot.get_chat_member(channel_id, user_id)
        return member.status != 'left'
    except Exception as e:
        print(e)
        return False


@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.chat.id
    if user_id not in chatting_users:
        bot.send_message(user_id, f"#Hello! Your ID is: {user_id}")
        chatting_users[user_id] = True
    bot.send_message(user_id, 'Hello, Welcome to OMG bot. \nAsk me whatever you want & get cool answer. \nPowered by [Gemechis](https://t.me/gladson1)', parse_mode='Markdown')


@bot.message_handler(commands=['developer'])
def send_developer(message):
    text = "I'm *Gemechis Chala*, the developer of this bot. \nYou can find me on telegram [@gladson1](https://t.me/gladson1).\n\nYou can also check out my channel [MAALGAARIIN](https://t.me/maalgaariin) for more information about my projects."
    bot.send_message(message.chat.id, text, parse_mode='Markdown')


@bot.message_handler(commands=['stop'])
def stop_chatting(message):
    user_id = message.chat.id
    if user_id != 5214644649: # replace this with your user ID
        bot.send_message(user_id, 'Sorry, only admins can send this command.')
        return
    try:
        target_user_id = int(message.text.split()[1])
    except:
        bot.send_message(user_id, 'Invalid command. Please use the format "/stop userid".')
        return
    if target_user_id not in chatting_users:
        bot.send_message(user_id, 'User is not currently chatting with the bot.')
        return
    chatting_users[target_user_id] = False
    bot.send_message(target_user_id, 'You may have to pay to use this bot. \nFor more: [Contact Me](https://t.me/gladson1)', parse_mode='Markdown')
    bot.send_message(user_id, 'Stopped chatting with user {}.'.format(target_user_id))


@bot.message_handler(commands=['unstop'])
def unstop_chatting(message):
    user_id = message.chat.id
    if user_id != 5214644649: # replace this with your user ID
        bot.send_message(user_id, 'Sorry, only admins can send this command.')
        return
    try:
        target_user_id = int(message.text.split()[1])
    except:
        bot.send_message(user_id, 'Invalid command. Please use the format "/unstop userid".')
        return
    if target_user_id not in chatting_users:
        bot.send_message(user_id, 'User is not known to the bot.')
        return
    chatting_users[target_user_id] = True
    bot.send_message(target_user_id, 'Your chat started again.')
    bot.send_message(user_id, 'Started chatting with user {} again.'.format(target_user_id))


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    user_id = message.chat.id
    if user_id not in chatting_users:
        bot.send_message(user_id, f"#Hello! Your ID is: {user_id}")
        chatting_users[user_id] = True
    if not chatting_users.get(user_id, False):
        bot.send_message(target_user_id, 'You may have to pay to use this bot. \nFor more: [Contact Me](https://t.me/gladson1)', parse_mode='Markdown')
        return
    if not check_user_in_channel(user_id):
        bot.send_message(user_id, 'Please join [@MAALGAARIIN](https://t.me/maalgaariin) to use me.', parse_mode='Markdown')
        return
    bot.send_chat_action(user_id, 'typing')
    msg = message.text
    response = rsp(msg, "gpt-2")
    bot.send_message(user_id, response)


print('bot start running')
while True:
    try:
        bot.polling()
    except Exception as e:
        print("An error has occurred:", e)
