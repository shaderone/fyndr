#script to reload the bot automatically when code changes are detected. It deals with files and reacts to changes in the file system.

import subprocess # to run shell commands
import sys # to access command line arguments
from watchdog.observers import Observer # to monitor file system events
import time # to sleep the script
import os # to handle file paths and environment variables
from watchdog.events import FileSystemEventHandler # to handle file system events

FILES_TO_WATCH = ["main.py", "db.py", "auto_reload.py"]  # List of files to watch for changes. You can add more files here if needed.

# this class defines what to do when a file change is detected
class FileChangeHandler(FileSystemEventHandler):
    """Handler for file system events to reload the bot when files change."""

    #script to reload the bot
    def __init__(self, script):
        self.script = script
        # the process_handle will be used to start and stop the bot
        self.process_handle = self.start()

    def start(self):
        """Start main.py"""
        process = subprocess.Popen([sys.executable, self.script])
        print(f"Starting new @fyndr_bot procees with with PID {process.pid}")
        return process
    
    # this method is called when a file change is detected
    def on_modified(self, event):
        #print(f"Detected change in file: {event.src_path} ")
        """Restart the bot when a file is modified."""
        # even.src_path = full path of the file that was modified

        if any(event.src_path.endswith(path) for path in FILES_TO_WATCH):
            print(f"\nFile {event.src_path} changed. Restarting the bot...")
            self.process_handle.kill()
            self.process_handle = self.start() # restart the bot and attach the new process handle

if __name__ == "__main__":
    event_handler = FileChangeHandler('main.py')  # Create an instance of the file change handler
    observer = Observer()  # Create an observer to monitor file changes. It is the engine that watches for file system events and notifies the handler when a change occurs.
    observer.schedule(event_handler, ".", recursive=False) # Schedule the handler to monitor the current directory for changes. recursive = false means it will not monitor subdirectories.
    observer.start()  # Start the observer to monitor file changes

    try:
        while True:
            time.sleep(1)  # Keep the script running to monitor file changes
    except KeyboardInterrupt:
        observer.stop() # Stop the observer on keyboard interrupt
        event_handler.process_handle.kill()  # Kill the bot process
        print("Bot stopped.")
    except Exception as e:
        observer.stop() # Stop the observer on any other exception
        print(f"An error occurred: {e}")
    finally:
        observer.join() # Wait for the observer to finish  