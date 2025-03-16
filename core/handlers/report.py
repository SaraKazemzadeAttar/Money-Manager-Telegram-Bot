import telebot
from telebot.types import Message
from typing import Tuple, List
from Model import storage 

def register(bot):
    @bot.message_handler(commands=['view_budget'])
    def view_budget_command(message):
        try:
            user_id = message.from_user.id
            finance = storage.get_user_data(user_id)
            
            if finance.budget <= 0:
                bot.reply_to(message, "❌ No budget set! Use /set_budget first")
                return
                
            remaining = finance.budget - finance.total_spent
            progress = min(finance.total_spent / finance.budget * 100, 100)
            
            response = (
                f"📊 Budget Overview\n\n"
                f"• Total Budget: {finance.currency_symbol}{finance.budget:.3f}\n"
                f"• Total Spent: {finance.currency_symbol}{finance.total_spent:.3f}\n"
                f"• Remaining: {finance.currency_symbol}{remaining:.3f}\n\n"
                f"Progress: [{'⬛' * int(progress//10)}{'⬜' * (10 - int(progress//10))}] "
                f"{progress:.1f}% used"
            )
            
            bot.send_message(message.chat.id, response)
            
        except Exception as e:
            bot.reply_to(message, f"⚠️ Error: {str(e)}")

    @bot.message_handler(commands=['view_expenses'])
    def view_expenses_command(message: Message):
        try:
            user_id = message.from_user.id
            finance = storage.get_user_data(user_id)
            
            if not finance.expenses:
                bot.reply_to(message, "📭 No expenses recorded yet!")
                return
                
            response = ["📋 Recent Expenses:"]
            for idx, expense in enumerate(finance.expenses[-5:], 1):
                response.append(
                    f"{idx}. {expense.category}: {finance.currency_symbol}{expense.amount:.3f}"
                )
                
            response.append(f"\n💵 Total Spent: {finance.currency_symbol}{finance.total_spent:.3f}")
            
            bot.send_message(message.chat.id, "\n".join(response))
            
        except Exception as e:
            bot.reply_to(message, f"⚠️ Error: {str(e)}")

    @bot.message_handler(commands=['history'])
    def show_history_command(message: Message):
        """Display chronological spending history"""
        try:
            user_id = message.from_user.id
            finance = storage.get_user_data(user_id)
            
            if not finance.expenses:
                bot.reply_to(message, "📭 No expenses recorded yet!")
                return
                
            response = [
                "🕰 Spending History 🕰",
                "-----------------------------"
            ]
            
            for idx, expense in enumerate(finance.expenses, 1):
                response.append(
                    f"{idx}. {expense.category}: {finance.currency_symbol}{expense.amount:.3f}"
                )
                
            response.extend([
                "-----------------------------",
                f"💸 Total Spent: {finance.currency_symbol}{finance.total_spent:.3f}",
                f"💵 Remaining: {finance.currency_symbol}{(finance.budget - finance.total_spent):.3f}"
            ])
            
            bot.send_message(message.chat.id, "\n".join(response))
            
        except Exception as e:
            bot.reply_to(message, f"⚠️ Error: {str(e)}")
            print(f"History error: {e}")