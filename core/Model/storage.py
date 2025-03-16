# Model repo/storage.py
from datetime import datetime
from typing import Dict, List, Tuple

CURRENCY_DATA = {
    'USD': {'symbol': '$', 'name': 'US Dollar'},
    'EUR': {'symbol': '€', 'name': 'Euro'},
    'GBP': {'symbol': '£', 'name': 'British Pound'},
    'JPY': {'symbol': '¥', 'name': 'Japanese Yen'},
    'INR': {'symbol': '₹', 'name': 'Indian Rupee'},
    'CNY': {'symbol': '¥', 'name': 'Chinese Yuan'},
    'RUB': {'symbol': '₽', 'name': 'Russian Ruble'},
    'TRY': {'symbol': '₺', 'name': 'Turkish Lira'},
    'IRR': {'symbol': 'ریال', 'name': 'Iranian Rial'},
    'IRT': {'symbol': 'تومان', 'name': 'Iranian Toman'}}

class Expense:
    def __init__(self, category: str, amount: float):
        self.category = category
        self.amount = amount
        self.timestamp = datetime.now()

# In storage.py
class UserFinance:
    def __init__(self):
        self.budget = 0.0
        self.expenses = []
        self.total_spent = 0.0
        self.currency = 'IRT'
        self.currency_symbol = 'تومان'
        self.custom_categories = [] 
        
user_data: Dict[int, UserFinance] = {}

def get_user_data(user_id: int) -> UserFinance:
    if user_id not in user_data:
        user_data[user_id] = UserFinance()
    return user_data[user_id]