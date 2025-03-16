import sqlite3
import os
from typing import List, Dict, Optional

class Database:
    def __init__(self, db_name: str = 'finance.db'):
        self.db_name = db_name
        self._run_migrations()
        
    def _get_connection(self) -> sqlite3.Connection:
        """Create and return a new database connection"""
        return sqlite3.connect(self.db_name)
    
    def _run_migrations(self):
        """Create tables if they don't exist"""
        with self._get_connection() as conn:
            # Create users table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    budget REAL DEFAULT 0,
                    currency TEXT DEFAULT 'rial'
                )
            ''')
            
            # Create expenses table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS expenses (
                    expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    amount REAL,
                    category TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES users(user_id)
                )
            ''')
            
            # Create categories table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS categories (
                    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    name TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(user_id)
                )
            ''')
            conn.commit()

class UserManager:
    def __init__(self, db: Database):
        self.db = db
        
    def create_user(self, user_id: int):
        """Add new user with default values"""
        with self.db._get_connection() as conn:
            conn.execute('''
                INSERT OR IGNORE INTO users (user_id)
                VALUES (?)
            ''', (user_id,))
            conn.commit()
    
    def set_budget(self, user_id: int, amount: float):
        """Update user's budget"""
        with self.db._get_connection() as conn:
            conn.execute('''
                UPDATE users 
                SET budget = ?
                WHERE user_id = ?
            ''', (amount, user_id))
            conn.commit()
    
    def set_currency(self, user_id: int, currency: str):
        """Update user's currency"""
        with self.db._get_connection() as conn:
            conn.execute('''
                UPDATE users 
                SET currency = ?
                WHERE user_id = ?
            ''', (currency.lower(), user_id))
            conn.commit()

    def is_registered(self, user_id: int) -> bool:
        """Check if user exists in database"""
        with self.db._get_connection() as conn:
            cursor = conn.execute(
                'SELECT 1 FROM users WHERE user_id = ?',
                (user_id,)
            )
            return cursor.fetchone() is not None

    def get_user(self, user_id: int) -> Optional[dict]:
        """Get full user data"""
        with self.db._get_connection() as conn:
            cursor = conn.execute(
                '''SELECT user_id, first_name, last_name, budget, currency 
                FROM users WHERE user_id = ?''',
                (user_id,))
            result = cursor.fetchone()
        return dict(result) if result else None
        
class ExpenseManager:
    def __init__(self, db: Database):
        self.db = db
        
    def add_expense(self, user_id: int, amount: float, category: str):
        """Record new expense"""
        with self.db._get_connection() as conn:
            conn.execute('''
                INSERT INTO expenses (user_id, amount, category)
                VALUES (?, ?, ?)
            ''', (user_id, amount, category))
            conn.commit()
    
    def get_expenses(self, user_id: int) -> List[Dict]:
        """Get all user expenses"""
        with self.db._get_connection() as conn:
            cursor = conn.execute('''
                SELECT category, amount, timestamp 
                FROM expenses 
                WHERE user_id = ?
                ORDER BY timestamp DESC
            ''', (user_id,))
            return [dict(row) for row in cursor.fetchall()]

class CategoryManager:
    def __init__(self, db: Database):
        self.db = db
        
    def add_category(self, user_id: int, name: str):
        """Add new custom category"""
        with self.db._get_connection() as conn:
            conn.execute('''
                INSERT INTO categories (user_id, name)
                VALUES (?, ?)
            ''', (user_id, name))
            conn.commit()
    
    def get_categories(self, user_id: int) -> List[str]:
        """Get all user categories"""
        with self.db._get_connection() as conn:
            cursor = conn.execute('''
                SELECT name FROM categories WHERE user_id = ?
            ''', (user_id,))
            return [row[0] for row in cursor.fetchall()]