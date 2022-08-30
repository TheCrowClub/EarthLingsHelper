from pyrogram import filters
from pyrogram.types import ForceReply
from mongox.exceptions import NoMatchFound

from bot import SUDOERS, bot
from bot.utilities.dbhelper import Helper


@bot.on_message(filters.command("fixme", ["/", "!", "$"]))
async def explain(_, message):
    if len(message.command) <= 2:
        return await message.reply("Example: fixme --explain 008")
    command = message.command[1]
    arguments = " ".join(message.command[2:])
    try:
        help_text = await Helper.query(Helper.help_keyword==arguments).get()
    except NoMatchFound:
        return await message.reply(f"No explaination found for {arguments}")
    return await message.reply(help_text.help_text)


keyword_and_help = []


@bot.on_message(filters.command("add", ["!", "/", "$"]) & filters.user(SUDOERS) & filters.private)
async def add_to_db(_, message):
    global keyword_and_help
    if len(message.command) < 2:
        return await message.reply("Example: $add keyword")
    keyword_and_help = []
    keyword_and_help.append(" ".join(message.command[1:]))
    await message.reply(
        "Kindly submit the help text for keyword.",
        reply_markup=ForceReply(True),
    )


@bot.on_message(filters.private & filters.user(SUDOERS) & filters.reply)
async def save_to_db(_, message):
    global keyword_and_help
    if bool(keyword_and_help):
        keyword = await Helper(help_keyword=keyword_and_help[0], help_text=message.text).insert()
        keyword_and_help = []
        return await message.reply(f"Saved!")
