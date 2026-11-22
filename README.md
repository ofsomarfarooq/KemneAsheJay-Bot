# KemneAsheJay — Discord Voice Logger & Anti-Spam Bot

A lightweight, 24/7 Discord utility and moderation bot built with **Python** and **`discord.py`**. It logs real-time voice channel activity directly inside each voice channel's built-in text chat and automatically protects servers against compromised-account spam waves.

---

## Features

- **Voice Channel Activity Logger**
  - Posts live updates in the voice channel's text chat when members **join**, **leave**, or **switch** voice channels.
  - Ignores mute, deafen, and stream toggles to keep chat clean.
- **Anti-Spam / Hacked Account Protection**
  - Tracks both **text** and **image/file attachments** (by filename and size) across all channels.
  - Automatically triggers when a user sends `5` identical messages within `60` seconds.
  - **24-Hour Timeout:** Mutes the offending account automatically.
  - **Auto-Cleanup:** Deletes all detected spam messages across every channel.
  - **Safe Audit Alert:** Logs the incident and safely quotes the original message (with `@everyone`/`@here` pings disabled) in case it was legitimate.
- **Secure Token Handling**
  - Uses `python-dotenv` to load the bot token from a `.env` file—no hardcoded secrets.

---

## Step 1: Create & Invite Your Discord Bot

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications) and click **New Application**.
2. Open the **Bot** tab on the left:
   - Click **Reset Token** and copy your bot token (keep this secret).
   - Scroll down to **Privileged Gateway Intents** and enable **Message Content Intent**, then click **Save Changes**.
3. Open **OAuth2 > URL Generator**:
   - Under **Scopes**, check `bot`.
   - Under **Bot Permissions**, check:
     - `View Channels`
     - `Send Messages`
     - `Manage Messages`
     - `Moderate Members` (Timeout Members)
4. Copy the generated URL, open it in your browser, and invite the bot to your server.
5. **Important (Role Hierarchy):** In your Discord server, go to **Server Settings > Roles** and drag the bot's role **above** regular member roles. Otherwise, Discord will block the bot from timing out spammers.

---

## Step 2: Host 24/7 for Free on Wispbyte (Recommended)

You can run this bot 24/7 without keeping your PC on using [Wispbyte](https://wispbyte.com/) (free tier, no credit card required):

1. **Create a Server:**
   - Sign in to Wispbyte and click **+ Create server**.
   - Select **Python** as the runtime, give your server a name, and click **Create server**.
2. **Upload Files:**
   - Open **Server Management > Files** and upload `bot.py` and `requirements.txt`.
3. **Set the Startup File:**
   - Go to **Configuration > Startup**.
   - Under **Variables**, change **App py file** from `main.py` to `bot.py`.
   - Leave **Requirements file** as `requirements.txt`.
4. **Add Your Bot Token:**
   - Go to **Configuration > Environment** and click **+ Create it** to create a `/.env` file.
   - Add a new variable:
     - **Name:** `DISCORD_TOKEN`
     - **Value:** *(Paste your Discord bot token)*
   - Click **Save changes**.
5. **Start the Bot:**
   - Go to **Server Management > Console** and click **Start**.
   - Once the console installs dependencies and prints `Logged in as <BotName>`, your bot is live 24/7.

> **Wispbyte Free Tier Note:** Log in to the Wispbyte dashboard at least once every **14 days** (with adblocker disabled on the panel) to keep the free server active.
