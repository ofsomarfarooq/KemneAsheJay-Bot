import os
import time
from collections import defaultdict
from datetime import timedelta
import discord
from dotenv import load_dotenv

load_dotenv()

# --- SETTINGS ---
SPAM_THRESHOLD = 5        # Triggers on the 5th identical message (change to 6 for "more than 5")
TIME_WINDOW = 60          # Seconds to look back for repeated messages
MUTE_HOURS = 24           # Mute duration in hours
LOG_CHANNEL_ID = None     # Optional: put a channel ID (e.g. 123456789012345678) to always log there; None = current channel

# Intents (message_content is required to read spam text)
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Tracks recent messages: user_messages[user_id][fingerprint] = [(timestamp, message), ...]
user_messages = defaultdict(lambda: defaultdict(list))


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")


# ==========================================
# 1. VOICE CHAT LOGGER (UNCHANGED)
# ==========================================
@client.event
async def on_voice_state_update(member, before, after):
    if before.channel == after.channel:
        return

    if before.channel is None and after.channel is not None:
        await after.channel.send(f"🟢 **{member.display_name}** joined the voice chat.")
    elif before.channel is not None and after.channel is None:
        await before.channel.send(f"🔴 **{member.display_name}** left the voice chat.")
    elif before.channel is not None and after.channel is not None:
        await before.channel.send(f"🔴 **{member.display_name}** moved to **{after.channel.name}**.")
        await after.channel.send(f"🟢 **{member.display_name}** joined from **{before.channel.name}**.")


# ==========================================
# 2. ANTI-SPAM / HACKED ACCOUNT PROTECTION
# ==========================================
@client.event
async def on_message(message):
    # Ignore bots and DMs
    if message.author.bot or not message.guild:
        return

    # Build a fingerprint from text + attached images/files (filename & size)
    text = message.content.strip().lower()
    attachments_sig = tuple(sorted((a.filename, a.size) for a in message.attachments))

    if not text and not attachments_sig:
        return

    fingerprint = (text, attachments_sig)
    now = time.time()
    user_id = message.author.id

    # Keep only messages sent within the TIME_WINDOW
    recent = [
        (ts, msg)
        for ts, msg in user_messages[user_id][fingerprint]
        if now - ts <= TIME_WINDOW
    ]
    recent.append((now, message))
    user_messages[user_id][fingerprint] = recent

    # Check if spam threshold is reached
    if len(recent) >= SPAM_THRESHOLD:
        spam_msgs = [msg for _, msg in recent]
        user_messages[user_id][fingerprint].clear()  # Reset tracker for this user

        # 1. Mute (Timeout) user for 24 hours
        muted_status = f"muted for **{MUTE_HOURS} hours**"
        try:
            await message.author.timeout(
                timedelta(hours=MUTE_HOURS),
                reason="Auto-mod: Spamming identical messages across channels"
            )
        except discord.Forbidden:
            muted_status = "**could not be muted** (missing permissions or higher role)"
        except Exception as e:
            muted_status = f"**could not be muted** ({e})"

        # 2. Delete all of the spam messages
        deleted_count = 0
        for spam_msg in spam_msgs:
            try:
                await spam_msg.delete()
                deleted_count += 1
            except (discord.NotFound, discord.Forbidden):
                pass

        # 3. Post update with the original message safely rewritten
        log_channel = client.get_channel(LOG_CHANNEL_ID) if LOG_CHANNEL_ID else message.channel
        original_text = message.content.strip() or "*[No text — image/file only]*"
        attachment_note = (
            f"\n📎 **Attachments:** {', '.join(a.filename for a in message.attachments)}"
            if message.attachments else ""
        )

        alert = (
            f"🚨 **{message.author.display_name}** ({message.author.mention}) has been {muted_status} "
            f"for spamming ({deleted_count} messages deleted).\n"
            f"**Original message (saved in case it was important):**\n"
            f">>> {original_text}{attachment_note}"
        )

        if log_channel:
            # AllowedMentions.none() prevents the bot from pinging @everyone if the spam had it
            await log_channel.send(alert, allowed_mentions=discord.AllowedMentions.none())


client.run(os.environ["DISCORD_TOKEN"])