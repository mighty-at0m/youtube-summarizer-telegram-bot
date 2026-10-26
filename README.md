# YouTube Summarizer Telegram Bot

Send this bot any YouTube link and it replies with an AI summary: a one-line TL;DR, 5 key points, and who it's worth watching for.

Built step by step on YouTube: [@dmightyatom](https://www.youtube.com/@dmightyatom)

## Setup

1. Install Python 3.10+.
2. Get a bot token: message [@BotFather](https://t.me/BotFather) on Telegram, send `/newbot`, follow the steps.
3. Get a free Gemini API key at [Google AI Studio](https://aistudio.google.com/apikey).
4. Install and configure:

```bash
pip install -r requirements.txt
cp .env.example .env   # then paste your token and key into .env
python bot.py
```

5. Open your bot in Telegram, send `/start`, then paste a YouTube link.

## Notes
- Works on videos that have captions (most do). Videos without captions return a friendly error.
- Run it on your own computer. Some cloud servers get blocked by YouTube when fetching captions.
- Long videos are trimmed to the first ~60k characters of transcript.

## License
MIT
