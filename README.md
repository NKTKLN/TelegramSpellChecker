# ✍️ Telegram Spell Checker

A helpful **Telegram userbot** that checks your messages for spelling and grammar mistakes using **LanguageTool**.

## 📦 Requirements

* [Python 3.12+](https://www.python.org/downloads/)
* [Poetry](https://python-poetry.org/docs/#installation)
* [Task](https://taskfile.dev/) *(optional, for task automation)*
* A **Telegram account** (this is a **userbot**, not a regular bot)

## 📁 Project Structure

```files
TelegramSpellChecker/
├── app/
│   ├── __init__.py         # Package marker
│   ├── config.py           # Loads environment variables
│   ├── handlers.py         # Telegram message and command handlers
│   ├── logger.py           # Logging setup
│   └── main.py             # Main entry point
├── compose.yml             # Docker Compose configuration
├── Dockerfile              # Docker image definition
├── LICENSE.md              # License (MIT)
├── poetry.lock             # Poetry lock file
├── pyproject.toml          # Project metadata and dependencies
├── README.md               # This file
└── Taskfile.yml            # Automation tasks (optional)
```

## ⚙️ Setup

### 1. Clone the Repository

```bash
git clone https://github.com/NKTKLN/TelegramSpellChecker
cd TelegramSpellChecker
```

### 2. Install Dependencies

```bash
poetry install --no-root
poetry run playwright install
```

### 3. Configure Environment Variables

Create a `.env` file based on the provided example:

```env
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
```

> You can get your API credentials here: [https://my.telegram.org/](https://my.telegram.org/)

### 4. Log In to Telegram

```bash
poetry run python -m app.main --login
```

This will prompt for your phone number and authentication code, and create a session file.

### 5. Start the Bot

```bash
poetry run python -m app.main
```

## 🐳 Run with Docker

### 1. Build the Docker Image

```bash
docker build -t telegram-spell-checker .
```

### 2. First-Time Login (Creates Session File)

```bash
docker run -it -v $(pwd):/app telegram-spell-checker --login
```

After login, the session file will be stored locally.

### 3. Run the Bot (Session Exists)

```bash
docker run -v $(pwd):/app telegram-spell-checker
```

### 4. Using Docker Compose

```bash
docker compose up --build -d
```

## 💬 Bot Commands

* `!start` — enable spell and grammar checking
* `!stop` — disable checking
* `!status` — display current bot status

> ⚠️ The bot only checks **your own messages** (userbot mode).

## 🤔 ToDo

* [ ] Add a “dictionary” with words added by the user

## 📝 License

This project is licensed under the **MIT License**. See the [LICENSE.md](./LICENSE.md) file for more information.
