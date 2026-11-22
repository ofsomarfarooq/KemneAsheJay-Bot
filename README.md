# KemneAsheJay — Discord Voice Logger & Anti-Spam Bot

A lightweight, 24/7 Discord utility and moderation bot built with Python (`discord.py`). It tracks who joins, leaves, or switches voice channels directly inside each voice channel's text chat, and automatically stops hacked-account spam waves before they flood your server.

## What It Does

- **Voice Channel Logger:** Posts real-time updates in the voice channel's built-in text chat whenever someone joins, leaves, or moves to another voice channel (ignores mute, deafen, and stream toggles).
- **Anti-Spam / Hacked Account Protection:**
  - Watches for repeated messages (both text and images/files) across all channels.
  - If a user sends the same message **5 times within 60 seconds**, the bot automatically:
    1. **Mutes (timeouts)** the user for **24 hours**.
    2. **Deletes** all of their spam messages.
    3. **Logs an alert** with the original message safely quoted (with `@everyone`/`@here` pings disabled) in case it was actually important.

---

## Step 1: Set Up Your Discord Bot

Before hosting, create your bot on Discord:

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications) and click **New Application**.
2. Open the **Bot** tab:
   - Click **Reset Token** and copy your token (keep it private).
   - Under **Privileged Gateway Intents**, turn **ON** **Message Content Intent** and click **Save Changes**.
3. Open **OAuth2 > URL Generator**:
   - **Scopes:** Check `bot`.
   - **Bot Permissions:** Check `View Channels`, `Send Messages`, `Manage Messages`, and `Moderate Members`.
4. Open the generated invite link and add the bot to your server.
5. **Important:** In your Discord server, go to **Server Settings > Roles** and drag the bot's role **above** regular member roles. If it's below them, Discord won't allow the bot to mute spammers.

---

## Step 2: Choose How to Host It

### Option A: Host 24/7 for Free on Wispbyte (No PC Needed)

1. Sign in to [Wispbyte](https://wispbyte.com/) and click **+ Create server**.
2. Choose **Python**, give your server a name, and click **Create server**.
3. Go to **Server Management > Files** and upload `bot.py` and `requirements.txt` from this repo.
4. Go to **Configuration > Startup** and change **App py file** from `main.py` to `bot.py`.
5. Go to **Configuration > Environment**, click **+ Create it** to make a `/.env` file, and add:
   - **Name:** `DISCORD_TOKEN`
   - **Value:** *(Paste your Discord bot token)*
   - Click **Save changes**.
6. Go to **Server Management > Console** and click **Start**. Once it prints `Logged in as <YourBot>`, it's live 24/7.

> **Note:** On Wispbyte's free plan, log in to the panel at least once every **14 days** (with adblocker off) to keep the server running.

---

### Option B: Run Locally on Your PC

Make sure you have **Python 3.10+** installed.

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/ofsomarfarooq/KemneAsheJay-Bot.git](https://github.com/ofsomarfarooq/KemneAsheJay-Bot.git)
   cd KemneAsheJay-Bot
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Add your bot token:**
   Create a file named `.env` in the project folder and add:
   ```env
   DISCORD_TOKEN=your_discord_bot_token_here
   ```
4. **Start the bot:**
   ```bash
   python bot.py
   ```
   *(The bot will stay online as long as the terminal window remains open.)*

---

## Customization

You can adjust the anti-spam settings at the top of `bot.py`:

| Setting | Default | What It Controls |
| :--- | :--- | :--- |
| `SPAM_THRESHOLD` | `5` | Number of identical messages needed to trigger a mute. |
| `TIME_WINDOW` | `60` | Time window (in seconds) to count repeated messages. |
| `MUTE_HOURS` | `24` | Length of the automatic timeout in hours. |
| `LOG_CHANNEL_ID` | `None` | Channel ID where alerts are sent (`None` posts in the channel where spam happened). |

*To use a dedicated `LOG_CHANNEL_ID`, turn on **Developer Mode** in Discord (**Settings > Advanced**), right-click your log channel → **Copy Channel ID**, and replace `None` with that number.*
