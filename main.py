import os
import discord
import asyncio
import schedule
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

TOKEN = os.getenv('TOKEN')
FORUM_CHANNEL_ID = int(os.getenv('FORUM_CHANNEL_ID'))
tag_id = int(os.getenv('TAG_ID'))

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
client = discord.Client(intents=intents)

async def create_thread_in_forum():
    now = datetime.now()
    forum_channel = client.get_channel(FORUM_CHANNEL_ID)
    threads = forum_channel.threads
    threads_with_tag = [
        thread for thread in threads if any(tag.id == tag_id for tag in thread.applied_tags)
    ]
    thread_url = ""

    if threads_with_tag:
        latest_thread = sorted(threads_with_tag, key=lambda t: t.created_at, reverse=True)[0]
        thread_url = f"https://discord.com/channels/{forum_channel.guild.id}/{latest_thread.id}"
        print(f"Latest thread with tag ID {tag_id}: {thread_url}")
    else:
        print(f"No threads found with tag ID {tag_id}.")

    thread_name = f"Daily Write Down {now.strftime('%d/%m/%Y')}"
    thread_content = (
        "<@&1049215981349781566> <@&1049216330647228436>\n\n"
        f"Previous: {thread_url}\n\n"
        "Please answer the following questions:\n"
        "```\n"
        "### What you have done yesterday\n"
        "{{ Answer here }}\n"
        "### What you are planning to do today\n"
        "{{ Answer here }}\n"
        "### What is currently blocking you from progressing\n"
        "{{ Answer here }}\n"
        "```"
    )

    if isinstance(forum_channel, discord.ForumChannel):
        tag_to_apply = next((tag for tag in forum_channel.available_tags if tag.id == tag_id), None)
        await forum_channel.create_thread(
            name=thread_name,
            content=thread_content,
            applied_tags=[tag_to_apply]
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