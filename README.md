# Discord Bot

A feature-rich Discord bot built with Python and discord.py, integrating audio DSP, computer vision, AI-powered chat, music streaming, and more — all accessible through Discord slash commands.

## Features

### 🟦 Chat & AI
- **GPT-powered chat** — mention the bot to start a conversation powered by GPT-4o-mini, with per-channel message history
- **Imitation mode** (`/ape`, `/noape`) — the bot mimics a specified user's messages with GPT-based text transformation, optionally with TTS
- **Markus Rühl mode** (`/maggus`, `/nomaggus`) — responses in a distinct persona style
- **Birthday intents** — ask the bot natural-language questions about upcoming birthdays (e.g. *"Who has a birthday next?"*)

### 🟨 Audio Effects
- **/slowed** — time-stretch audio without pitch shift (PSOLA)
- **/slowed_reverb** — slowed + convolution reverb via impulse response
- **/reverb** — convolution reverb only
- **/stereo** — mono → stereo widening using the Haas effect
- **/mono** — stereo → mono mixdown

### 🟧 Graphics
- **/sw** — convert image or video to grayscale (OpenCV + FFmpeg)
- **/watermark** — overlay a watermark image on photos or videos with configurable position, scale, and transparency
- **/image** — generate an image with DALL·E 3 *(currently disabled)*

### 🟥 Image Analysis
- **/check** — analyse an image with GPT-4o vision and a custom prompt; result is stored in channel memory so you can follow up by mentioning the bot

### 🟩 Birthday Management
- **/setbirthday**, **/editbirthday**, **/viewbirthday**, **/viewbirthdays**, **/deletebirthday** — per-guild birthday registry backed by a JSON file
- Automatic midnight greeting sent to the guild's system channel on each member's birthday

### 🟪 Music
- **/play** — stream audio from YouTube or Spotify links via yt-dlp
- **/queue** — display the current queue and now-playing track
- **/skip** — skip one or more tracks
- **/clear_queue**, **/pause**, **/resume**, **/stop** — full playback control

## Tech Stack

| Layer | Libraries |
|---|---|
| Bot framework | discord.py 2.5+ |
| Audio DSP | scipy, librosa, soundfile, psola |
| Computer vision | OpenCV, Pillow, FFmpeg |
| AI / LLM | OpenAI SDK (GPT-4o-mini, DALL·E 3) |
| Music streaming | yt-dlp, spotipy, ffmpeg-python, PyNaCl |
| OCR | pytesseract, pylatexenc |
| HTTP | aiohttp |
| Package manager | Poetry |

## Getting Started

### Prerequisites
- Python 3.10+
- [Poetry](https://python-poetry.org/)
- FFmpeg on `PATH`
- Tesseract OCR on `PATH`

### Installation

```bash
# 1. Install dependencies
poetry install --no-root

# 2. Copy the example env file and fill in your credentials
cp .env.example .env
```

**.env** variables required:

```
BOT_TOKEN=
OPENAI_API_KEY=
SPOTIFY_CLIENT_ID=
SPOTIFY_CLIENT_SECRET=
```

```bash
# 3. Run the bot
poetry run python main.py
```

## Project Structure

```
cogs/            # discord.py Cogs (one per feature domain)
utils/           # Business logic used by Cogs
main.py          # Entry point — loads cogs and starts the bot
birthdays.json   # Persistent birthday store
pyproject.toml   # Poetry project config
.env             # Secrets (not committed)
```

## Slash Command Sync

The bot uses [Umbra's sync command](https://about.abstractumbra.dev/discord.py/2023/01/29/sync-command-example.html):

```
/sync ~   — sync to current guild
/sync *   — copy globals to current guild
/sync ^   — clear guild commands
/sync     — global sync
```

## Known Issues

- Music playback from some sources may be blocked — yt-dlp is occasionally detected as a bot by certain platforms. A fix is being investigated.

## Author

Heinrich Teich
