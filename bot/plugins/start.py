from pyrogram import filters

from bot import bot


@bot.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        "Hello, I'm a bot.\n\n" "You can use /help to see all the commands."
    )
