# Model repo/storage.py
from datetime import datetime
from typing import Dict, List, Tuple

class Expense:
    def __init__(self, category: str, amount: float):
        self.category = category
        self.amount = amount
        self.timestamp = datetime.now()

class UserFinance:
    def __init__(self):
        self.budget: float = 0.0
        self.expenses: List[Expense] = []
        self.total_spent: float = 0.0
        
user_data: Dict[int, UserFinance] = {}

def get_user_data(user_id: int) -> UserFinance:
    if user_id not in user_data:
        user_data[user_id] = UserFinance()
    return user_data[user_id]