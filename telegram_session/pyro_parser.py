from pyrogram import Client, filters


def check(api_id, api_hash):
    app = Client("my_account", api_id=api_id, api_hash=api_hash)

    @app.on_message(filters.text & filters.private)
    async def echo(client, message):
        await message.reply(message.text)

    app.run()  # Automatically start() and idle()