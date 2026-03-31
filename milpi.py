import os
from dotenv import load_dotenv
import discord
import asyncio
from scraper import scrape_library

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True # You MUST turn this on in the Dev Portal
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}. Waiting for the word.')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower() == "!events":
        status_msg = await message.channel.send("Searching the library site... let me cook.")
        
        try:
            # This is the magic line that lets Sync play with Async
            events = await asyncio.to_thread(scrape_library)
            
            if isinstance(events, str): # If the scraper returned an error string
                await message.channel.send(content=events)
                return
            if not events:
                await message.channel.send(content="No upcoming D&D events found. \nThe library is a wasteland. FML 😭")
                return

            response = "**⚔️ Milpitas Library D&D Sessions ⚔️**\n"
            for ev in events:
                response += f"\n**{ev['title']}**\n📅 {ev['date']} @ {ev['time']}\n🔗 <{ev['url']}>\n{'-'*20}"
            
            await message.channel.send(content=response)
        except Exception as e:
            await message.channel.send(content=f"Error: {e}")

client.run(TOKEN)