# Money-Manager-Telegram-Bot

A Telegram bot for personal finance management that helps users take control of their expenses, set budgets, and analyze spending patterns.
This project is available with this ID on telegram : @Save_Money_Minder_bot
## ✨ Features

### Current Implementation
- **In-Memory Storage** (Temporary Solution instead of database):
  - Set monthly budgets with `/set_budget`
  - Record expenses with categories using `/add_expense`
  - View budget status with `/view_budget`
  - Check expense history with `/history`
  - Generate basic spending reports
  - Contact support through interactive buttons

- **User Management**:
  - Registration system with `/register`
  - Channel membership verification

### Planned Database Integration 🔜
- **Persistent Storage**:
  - SQLite database implementation
  - User data persistence between sessions
  - Historical data analysis
  - Multi-user support with proper data isolation

- **Enhanced Features**:
  - Monthly budget rollovers
  - Expense categorization
  - Custom reporting periods
  - Data export functionality
  - Backup/restore capabilities

## 🛠️ Installation

1. Clone repository:
```bash
git clone https://github.com/SaraKazemzadeAttar/Money-Manager-Telegram-Bot
cd budget-manager-bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
```bash
cp .env.example .env
```
Edit `.env` with:
```ini
API_TOKEN=your_telegram_bot_token
CHANNEL_ID=your_channel_id
CHANNEL_LINK=your_channel_join_link
```

4. Run the bot:
```bash
python main.py
```

## 🚀 Usage

Start the bot in Telegram:
```text
/start - Initialize bot and show welcome message
/help - Display command list and instructions
/register - Create your account
```

Example workflow:
1. `/register` - Create account
2. `/set_budget 1500` - Set $1500 monthly budget
3. `/add_expense` → "Food" → "45.50" - Record lunch expense
4. `/view_budget` - Check remaining balance

## 📦 Database Roadmap

### Current Temporary Solution
⚠️ **Note**: The current version uses in-memory storage (Python dictionaries). Data will reset on bot restart.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/db-integration`)
3. Commit changes (`git commit -m 'Add database schema'`)
4. Push to branch (`git push origin feature/db-integration`)
5. Open Pull Request