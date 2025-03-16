import telebot
from telebot import types
from telebot.types import Message
from typing import Tuple
from Model import storage

user_states = {}

def register(bot) -> None:
    @bot.message_handler(commands=['set_budget'])
    def set_budget_command(message: Message):
        """First step: Currency selection"""
        try:
            user_id = message.from_user.id
            user_states[user_id] = {'awaiting_currency': True}
            
            markup = types.InlineKeyboardMarkup(row_width=2)
            buttons = [
                types.InlineKeyboardButton(
                    text=f"{data['symbol']} {data['name']}",
                    callback_data=f"SET_CURRENCY_{code}"
                ) for code, data in storage.CURRENCY_DATA.items()
            ]
            markup.add(*buttons)
            
            bot.send_message(
                message.chat.id,
                "💰 First select your currency:",
                reply_markup=markup
            )
            
        except Exception as e:
            bot.reply_to(message, f"⚠️ Error: {str(e)}")

    @bot.callback_query_handler(func=lambda call: call.data.startswith('SET_CURRENCY_'))
    def handle_currency_selection(call):
        """Second step: After currency selection, request budget"""
        try:
            user_id = call.from_user.id
            currency_code = call.data.split('_')[-1]
            
            if currency_code not in storage.CURRENCY_DATA:
                bot.answer_callback_query(call.id, "⚠️ Invalid currency selection", show_alert=True)
                return

            # Update user's currency
            finance = storage.get_user_data(user_id) 
            finance.currency = currency_code
            finance.currency_symbol = storage.CURRENCY_DATA[currency_code]['symbol']
            
            # Request budget amount
            msg = bot.send_message(
                call.message.chat.id,
                f"💰 Now enter monthly budget amount in {finance.currency_symbol} (e.g., 500.000 means five hundred thousand {finance.currency_symbol} ) :"
            )
            
            bot.answer_callback_query(call.id, f"Currency set to {currency_code}")
            bot.register_next_step_handler(msg, process_budget_amount)
            
        except Exception as e:
            bot.reply_to(call.message, f"⚠️ Error: {str(e)}")

    def process_budget_amount(message: Message):
        """Final step: Handle budget input"""
        try:
            user_id = message.from_user.id
            finance = storage.get_user_data(user_id)
            
            amount = float(message.text)
            if amount <= 0:
                raise ValueError("Negative amount")
                
            finance.budget = amount
            bot.reply_to(
                message,
                f"✅ Budget set to {finance.currency_symbol}{amount:.3f}\n"
                f"Use /add_expense to track spending"
            )
            
        except ValueError:
            bot.reply_to(message, "❌ Invalid amount! Please enter positive numbers only.")
        except Exception as e:
            bot.reply_to(message, f"⚠️ Error: {str(e)}")
            
    @bot.message_handler(commands=['add_expense'])
    def add_expense_command(message):
        try:
            user_id = message.from_user.id
            finance = storage.get_user_data(user_id)
            
            # Create category keyboard with distinctive "Create" button
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2)
            categories = [
                '🏥 Health', '🎉 Leisure', '🏠 Home', 
                '☕ Cafe', '🎓 Education', '🛒 Groceries',
                '🚌 Transportation', '📦 Other', '✨📌 Create New Category'
            ]
            
            # Add categories in organized rows
            markup.row(categories[0], categories[1])  # 🏥 Health, 🎉 Leisure
            markup.row(categories[2], categories[3])  # 🏠 Home, ☕ Cafe
            markup.row(categories[4], categories[5])  # 🎓 Education, 🛒 Groceries
            markup.row(categories[6], categories[7])  # 🚌 Transportation, 📦 Other
            markup.row(categories[8])  # ✨📌 Create New Category (standout row)
            
            msg = bot.reply_to(
                message,
                "📂 *Category Selection*\n\n"
                "Choose from common categories or create your own:",
                reply_markup=markup,
                parse_mode="Markdown"
            )
            bot.register_next_step_handler(msg, process_expense_category)
        except Exception as e:
            bot.reply_to(message, f"⚠️ Error: {str(e)}")

    def process_expense_category(message):
        try:
            user_id = message.from_user.id
            selected = message.text.strip()
            
            # Remove emojis for processing
            clean_selection = selected.replace('✨📌 ', '').strip()
            
            if clean_selection == 'Create New Category':
                # Handle custom category creation with special formatting
                msg = bot.reply_to(
                    message,
                    "What name would you like to use? (e.g., 'Pet Care' or 'Gaming')\n"
                    "Type your new category name:",
                    reply_markup=types.ReplyKeyboardRemove(),
                    parse_mode="Markdown"
                )
                bot.register_next_step_handler(msg, process_custom_category)
            else:
                # Extract clean category name from emoji-containing text
                category = selected.split(' ', 1)[1] if ' ' in selected else selected
                msg = bot.reply_to(
                    message,
                    f"💸 *Enter Amount for {category}:*\n"
                    f"Please type the amount in {storage.get_user_data(user_id).currency_symbol}",
                    reply_markup=types.ReplyKeyboardRemove(),
                    parse_mode="Markdown"
                )
                bot.register_next_step_handler(
                    msg, 
                    lambda m: process_expense_amount(m, category)
                )
        except Exception as e:
            bot.reply_to(message, f"⚠️ Error: {str(e)}")
    def process_custom_category(message):
        try:
            user_id = message.from_user.id
            finance = storage.get_user_data(user_id)
            new_category = message.text.strip()
            
            if not new_category:
                raise ValueError("Empty category name")
                
            # Add to user's custom categories
            if new_category not in finance.custom_categories:
                finance.custom_categories.append(new_category)
                
            # Proceed to amount entry
            msg = bot.reply_to(
                message,
                f"💸 Enter amount for {new_category}:",
                reply_markup=types.ReplyKeyboardRemove()
            )
            bot.register_next_step_handler(
                msg, 
                lambda m: process_expense_amount(m, new_category)
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
                f"• Amount: {finance.currency_symbol}{amount:.3f}\n\n"
                f"💵 Remaining budget: {finance.currency_symbol}{remaining:.3f}"
            )
            
            if remaining < 0:
                response += "\n\n⚠️ WARNING: You've exceeded your budget!"
                
            bot.send_message(message.chat.id, response)
            
        except ValueError:
            bot.reply_to(message, "❌ Invalid amount! Please enter numbers only.")
        except Exception as e:
            bot.reply_to(message, f"⚠️ Error: {str(e)}")