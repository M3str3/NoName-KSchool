from telethon.sync import TelegramClient
from datetime import datetime
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.types import Channel, User
from telethon.errors import FloodWaitError

import argparse
import json
import sqlite3
import os
import time

def log_message(message: str, log_type: str = "INFO"):
    print(f"[{log_type}] [{datetime.now().strftime('%H:%M:%S')}] {message}")

def initialize_database(database_path: str):
    sql_script = """
    CREATE TABLE IF NOT EXISTS channels (
        channel_id INTEGER PRIMARY KEY AUTOINCREMENT,
        channel_telegram_id INTEGER UNIQUE,
        channel_username TEXT UNIQUE,
        title TEXT,
        is_broadcast BOOLEAN
    );

    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        first_name TEXT,
        last_name TEXT
    );

    CREATE TABLE IF NOT EXISTS messages (
        message_id INTEGER PRIMARY KEY,
        channel_id INTEGER,
        date TEXT,
        text TEXT,
        user_id INTEGER,
        views INTEGER,
        forwards INTEGER,
        FOREIGN KEY(channel_id) REFERENCES channels(channel_id),
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    );

    CREATE TABLE IF NOT EXISTS interactions (
        interaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
        interaction_type TEXT,
        message_id INTEGER,
        user_id INTEGER,
        date TEXT,
        content TEXT,
        FOREIGN KEY(message_id) REFERENCES messages(message_id),
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    );
    """
    
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()
    cursor.executescript(sql_script)
    connection.commit()
    connection.close()
    log_message(f"Database initialized at {database_path}")

parser = argparse.ArgumentParser(description='Download messages from a Telegram channel.')
parser.add_argument('-c', '--channel', type=str, required=True, help='The Telegram channel username (e.g., @noname05716)')
parser.add_argument('--database', type=str, default='telegram.db', help='The SQLite database file (default: telegram.db)')
args = parser.parse_args()

def main():

    print("="*60)
    print(" "*25+"TgCrawler")
    print("Just a Telegram crawler")
    print("Author: M3str3<namestre3@protonmail.com>")
    print("="*60)
    config_file = "tgcrawler.json"
    log_message("Initializing the database...")
    if not os.path.exists(args.database):
        initialize_database(args.database)

    if os.path.exists(config_file):
        with open(config_file) as file:
            config = json.load(file)

        api_id = config['id_telegram']
        api_hash = config['hash_telegram']
    else:
        print("For more info check https://my.telegram.org/apps")
        api_id = input('id_telegram: ')
        api_hash = input('hash_telegram: ')
        config = {}
        with open(config_file,'w') as file:
            config['id_telegram'] = api_id
            config['hash_telegram'] = api_hash
            json.dump(config,file)

    client = TelegramClient('session', api_id, api_hash)
    connection = sqlite3.connect(args.database)
    cursor = connection.cursor()

    async def fetch_channel_info():
        async with client:
            channel = await client.get_entity(args.channel)
            full_channel = await client(GetFullChannelRequest(channel=channel))
            is_broadcast = isinstance(channel, Channel) and channel.broadcast
            
            cursor.execute('''
            INSERT OR IGNORE INTO channels (channel_telegram_id, channel_username, title, is_broadcast)
            VALUES (?, ?, ?, ?)
            ''', (channel.id, args.channel, channel.title, is_broadcast))
            connection.commit()
            log_message(f"Channel information for '{args.channel}' saved in the database.")
            return channel.id, is_broadcast

    async def fetch_and_store_messages(channel_telegram_id, is_broadcast):
        usuarios = []
        users_count = 0
        messages_count = 0
        async with client:
            async for message in client.iter_messages(args.channel, limit=None):
                while True:
                    try:
                        if message.date and message.text:
                            user_id = message.sender_id if not is_broadcast else None
                            if user_id and not is_broadcast and not user_id in usuarios:
                                usuarios.append(user_id)
                                users_count += 1

                                user = await client.get_entity(user_id)
                                if isinstance(user, User):
                                    cursor.execute('''
                                    INSERT OR IGNORE INTO users (user_id, username, first_name, last_name)
                                    VALUES (?, ?, ?, ?)
                                    ''', (user_id, user.username, user.first_name, user.last_name))

                            cursor.execute('''
                            INSERT OR IGNORE INTO messages (message_id, channel_id, date, text, user_id, views, forwards)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                            ''', (message.id, channel_telegram_id, message.date.strftime('%Y-%m-%d %H:%M:%S'), message.text, user_id, message.views, message.forwards))
                            messages_count += 1
                            connection.commit()
                        break
                    except FloodWaitError as e:
                        log_message(f"Flood wait error: waiting for {e.seconds} seconds", "ERROR")
                        for i in range(1,e.seconds):
                            print(f"\r[WAIT] {e.seconds}s | Actual: {i}s",end="")
                            time.sleep(1)
                        print()
                print(f"\r[INFO] [{datetime.now().strftime('%H:%M:%S')}] Messages received:{messages_count} Users received:{users_count}",end='')

        print()            
        log_message("Messages saved in the database.")

    async def main_async():
        channel_telegram_id, is_broadcast = await fetch_channel_info()
        await fetch_and_store_messages(channel_telegram_id, is_broadcast)

    with client:
        client.loop.run_until_complete(main_async())

    connection.close()
    log_message("Database connection closed.")

if __name__ == '__main__':
    main()
