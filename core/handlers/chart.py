import matplotlib.pyplot as plt
import os
from telebot import TeleBot, types
from telebot.types import Message
from Model import storage 

# Function to generate the pie chart and save it
def generate_expense_chart(user_id):
    finance = storage.get_user_data(user_id)

    if not finance.expenses:
        return None  # No expenses recorded

    # Aggregate expenses by category
    category_totals = {}
    for expense in finance.expenses:
        category_totals[expense.category] = category_totals.get(expense.category, 0) + expense.amount

    categories = list(category_totals.keys())
    amounts = list(category_totals.values())

    # Define colors
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0', '#ffb3e6']

    # Create pie chart
    plt.figure(figsize=(6,6))
    plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140, colors=colors, wedgeprops={'edgecolor': 'black'})
    plt.title("📊 Expense Breakdown")

    # Save the chart image
    img_path = f"expense_chart_{user_id}.png"
    plt.savefig(img_path)
    plt.close()

    return img_path  # Return the image file path

def register(bot):
    @bot.message_handler(commands=['view_chart'])
    def send_expense_report(message: Message):
        try:
            user_id = message.from_user.id
            img_path = generate_expense_chart(user_id)

            if img_path:
                with open(img_path, 'rb') as img:
                    bot.send_photo(message.chat.id, img, caption="📊 Here is your expense report!")
                os.remove(img_path)  # Delete the image after sending
            else:
                bot.reply_to(message, "📭 No expenses recorded yet.")
        
        except Exception as e:
            bot.reply_to(message, f"⚠️ Error: {str(e)}")
