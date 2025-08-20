import os
import json
from dotenv import load_dotenv
import discord
from discord.ext import commands
import lyricsgenius
import random

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GENIUS_TOKEN = os.getenv("GENIUS_ACCESS_TOKEN")

genius = lyricsgenius.Genius(GENIUS_TOKEN)
genius.remove_section_headers = True

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=";", intents=intents)


all_lyrics = []
LYRICS_FILE = "scarlxrd_lyrics.json"

def fetch_and_store_lyrics():
    print("Fetching Scarlxrd's songs from Genius...")
    artist = genius.search_artist("Scarlxrd", max_songs=200, sort="title")
    lyrics_list = []
    for song in artist.songs:
        lyrics_lines = [line for line in song.lyrics.split("\n") if line.strip()]
        lyrics_list.extend(lyrics_lines)
        
    with open(LYRICS_FILE, "w", encoding="utf-8") as f:
        json.dump(lyrics_list, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(lyrics_list)} lyrics lines locally.")
    return lyrics_list


@bot.event
async def on_ready():
    global all_lyrics
    print(f"Logged in as {bot.user}")

    if os.path.exists(LYRICS_FILE):
        with open(LYRICS_FILE, "r", encoding="utf-8") as f:
            all_lyrics = json.load(f)
        print(f"Loaded {len(all_lyrics)} lyrics lines from local file.")
    else:
        all_lyrics = fetch_and_store_lyrics()


@bot.command()
async def roast(ctx, *, target: str):
    try:
        if not all_lyrics:
            await ctx.send("Lyrics are not ready yet, try again in a few seconds.")
            return

        lyric_line = random.choice(all_lyrics)
        await ctx.send(f"{target}, {lyric_line}")
    except Exception as e:
        await ctx.send(f"Error fetching roast: {e}")


@bot.command()
async def scream(ctx, *, target: str):
    try:
        if not all_lyrics:
            await ctx.send("Lyrics are not ready yet, try again in a few seconds.")
            return

        target_upper = target.upper()
        lyric_line = random.choice(all_lyrics).upper()
        await ctx.send(f"{target_upper}, {lyric_line}")
    except Exception as e:
        await ctx.send(f"Error fetching scream roast: {e}")


@bot.command()
async def count(ctx, *, word: str):
    if not all_lyrics:
        await ctx.send("Lyrics are not ready yet, try again in a few seconds.")
        return

    word_lower = word.lower()
    total_count = sum(line.lower().count(word_lower) for line in all_lyrics)

    await ctx.send(f"The word '{word}' appears {total_count} times in the Scarlxrd lyrics!")

bot.run(TOKEN)