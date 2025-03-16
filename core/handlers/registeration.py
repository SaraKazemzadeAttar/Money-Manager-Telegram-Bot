import telebot
import os

CHANNEL_ID = os.environ.get("CHANNEL_ID")
CHANNEL_LINK = os.environ.get("CHANNEL_LINK")

def register(bot):
    def is_member(bot , message):
        if not bot:
            return False

        user_info = bot.get_chat_member(CHANNEL_ID, message.from_user.id)
        if user_info.status not in ["administrator", "creator", "member"]:
            bot.send_message(
                message.chat.id,
                f"⚠️ Please subscribe to our channel to use this bot: [Join Channel]({CHANNEL_LINK})",
                parse_mode="Markdown",
            )
            return False
        return True

    @bot.message_handler(commands= ["register"])
    def setup_name(message):
        if not is_member(bot ,message):
            return
        bot.send_message(message.chat.id , "Please enter your first name .")
        bot.register_next_step_handler(message , callback = ask_lname)
        
    def ask_lname(message,*args, **kwargs):
        fname = message.text
        bot.send_message(message.chat.id ,"Please enter your last name .")
        bot.register_next_step_handler(message ,set_user , fname)

    def set_user(message , fname):
        lname = message.text
        bot.send_message(message.chat.id , f"Dear {fname} {lname} ,your registeration completed.\nThanks for using this bot.🤝")