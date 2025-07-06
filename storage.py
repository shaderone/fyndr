"""
This module handles file storage for the bot.
Files are stored in 'files/{user_id}/' with UUID names to avoid collisions.
"""

import os
from pathlib import Path
import uuid

BASE_DIR = Path(__file__).resolve().parent / 'files'  # Base directory for storing files

def get_storage_path(user_id): 
    """
    Create and return the user-specific storage directory.
    
    Args:
        user_id (int): Telegram user ID.
    
    Returns:
        the instance to the storage path for the user.
    """
    storage_path = BASE_DIR / str(user_id)
    #parents = true ensures that all parent directories are created if they do not exist
    #exist_ok = true ensures that no error is raised if the directory already exists.
    storage_path.mkdir(parents=True, exist_ok=True)
    return storage_path #the path object to the created folder

async def save_file(bot_instance, telegram_file, original_name, user_id):
    """
    Save a file to the user's storage directory with a unique name.

    Args:
        bot_instance: Telegram bot instance.
        telegram_file: Telegram File object.
        original_name: Original filename.
        user_id: Telegram user ID.

    Returns:
        dict: Contains 'saved_as' (UUID name) and 'file_path'.
    
    """
    storage_path = get_storage_path(user_id) # Get the user's storage path
    extension = Path(original_name).suffix  # Get the file extension
    unique_name = f"{uuid.uuid4().hex}{extension}"  # Generate a unique file name
    full_path = storage_path / unique_name  # Create the full file path
    
    # Download the file from Telegram
    await telegram_file.download_to_drive(full_path)

    return {
        #"file_name": original_name, # Original file name
        #"telegram_file_id": telegram_file.file_id,  # Telegram file ID
        "saved_as": unique_name,  # Unique file name saved in the system
        "file_path": str(full_path)  # Full path to the saved file
    }