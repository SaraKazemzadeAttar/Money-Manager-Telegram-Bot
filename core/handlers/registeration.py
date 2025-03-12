import telebot

def register(bot):
    @bot.message_handler(commands= ["register"])
    def setup_name(message):
        bot.send_message(message.chat.id , "Please enter your first name .")
        bot.register_next_step_handler(message , callback = assign_fname)
        
    def ask_lname(message,*args, **kwargs):
        fname = message.text
        bot.send_message(message.chat.id ,"Please enter your last name .")
        bot.register_next_step_handler(message ,assign_lname , fname)

    def set_user(message , fname):
        lname = message.text
        bot.send_message(message.chat.id , f"Dear {fname} {lname} ,your registeration completed.\nThanks for using this bot.💚")