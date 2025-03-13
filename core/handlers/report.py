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
                f"• Total Budget: ${finance.budget:.2f}\n"
                f"• Total Spent: ${finance.total_spent:.2f}\n"
                f"• Remaining: ${remaining:.2f}\n\n"
                f"Progress: [{ '⬛' * int(progress//10) }{ '⬜' * (10 - int(progress//10)) }] "
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
            # Changed line vvv - use expense object
            for idx, expense in enumerate(finance.expenses[-5:], 1):  # Show last 5
                response.append(
                    f"{idx}. {expense.category}: ${expense.amount:.2f}"
                )
                
            response.append(f"\n💵 Total Spent: ${finance.total_spent:.2f}")
            
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
                "🕰 *Spending History* 🕰",
                "-----------------------------"
            ]
            
            # Add expenses with numbering
            for idx, expense in enumerate(finance.expenses, 1):  # Changed here
                response.append(
                    f"{idx}. {expense.category}: ${expense.amount:.2f}"
                )
                
            response.extend([
                "-----------------------------",
                f"💸 *Total Spent*: ${finance.total_spent:.2f}",
                f"💵 *Remaining*: ${(finance.budget - finance.total_spent):.2f}"
            ])
            

            bot.send_message(
                message.chat.id,
                "\n".join(response),
                parse_mode="Markdown"
            )
            
        except Exception as e:
            bot.reply_to(message, f"⚠️ Error: {str(e)}")
            print(f"History error: {e}")