import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from typing import Dict, List

CONTACT_LINKS: Dict[str, str] = {
    "LinkedIn": "https://www.linkedin.com/in/sara-kazemzade-attar",
    "GitHub": "https://github.com/SaraKazemzadeAttar",
    "Telegram": "https://t.me/sareattar"
}

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

def register(bot: telebot.TeleBot) -> None:
    @bot.message_handler(commands=["contact"])
    def handle_contact_command(message: Message) -> None:
        """Send contact options to the user."""
        try:
            reply_text = (
                f"📬 *Contact Options* 📬\n\n"
                f"Dear {message.from_user.first_name}! "
                "You can reach me through these platforms:"
            )
            
            markup = create_contact_keyboard()
            
            bot.send_message(
                chat_id=message.chat.id,
                text=reply_text,
                reply_markup=markup,
                parse_mode="Markdown"
            )
        except Exception as e:
            error_message = "⚠️ Failed to send contact information. Please try again later."
            bot.reply_to(message, error_message)
            # Consider adding logging here