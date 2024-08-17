import discord
import os
from pystyle import Colorate, Colors
import asyncio
import webbrowser
import random
from datetime import datetime
import time

intents = discord.Intents.all()
client = discord.Client(intents=intents)

def read_tokens(file_path):
    with open(file_path, 'r') as file:
        tokens = [line.strip() for line in file.readlines() if line.strip()]
    return tokens

def center_text(text, width=80):
    try:
        term_size = os.get_terminal_size()
        width = term_size.columns
    except OSError:
        pass 

    return text.center(width)

def print_banner():
    banner =  """
▒███████▒ ▒█████   ██▒   █▓     █████▒██▓     ▒█████   ▒█████  ▓█████▄ ▓█████  ██▀███  
▒ ▒ ▒ ▄▀░▒██▒  ██▒▓██░   █▒   ▓██   ▒▓██▒    ▒██▒  ██▒▒██▒  ██▒▒██▀ ██▌▓█   ▀ ▓██ ▒ ██▒
░ ▒ ▄▀▒░ ▒██░  ██▒ ▓██  █▒░   ▒████ ░▒██░    ▒██░  ██▒▒██░  ██▒░██   █▌▒███   ▓██ ░▄█ ▒
  ▄▀▒   ░▒██   ██░  ▒██ █░░   ░▓█▒  ░▒██░    ▒██   ██░▒██   ██░░▓█▄   ▌▒▓█  ▄ ▒██▀▀█▄  
▒███████▒░ ████▓▒░   ▒▀█░     ░▒█░   ░██████▒░ ████▓▒░░ ████▓▒░░▒████▓ ░▒████▒░██▓ ▒██▒
░▒▒ ▓░▒░▒░ ▒░▒░▒░    ░ ▐░      ▒ ░   ░ ▒░▓  ░░ ▒░▒░▒░ ░ ▒░▒░▒░  ▒▒▓  ▒ ░░ ▒░ ░░ ▒▓ ░▒▓░
░░▒ ▒ ░ ▒  ░ ▒ ▒░    ░ ░░      ░     ░ ░ ▒  ░  ░ ▒ ▒░   ░ ▒ ▒░  ░ ▒  ▒  ░ ░  ░  ░▒ ░ ▒░
░ ░ ░ ░ ░░ ░ ░ ▒       ░░      ░ ░     ░ ░   ░ ░ ░ ▒  ░ ░ ░ ▒   ░ ░  ░    ░     ░░   ░ 
  ░ ░        ░ ░        ░                ░  ░    ░ ░      ░ ░     ░       ░  ░   ░     
░                      ░                                        ░                      
    """
    for line in banner.splitlines():
        print(Colorate.Horizontal(Colors.cyan_to_green, center_text(line)))

async def dm_flooder():
    os.system('title [Credits: Decompyle++ and h3xcolor] - DM Flooder 2.0')
    os.system('cls' if os.name == 'nt' else 'clear')
    tokens = read_tokens('input.txt')
    user_id = input(Colorate.Horizontal(Colors.cyan_to_green, "Введите ID пользователя: "))
    message_content = input(Colorate.Horizontal(Colors.cyan_to_green, "Введите текст для рассылки: "))
    message_count = int(input(Colorate.Horizontal(Colors.cyan_to_green, "Введите количество сообщений: ")))
    random_suffix = input(Colorate.Horizontal(Colors.cyan_to_green, "Добавлять случайные строки? (y/n): ")).strip().lower() == 'y'
    random_message = input(Colorate.Horizontal(Colors.cyan_to_green, "Добавлять случайные эмодзи? (y/n): ")).strip().lower() == 'y'
    
    emoji_count = 0
    if random_message:
         emoji_count = int(input(Colorate.Horizontal(Colors.cyan_to_green, "Введите количество эмодзи: ")))

    async def spam(token, uid, message, count, rs, rm, em):
        client = discord.Client(intents=intents)

        @client.event
        async def on_ready():
            await asyncio.sleep(1)
            print(Colorate.Horizontal(Colors.cyan_to_green, f"Авторизован как {client.user.name}"))
            await asyncio.sleep(1)
            target = await client.fetch_user(int(uid))
            emojis = [':smile:', ':laughing:', ':blush:', ':heart:', ':wink:']  # Примеры эмодзи

            for i in range(count):
                try:
                    msg = message
                    if rs:
                        msg += " -> " + ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', k=25))
                    
                    if rm:
                        msg += " -> " + ' '.join(random.choices(emojis, k=em))

                    await target.send(msg)
                    print(Colorate.Horizontal(Colors.cyan_to_green, f"Отправлено сообщение {i + 1} ~ {msg} ({client.user.name})"))

                    await asyncio.sleep(0.2)

                except discord.Forbidden:
                    print(Colorate.Horizontal(Colors.cyan_to_green, f"ЛС у {target.name} закрыты ({client.user.name})"))
                    break
                except discord.HTTPException as e:
                    if e.status == 429:
                        retry_after = e.retry_after
                        print(Colorate.Horizontal(Colors.cyan_to_green, f"Достигнут лимит запросов. Ожидание {retry_after} секунд."))
                        await asyncio.sleep(retry_after)
                    else:
                        print(Colorate.Horizontal(Colors.cyan_to_green, f"HTTP исключение: {e}"))
                except Exception as e:
                    print(Colorate.Horizontal(Colors.cyan_to_green, f"Неизвестная ошибка: {e}"))
        
        await client.start(token)

    tasks = [spam(token, user_id, message_content, message_count, random_suffix, random_message, emoji_count) for token in tokens]
    await asyncio.gather(*tasks)

def credits():
    os.system('title [Credits: Decompyle++ and h3xcolor] - Credits')
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Colorate.Horizontal(Colors.cyan_to_green, "Открытие Telegram канала..."))
    webbrowser.open("https://t.me/h3xcolor")
    input(Colorate.Horizontal(Colors.cyan_to_green, "Нажмите Enter для продолжения..."))

async def main_menu():
    while True:
        os.system('title [Credits: Decompyle++ and h3xcolor] - Menu')
        os.system('cls' if os.name == 'nt' else 'clear')
        print_banner()

        print(Colorate.Horizontal(Colors.cyan_to_green, center_text("1. DM Flooder 2.0")))
        print(Colorate.Horizontal(Colors.cyan_to_green, center_text("2. Credits        ")))
        print(Colorate.Horizontal(Colors.cyan_to_green, center_text("3. Exit           ")))

        choice = input(Colorate.Horizontal(Colors.cyan_to_green, "Выберите опцию: "))

        if choice == '1':
            await dm_flooder()
        elif choice == '2':
            credits()
        elif choice == '3':
            print("Выход...")
            break
        else:
            print(Colorate.Horizontal(Colors.cyan_to_green, "Неверный выбор. Попробуйте снова."))
            input(Colorate.Horizontal(Colors.cyan_to_green, "Нажмите Enter для продолжения..."))

if __name__ == "__main__":
    asyncio.run(main_menu())
