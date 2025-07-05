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

load_dotenv()  # Load environment variables from .env file
TOKEN = os.getenv('BOT_TOKEN')

"""------------------commands------------------"""

# functions that are executed when a user sends a command to the bot. these functions will be called when the user sends a respective command to the bot.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    await update.message.reply_text(f'Hello! {update.message.from_user.first_name} . How can I assist you today?')

"""------------------Bot Exec------------------"""
def main():
    """start the bot"""
    print("Starting the bot...")
    # create the bot application
    application = ApplicationBuilder().token(TOKEN).build()

    # add command handlers
    application.add_handler(CommandHandler("start", start))

    print("bot running...")
    application.run_polling()  # Start the bot and listen for updates

if __name__ == '__main__':
    main()  # Run the main function to start the bot
