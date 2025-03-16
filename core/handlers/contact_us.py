import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from typing import Dict, List
import os

CHANNEL_ID = os.environ.get("CHANNEL_ID")
CHANNEL_LINK = os.environ.get("CHANNEL_LINK")

CONTACT_LINKS: Dict[str, str] = {
    "LinkedIn": "https://www.linkedin.com/in/sara-kazemzade-attar",
    "GitHub": "https://github.com/SaraKazemzadeAttar",
    "Telegram": "https://t.me/sareattar"
}

BOT_DESCRIPTION = """
💼 *Budget & Expense Manager Bot* 💰

_Take control of your finances effortlessly! Here's what I can do:

📊 *Features*:
- Set monthly budgets for different categories
- Record expenses with categories and notes
- Generate detailed spending reports
- Receive remaining budget alerts
- Analyze spending patterns
- Export data to spreadsheets

🎯 *Getting Started*:
1. Register with /register to begin
2. Set your monthly budget using /set_budget
3. Add expenses with /add_expense
4. Check your budget status with /view_budget
5. Review expenses with /view_expenses

Type /help anytime for detailed instructions!
"""

HELP_TEXT = """
🛠 *Available Commands*:

🔹 _Account Setup_
/register - Create your account
/start - Show bot introduction

🔹 _Budget Management_
/set_budget - Set monthly budget limit
/view_budget - Check current budget status

🔹 _Expense Tracking_
/add_expense - Record new expense
/view_expenses - Show recent transactions
/history - View spending history

🔹 _Support_
/help - Show this help message
/contact - Contact developer support
"""

def create_contact_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)
    
    # Create buttons using dictionary items
    buttons = [
        InlineKeyboardButton(text=platform, url=url)
        for platform, url in CONTACT_LINKS.items()
    ]
    
    # Arrange buttons: first two in a row, then Telegram separately
    markup.add(*buttons[:2])  # LinkedIn and GitHub
    markup.add(buttons[2])    # Telegram
    
    return markup

def register(bot) -> None:
    
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

    @bot.message_handler(commands=["start"])
    def handle_contact_command(message):
        try:
            reply_text = (
                f"Hello {message.from_user.first_name}! , Welcome to this bot .\n {BOT_DESCRIPTION}"
            )
            markup = create_contact_keyboard()
            if not is_member(bot ,message):
                return
            bot.send_message(
                chat_id=message.chat.id,
                text=reply_text,
                reply_markup=markup
            )
        except Exception as e:
            error_message = "⚠️ Please try again later or contact with developer with /start command."
            bot.reply_to(message, "Error!")
            print(e)
            
    @bot.message_handler(commands=["help"])
    def handle_contact_command(message):
        try:
            if not is_member(bot ,message):
                return
            bot.send_message(
                chat_id=message.chat.id,
                text=HELP_TEXT,
            )
        except Exception as e:
            error_message = "⚠️ Please try again later or contact with developer with /start command."
            bot.reply_to(message, "Error!")
            print(e)