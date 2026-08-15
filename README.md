<div align="center">

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif">

# ⚡ EDGE RENAME BOT

**A powerful Telegram bot to rename, re-type, and enrich your media files — instantly.**

[![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python)](https://python.org)
[![Pyrogram](https://img.shields.io/badge/Pyrogram-2.0.83-green?style=for-the-badge)](https://pyrogram.org)
[![MongoDB](https://img.shields.io/badge/MongoDB-Motor-brightgreen?style=for-the-badge&logo=mongodb)](https://mongodb.com)
[![License](https://img.shields.io/badge/License-Apache%202.0-red?style=for-the-badge)](LICENSE)

<p>
  <a href="https://t.me/EDGE_Rename_Bot">
    <img src="https://img.shields.io/static/v1?label=Try+Bot&message=@EDGE_Rename_Bot&color=blue&style=for-the-badge&logo=telegram">
  </a>
  &nbsp;
  <a href="https://t.me/EdgeBotSupport">
    <img src="https://img.shields.io/static/v1?label=Support&message=@EdgeBotSupport&color=blueviolet&style=for-the-badge&logo=telegram">
  </a>
  &nbsp;
  <a href="https://t.me/EdgeBots">
    <img src="https://img.shields.io/static/v1?label=Updates&message=@EdgeBots&color=orange&style=for-the-badge&logo=telegram">
  </a>
</p>

[![GitHub Card](https://opengraph.githubassets.com/1/GeekLuffy/EDGE_RENAME)](https://github.com/GeekLuffy/EDGE_RENAME)

</div>

---

## 📌 What Is This?

**EDGE Rename Bot** is a self-hostable Telegram bot built with [Pyrogram](https://pyrogram.org) that lets users rename any file sent to it — with full control over:

- Interactive `/settings` dashboard for 1-tap preference toggling
- Output file type (Document / Video / Audio)
- Real-time task cancellation engine (instantly stop downloads/uploads)
- Non-blocking async FFmpeg remuxing & metadata injection
- Custom caption with dynamic variables
- Custom thumbnail
- Prefix & suffix injection
- Rich media metadata (title, author, artist, audio, subtitle, video) via `ffmpeg`
- Auto-forward renamed files to a personal dump channel

No more clunky desktop tools. Just send the file, type the new name, done.

---

## ✨ Features

| Feature | Description |
|---|---|
| 📁 **Rename Any File** | Supports documents, videos, and audio up to 2GB |
| ⚙️ **Interactive Dashboard** | Control all bot settings with `/settings` menu |
| 🛑 **Real-Time Cancel** | Abort active downloads/uploads instantly |
| ⚡ **Async FFmpeg** | Non-blocking background remuxing without bot lag |
| 🎥 **Choose Output Type** | Send as Document, Video, or Audio |
| 🖼️ **Custom Thumbnail** | Set a persistent thumbnail for all uploads |
| 📝 **Custom Caption** | Dynamic captions with `{filename}`, `{filesize}`, `{duration}` |
| 🏷️ **Prefix & Suffix** | Auto-inject tags around filenames safely |
| 🎬 **Metadata Editing** | Embed title, author, artist, video/audio/subtitle titles via ffmpeg |
| 📤 **Dump Channel** | Auto-forward renamed files to your own channel |
| 🔒 **Force Subscribe** | Restrict bot to channel members only |
| 📊 **Admin Stats** | CPU, RAM, disk usage dashboard for admins |
| 📣 **Broadcast** | Send messages to all users (admin only) |

---

## 🚀 Deploy

Choose your preferred platform:

### ☁️ Koyeb
[![Deploy to Koyeb](https://www.koyeb.com/static/images/deploy/button.svg)](https://app.koyeb.com/deploy?type=git&repository=github.com/Geekluffy/EDGE_RENAME&env[BOT_TOKEN]&env[API_ID]&env[API_HASH]&env[WEBHOOK]=True&env[ADMIN]&env[DB_URL]&env[DB_NAME]=EdgeRenameBot&env[FORCE_SUB]&env[START_PIC]&env[LOG_CHANNEL]=You%20Dont%20Need%20LogChannel%20To%20Remove%20This%20Variable&run_command=python%20bot.py&branch=main&name=pyro-rename)

### 🌐 Render
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/GeekLuffy/EDGE_RENAME)

### 🚂 Railway
<a href="https://graph.org/file/fabd75cd5043d2cfdc13d.jpg"><img src="https://railway.app/button.svg" alt="Deploy on Railway"></a>

### 💜 Heroku
<a href="https://heroku.com/deploy?template=https://github.com/GeekLuffy/EDGE_RENAME"><img src="https://www.herokucdn.com/deploy/button.svg" alt="Deploy on Heroku"></a>

### 🖥️ Self-Host (VPS / Local)

```bash
# Clone the repo
git clone https://github.com/GeekLuffy/EDGE_RENAME
cd EDGE_RENAME

# Install ffmpeg
sudo apt install ffmpeg -y

# Install dependencies
pip install -r requirements.txt

# Add your config (see variables below)
cp .env.example .env
nano .env

# Run
python bot.py
```

---

## ⚙️ Environment Variables

| Variable | Required | Description |
|---|---|---|
| `BOT_TOKEN` | ✅ | Your bot token from [@BotFather](https://t.me/BotFather) |
| `API_ID` | ✅ | Telegram App ID from [my.telegram.org](https://my.telegram.org) |
| `API_HASH` | ✅ | Telegram App Hash from [my.telegram.org](https://my.telegram.org) |
| `DB_URL` | ✅ | MongoDB connection string |
| `DB_NAME` | ❌ | Database name (default: `EdgeRenameBot`) |
| `ADMIN` | ✅ | Space-separated Telegram user IDs with admin access |
| `LOG_CHANNEL` | ❌ | Channel ID for bot logs (must start with `-100`) |
| `DUMP_CHANNEL` | ❌ | Default dump channel for all renamed files |
| `FORCE_SUB_1` | ❌ | Username of first force-subscribe channel (without `@`) |
| `FORCE_SUB_2` | ❌ | Username of second force-subscribe channel (without `@`) |
| `START_PIC` | ❌ | URL of start command media (image or video) |
| `WEBHOOK` | ❌ | Set `True` if hosting on a web server (default: `True`) |
| `PORT` | ❌ | Web server port for health checks (default: `8080`) |

> ⚠️ **Note:** Server must have `ffmpeg` installed for metadata features to work.

---

## 🤖 Bot Commands

```
/start        → Welcome message & quick menu
/settings     → Interactive settings dashboard
/metadata     → Toggle metadata embedding on/off
/settitle     → Set media title metadata
/setauthor    → Set author metadata
/setartist    → Set artist metadata
/setaudio     → Set audio track title
/setsubtitle  → Set subtitle track title
/setvideo     → Set video track title
/set_caption  → Set custom upload caption
/del_caption  → Remove custom caption
/see_caption  → View current caption
/set_prefix   → Add prefix to filenames
/del_prefix   → Remove prefix
/see_prefix   → View current prefix
/set_suffix   → Add suffix to filenames
/del_suffix   → Remove suffix
/see_suffix   → View current suffix
/setdump      → Set personal dump channel
/viewdump     → View current dump channel
/removedump   → Remove dump channel
/view_thumb   → View saved thumbnail
/del_thumb    → Delete saved thumbnail

── Admin Only ──
/stats        → System stats (CPU, RAM, disk, users)
/broadcast    → Send message to all users
/restart      → Restart the bot
```

---

## 🏗️ Project Structure

```
EDGE_RENAME/
├── bot.py                  # Entry point, Pyrogram client init
├── config.py               # Config + text constants + .env loader
├── route.py                # Aiohttp web server (for webhook mode)
├── requirements.txt        # Dependencies (Pyrogram, Motor, Pillow, etc.)
├── .env.example            # Environment variables template
├── Dockerfile
├── helper/
│   ├── database.py         # MongoDB async operations (Motor)
│   └── utils.py            # Async FFmpeg, safe paths, progress & cancel
└── plugins/
    ├── rename.py           # Core rename + upload + metadata + cancel logic
    ├── settings.py         # /settings interactive dashboard
    ├── start_&_cb.py       # /start command + all callback handlers
    ├── metadata.py         # Metadata set commands
    ├── thumb_&_cap.py      # Thumbnail + caption commands
    ├── prefix_suffix.py    # Prefix/suffix set/del/see commands
    ├── dump_settings.py    # Dump channel commands
    ├── admin_panel.py      # Admin stats + broadcast + restart
    ├── Force_Sub.py        # Force subscribe gate
    └── antinsfw.py         # NSFW filename filter (optional)
```


---

## 🐳 Docker

```bash
docker build -t edge-rename .
docker run -d \
  -e BOT_TOKEN=your_token \
  -e API_ID=your_id \
  -e API_HASH=your_hash \
  -e DB_URL=your_mongo_url \
  -e ADMIN=your_user_id \
  edge-rename
```

---

## 🙏 Credits & Acknowledgements

- [Pyrogram](https://github.com/pyrogram/pyrogram) — MTProto Python framework
- [Motor](https://github.com/mongodb/motor) — Async MongoDB driver
- [Hachoir](https://github.com/vstinner/hachoir) — Media metadata extraction
- [FFmpeg](https://ffmpeg.org) — Media metadata embedding
- Base inspiration: [TEAM-PYRO-BOTZ/PYRO-RENAME-BOT](https://github.com/TEAM-PYRO-BOTZ/PYRO-RENAME-BOT)

---

## 📄 License

Licensed under [Apache 2.0](LICENSE). Free to use, modify, and distribute — keep credits intact. ⭐

---

<div align="center">

**Made with ❤️ by [GeekLuffy](https://github.com/GeekLuffy)**

[![GitHub followers](https://img.shields.io/github/followers/GeekLuffy?style=social)](https://github.com/GeekLuffy)
[![GitHub stars](https://img.shields.io/github/stars/GeekLuffy/EDGE_RENAME?style=social)](https://github.com/GeekLuffy/EDGE_RENAME)

</div>
