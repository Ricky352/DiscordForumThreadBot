import os
import discord
import asyncio
import schedule
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

TOKEN = os.getenv('TOKEN')
FORUM_CHANNEL_ID = int(os.getenv('FORUM_CHANNEL_ID'))

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
client = discord.Client(intents=intents)

async def create_thread_in_forum():
    now = datetime.now()
    thread_name = f"Daily Write Down {now.strftime('%d/%m/%Y')}"
    thread_content = (
        "<@&1049215981349781566> <@&1049216330647228436>\n\n"
        "```\n"
        "### What you have done yesterday\n"
        "{{ Answer here }}\n"
        "### What you are planning to do today\n"
        "{{ Answer here }}\n"
        "### What is currently blocking you from progressing\n"
        "{{ Answer here }}\n"
        "```"
    )
    forum_channel = client.get_channel(FORUM_CHANNEL_ID)
    if isinstance(forum_channel, discord.ForumChannel):
        await forum_channel.create_thread(
            name=thread_name,
            content=thread_content
        )
        print(f"Created thread: {thread_name}")

def job():
    asyncio.run_coroutine_threadsafe(create_thread_in_forum(), client.loop)

def schedule_jobs():
    schedule.every().monday.at("07:30").do(job)
    schedule.every().tuesday.at("07:30").do(job)
    schedule.every().wednesday.at("07:30").do(job)
    schedule.every().thursday.at("07:30").do(job)
    schedule.every().friday.at("07:30").do(job)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    schedule_jobs()

async def main():
    asyncio.create_task(client.start(TOKEN))
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)

asyncio.run(main())