"""FYNDR CORE"""

import os #creating files and handling file paths and getting environment variables
from dotenv import load_dotenv #loading environment variables from a .env file

#Every time a user interacts with your bot (sends a file, message, command, etc.), Telegram sends your bot a JSON object containing all details of that event. This object is called an Update.
#The telegram moudle has the raw apis and data-structures needed to interact with the bot. 
#Basically telegram module is enough to build a bot. but it'll be like building a web app with just html, css and js only.
from telegram import Update

#The telegram.ext module provides a high-level interface for building Telegram bots. It includes classes and functions to handle updates, commands, messages, and more.
#This module simplifies the process of creating a bot by providing a framework for handling updates and managing the bot's state.
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
"""ApplicationBuilder - This class is used to create an instance of the bot application. It allows you to configure the bot, add handlers, and start the bot.
CommandHandler - This class is used to handle commands sent by users. It takes a command name and a callback function that will be called when the command is received.
MessageHandler - This class is used to handle messages sent by users. It takes a filter and a callback function that will be called when a message matching the filter is received.
filters - This module provides various filters that can be used to filter messages, such as text messages, documents, photos, etc.
ContextTypes - This module provides context types that can be used to access the bot's context, such as the bot instance, the update, and the user data."""

from auto_reload import FileChangeHandler  # Importing the file change handler for auto-reloading the bot
# This handler will monitor file changes and restart the bot automatically when changes are detected.

from storage import save_file  # Importing the save_file function to handle file storage
from db import init_db, store_file

load_dotenv()  # Load environment variables from .env file
TOKEN = os.getenv('BOT_TOKEN')

"""------------------commands------------------"""

# functions that are executed when a user sends a command to the bot. these functions will be called when the user sends a respective command to the bot.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    await update.message.reply_text(f'Hello! {update.message.from_user.first_name} .The bot is still under construction. Please wait for the next update.  \n\n')

"""------------------Handlers------------------"""

async def handle_user_files(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle incoming files from users.
    This function will be called when a user sends a file to the bot.
    It will save the file and store its details in the database.
    """

    print("Received a file from user:", update.effective_user.id, update.effective_user.first_name)
    user = update.effective_user
    document = update.message.document

    if not document:
        await update.message.reply_text("Please send a valid file.")
        return
    
    #get the file
    telegram_file = await context.bot.get_file(document.file_id)
    original_name = document.file_name

    #save the file
    storage_details = await save_file(context.bot, telegram_file, original_name, user.id)

    store_file(user_id=user.id, file_name=original_name, saved_as=storage_details['saved_as'], telegram_file_id=telegram_file.file_id)

    await update.message.reply_text(
        f"File '{original_name}' saved as '{storage_details['saved_as']}'.\n"
        f"File path: {storage_details['file_path']}", parse_mode='Markdown'
    )

"""------------------Bot Exec------------------"""
def main():
    # Initialize the database
    init_db()  
    """start the bot"""
    print("Reloaded main.py")
    # create the bot application
    application = ApplicationBuilder().token(TOKEN).build()

    # add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_user_files))

    print("bot running...")
    application.run_polling()  # Start the bot and listen for updates

if __name__ == '__main__':
    main() 