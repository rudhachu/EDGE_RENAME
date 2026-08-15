import math, time, os, asyncio, uuid, shutil
from pathlib import Path
from datetime import datetime
from pytz import timezone
from config import Config, Txt 
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def split_name_and_ext(filename: str) -> tuple:
    """Safely split filename into stem and extension without assuming 3-char ext length."""
    p = Path(filename)
    suffix = p.suffix  # e.g. '.mkv', '.mp4', '.tar'
    stem = p.stem
    return stem, suffix

def format_custom_filename(filename: str, prefix: str = None, suffix: str = None) -> str:
    """Formats the filename applying prefix and suffix safely without mangling extensions."""
    stem, ext = split_name_and_ext(filename)
    parts = []
    if prefix:
        parts.append(prefix.strip())
    parts.append(stem.strip())
    if suffix:
        parts.append(suffix.strip())
    
    formatted_name = " ".join(parts) + ext
    return formatted_name

async def run_async_ffmpeg(cmd: list) -> tuple:
    """Executes FFmpeg non-blockingly inside the asyncio event loop."""
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return process.returncode, stdout.decode('utf-8', errors='ignore'), stderr.decode('utf-8', errors='ignore')

def convert_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"

async def progress_for_pyrogram(current, total, ud_type, message, start):
    now = time.time()
    diff = now - start
    if round(diff % 5.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_time = TimeFormatter(milliseconds=elapsed_time)
        estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)
        time_left = (total - current) / speed
        elapsed_minutes = int(diff / 60)  # Calculate elapsed minutes
        elapsed_seconds = int(diff % 60)  # Calculate elapsed seconds

        num_boxes = 10
        completed_boxes = int(percentage / (100 / num_boxes))
        remaining_boxes = num_boxes - completed_boxes

        progress = "■" * completed_boxes + "□" * remaining_boxes

        text = f"Progress: [{progress}] {percentage:.1f}%\n"
        if ud_type == "Uᴩʟᴏᴀᴅ Sᴛᴀʀᴛᴇᴅ....":
            text += f"📤 Uploading: {humanbytes(current)} | {humanbytes(total)}\n"
        else:
            text += f"📥 Downloading: {humanbytes(current)} | {humanbytes(total)}\n"
        text += f"⚡️ Speed: {humanbytes(speed)}/s\n"
        text += f"⌛ ETA: {convert_time(time_left)}\n"
        text += f"⏱️ Time elapsed: {elapsed_minutes}m {elapsed_seconds}s"
        try:
            await message.edit(
                text=text,
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✖️ 𝙲𝙰𝙽𝙲𝙴𝙻 ✖️", callback_data="close")]])
            )
        except:
            pass


def humanbytes(size):    
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'ʙ'


def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "ᴅ, ") if days else "") + \
        ((str(hours) + "ʜ, ") if hours else "") + \
        ((str(minutes) + "ᴍ, ") if minutes else "") + \
        ((str(seconds) + "ꜱ, ") if seconds else "") + \
        ((str(milliseconds) + "ᴍꜱ, ") if milliseconds else "")
    return tmp[:-2] 

def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60      
    return "%d:%02d:%02d" % (hour, minutes, seconds)

async def send_log(b, u):
    if Config.LOG_CHANNEL:
        curr = datetime.now(timezone("Asia/Kolkata"))
        date = curr.strftime('%d %B, %Y')
        time = curr.strftime('%I:%M:%S %p')
        try:
            await b.send_message(
                Config.LOG_CHANNEL,
                f"**--Nᴇᴡ Uꜱᴇʀ Sᴛᴀʀᴛᴇᴅ Tʜᴇ Bᴏᴛ--**\n\nUꜱᴇʀ: {u.mention}\nIᴅ: `{u.id}`\nUɴ: @{u.username}\n\nDᴀᴛᴇ: {date}\nTɪᴍᴇ: {time}\n\nBy: {b.mention}"
            )
        except:
            pass
