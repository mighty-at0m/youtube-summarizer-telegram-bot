"""Telegram bot: send it a YouTube link, get an AI summary back.

Built for the @dmightyatom tutorial.
"""
import os
import re
import logging

from dotenv import load_dotenv
from google import genai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv()
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
ai = genai.Client(api_key=GEMINI_API_KEY)

YT_ID = re.compile(r"(?:v=|youtu\.be/|shorts/|embed/|live/)([A-Za-z0-9_-]{11})")


def video_id(text: str) -> str | None:
    """Pull the 11-character video ID out of any YouTube link."""
    m = YT_ID.search(text)
    return m.group(1) if m else None


def get_transcript(vid: str) -> str:
    """Download the video's captions as one block of text."""
    fetched = YouTubeTranscriptApi().fetch(vid, languages=["en", "en-US", "en-GB"])
    return " ".join(s.text for s in fetched)


def summarize(transcript: str) -> str:
    """Ask Gemini for a short, skimmable summary."""
    prompt = (
        "Summarize this YouTube video transcript for someone deciding whether to watch it.\n"
        "Give: a one-line TL;DR, then 5 key points as short bullets, then one 'worth watching if...' line.\n"
        "Plain text, no markdown headings.\n\n"
        f"Transcript:\n{transcript[:60000]}"
    )
    return ai.models.generate_content(model=MODEL, contents=prompt).text.strip()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me any YouTube link and I'll summarize it for you.")


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    vid = video_id(update.message.text or "")
    if not vid:
        await update.message.reply_text("That doesn't look like a YouTube link. Try again?")
        return
    await update.message.reply_text("Reading the video...")
    try:
        transcript = get_transcript(vid)
    except Exception as e:
        logging.warning("transcript failed for %s: %s", vid, e)
        await update.message.reply_text("Sorry, I couldn't get captions for that video. It may not have any.")
        return
    try:
        summary = summarize(transcript)
    except Exception as e:
        logging.error("AI failed: %s", e)
        await update.message.reply_text("The AI is busy right now. Try again in a minute.")
        return
    await update.message.reply_text(summary[:4000])


def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    logging.info("Bot is running. Press Ctrl+C to stop.")
    app.run_polling()


if __name__ == "__main__":
    main()
