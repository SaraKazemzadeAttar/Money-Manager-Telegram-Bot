import telebot
from telebot import types
from telebot.types import Message
from typing import Tuple
from Model import storage

def register(bot) -> None:

    @bot.message_handler(commands=['set_budget'])
    def set_budget_command(message):
        try:
            msg = bot.reply_to(
                message,
                "💰 Please enter your monthly budget amount (e.g., 1500.50):"
            )
            bot.register_next_step_handler(msg, process_budget_amount)
        except Exception as e:
            bot.reply_to(message, f"⚠️ Error: {str(e)}")

    def process_budget_amount(message: Message):
        try:
            user_id = message.from_user.id
            amount = float(message.text)
            
            if amount <= 0:
                bot.reply_to(message, "❌ Budget must be a positive number!")
                return
                
            finance = storage.get_user_data(user_id)
            finance.budget = amount
            finance.total_spent = 0.0
            
            bot.send_message(
                message.chat.id,
                f"✅ Budget set to ${amount:.2f}\n"
                f"Use /add_expense to track spending\n"
                f"Check /view_budget for remaining balance"
            )
        except ValueError:
            bot.reply_to(message, "❌ Invalid amount! Please enter numbers only.")
        except Exception as e:
            bot.reply_to(message, f"⚠️ Error: {str(e)}")

    @bot.message_handler(commands=['add_expense'])
    def add_expense_command(message):
        try:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add('Food', 'Transport', 'Bills', 'Shopping', 'Other')
            
            msg = bot.reply_to(
                message,
                "🛒 Select or type an expense category:",
                reply_markup=markup
            )
            bot.register_next_step_handler(msg, process_expense_category)
        except Exception as e:
            bot.reply_to(message, f"⚠️ Error: {str(e)}")

    def process_expense_category(message):
        try:
            category = message.text.strip()
            msg = bot.reply_to(
                message,
                f"💸 Enter amount for {category}:",
                reply_markup=types.ReplyKeyboardRemove()
            )
            bot.register_next_step_handler(
                msg, 
                lambda m: process_expense_amount(m, category)
            )
        except Exception as e:
            bot.reply_to(message, f"⚠️ Error: {str(e)}")

    def process_expense_amount(message: Message, category: str):
        try:
            user_id = message.from_user.id
            finance = storage.get_user_data(user_id)
            
            if finance.budget <= 0:
                bot.reply_to(message, "❌ Please set a budget first using /set_budget")
                return
                
            amount = float(message.text)
            if amount <= 0:
                bot.reply_to(message, "❌ Amount must be positive!")
                return
                
            finance.expenses.append(storage.Expense(category, amount))
            finance.total_spent += amount
            remaining = finance.budget - finance.total_spent
            
            response = (
                f"📝 Expense added:\n"
                f"• Category: {category}\n"
                f"• Amount: ${amount:.2f}\n\n"
                f"💵 Remaining budget: ${remaining:.2f}"
            )
            
            if remaining < 0:
                response += "\n\n⚠️ WARNING: You've exceeded your budget!"
                
            bot.send_message(message.chat.id, response)
            
        except ValueError:
            bot.reply_to(message, "❌ Invalid amount! Please enter numbers only.")
        except Exception as e:
            bot.reply_to(message, f"⚠️ Error: {str(e)}")